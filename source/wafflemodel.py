import source.thermalfunctions as tf


WATER_CONDUCTIVITY = 0.599
WATER_CAPACITY = 4200.0
WATER_BOILING_TEMPERATURE = 100.0
WATER_EVAPORATION_HEAT = 2.26 * 10 ** 6


class WaffleLayer:
	def __init__(self, dry_mass: float,  water_mass: float, temperature: float):
		if temperature > 100:
			raise ValueError("Starting temperature exceeds 100 degree Celsius!")
		if temperature < 0:
			raise ValueError("Starting temperature lower then 0 degree Celsius!")
		self.__dry_mass = 0
		self.set_dry_mass(dry_mass)
		self.__water_mass = 0
		self.set_water_mass(water_mass)
		self.__temperature = temperature
		self.__energy_gained = 0.0

	def set_dry_mass(self, mass) -> bool:
		if mass < 0.0:
			raise ValueError("Negative mass value!")
		self.__dry_mass = mass
		return True

	def set_water_mass(self, mass) -> bool:
		if mass < 0.0:
			raise ValueError("Negative mass value!")
		self.__water_mass = mass
		return True

	def set_temperature(self, new_temperature: float):
		self.__temperature = new_temperature

	def set_energy(self, new_energy):
		self.__energy_gained = new_energy

	def adjust_energy(self, temperature_change):
		self.__energy_gained += temperature_change

	def get_mass(self) -> float:
		return self.__dry_mass + self.__water_mass

	def get_water_mass(self) -> float:
		return self.__water_mass

	def get_humidity(self) -> float:
		return self.__water_mass / self.get_mass()

	def get_temperature(self) -> float:
		return self.__temperature

	def get_energy(self) -> float:
		return self.__energy_gained


class Waffle:

	def __init__(
			self, thickness: float, volume: float, temperature_capacity: float,
			temperature_conductivity: float, layer_count: int, humidity: float,
			default_temperature: float, mass: float):
		if (
				volume <= 0 or thickness <= 0 or temperature_capacity <= 0
				or temperature_conductivity <= 0 or humidity <= 0):
			raise ValueError("Zero or negative non-temperature attribute")
		self.__layer_volume = volume / layer_count
		self.__layer_thickness = thickness / layer_count
		self.__dry_temperature_capacity = (temperature_capacity - WATER_CAPACITY * humidity) / (1 - humidity)
		self.__dry_temperature_conductivity = (temperature_conductivity - WATER_CONDUCTIVITY * humidity) / (1 - humidity)
		layer_water_mass = (mass * humidity) / layer_count
		layer_dry_mass = (mass * (1 - humidity)) / layer_count
		self.__layer_list = []
		self.reinitialize_layer_list(layer_dry_mass, layer_water_mass, default_temperature, layer_count)

	def reinitialize_layer_list(
									self, layer_dry_mass: float, layer_water_mass: float, temperature: float,
									layer_count: int):
		self.__layer_list = [
			WaffleLayer(layer_dry_mass, layer_water_mass, temperature) for _ in range(layer_count)]

	# Function return flux ingoing/outgoing from external source
	def expose_layer(
			self, temperature: float, heat_conductivity: float,
			thickness: float, time: int, layer_id: int) -> float:
		if layer_id >= len(self.__layer_list):
			raise IndexError("Layer index out of range!")
		layer = self.__layer_list[layer_id]
		layer_conductivity = (
			self.__dry_temperature_conductivity * (1 - layer.get_humidity()) +
			WATER_CONDUCTIVITY * layer.get_humidity())
		layer_thermal_resistance = tf.thermal_resistance(
			self.__layer_thickness, layer_conductivity, self.__layer_volume / self.__layer_thickness)
		external_thermal_resistance = tf.thermal_resistance(
			thickness, heat_conductivity, thickness)
		flux = tf.temperature_flux(
			temperature, layer.get_temperature(),
			layer_thermal_resistance + external_thermal_resistance) * time / 1000
		if layer.get_temperature() > temperature:
			flux *= -1
		layer.adjust_energy(flux)
		return -1 * flux

	def conduct_layer_temperature(self, time):
		first_layer = self.__layer_list[0]
		first_layer_resistance = tf.thermal_resistance(
			self.__layer_thickness,
			(self.__dry_temperature_conductivity * (1 - first_layer.get_humidity()) +
				WATER_CONDUCTIVITY * first_layer.get_humidity()),
			self.__layer_volume / self.__layer_thickness)
		for layer_id in range(1, len(self.__layer_list)):
			second_layer = self.__layer_list[layer_id]
			second_layer_resistance = tf.thermal_resistance(
				self.__layer_thickness,
				(self.__dry_temperature_conductivity * (1 - first_layer.get_humidity()) +
					WATER_CONDUCTIVITY * second_layer.get_humidity()),
				self.__layer_volume / self.__layer_thickness)
			flux = tf.temperature_flux(
				first_layer.get_temperature(), second_layer.get_temperature(),
				first_layer_resistance + second_layer_resistance) * time / 1000
			if first_layer.get_temperature() < second_layer.get_temperature():
				flux *= -1
			first_layer.adjust_energy(-1 * flux)
			second_layer.adjust_energy(flux)
			first_layer = second_layer

	def apply_energy_change(self):
		for layer in self.__layer_list:
			layer_temperature_capacity = (
				self.__dry_temperature_capacity * (1 - layer.get_humidity()) +
				WATER_CAPACITY * layer.get_humidity())
			# Expected temperature if solution isn't boiling (expected_temp < 100C)
			expected_temperature = layer.get_temperature() + tf.temperature_change_from_energy(
				layer.get_energy(), layer_temperature_capacity, layer.get_mass())
			boiling_energy = 0.0
			# If layer is humid we try to calculate how much energy will be used for boiling
			if layer.get_humidity() > 0.0:
				# If expected temperature < 100C, boiling energy and percentage both equals 0
				boiling_energy = max(tf.energy_from_temperature_change(
					expected_temperature - 100.0, layer_temperature_capacity, layer.get_mass()), 0)
				boiled_percentage = tf.evaporated_liquid_proportion(
					boiling_energy, layer.get_water_mass(), WATER_EVAPORATION_HEAT)
				# If we can boil more water then layer have, we calculate temperature of dry layer after boiling is done
				if boiled_percentage >= 1.0:
					# Energy that is used for heating dry layer
					excess_energy = boiling_energy - tf.evaporation_energy(layer.get_water_mass(), WATER_EVAPORATION_HEAT)
					# Ensuring that layer is dry
					layer.set_water_mass(0.0)
					# Expected temperature will always be "100C + xC" since this part of code accessible only once per layer
					expected_temperature = 100.0 + tf.temperature_change_from_energy(
						excess_energy, self.__dry_temperature_capacity, layer.get_mass())
					layer.set_temperature(expected_temperature)
					layer.set_energy(0)
					# If layer isn't boiling or boiling partially previous calculations are used in the same way
					# But if layer was dried because of energy overflow we set new temp and mass values here and continue
					continue
				# Water mass change here only if some percent of water was boiled
				expected_water_mass = layer.get_water_mass() * (1 - boiled_percentage)
				if expected_water_mass <= 0.001:
					expected_water_mass = 0.0
				layer.set_water_mass(expected_water_mass)
			# Since Float type can behave strangely with "=="
			# We use if statement for situations when boiling temperature ~0
			if boiling_energy >= 0.00001:
				expected_temperature = layer.get_temperature() + tf.temperature_change_from_energy(
					layer.get_energy() - boiling_energy, layer_temperature_capacity, layer.get_mass())
			layer.set_temperature(expected_temperature)
			layer.set_energy(0)

	def get_layer_temperature(self, layer_id):
		return self.__layer_list[layer_id].get_temperature()

	def get_layer_humidity(self, layer_id):
		return self.__layer_list[layer_id].get_humidity()

	def get_layer_amount(self):
		return len(self.__layer_list)

	def __iter__(self):
		for layer in self.__layer_list:
			yield layer
