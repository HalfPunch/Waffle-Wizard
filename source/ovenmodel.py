import source.wafflemodel as wm
import source.thermalfunctions as tf


BAKING_TIME_CAP = 300000


class OvenPlate:
	def __init__(
			self, area: float, thickness: float, density: float,
			t_conductivity: float, t_capacity: float, temperature: float):
		if area <= 0 or thickness <= 0 or density <= 0 or t_conductivity <= 0 or t_capacity <= 0:
			raise ValueError("Only temperature can be negative")
		self.__area = area
		self.__thickness = thickness
		self.__density = density
		self.__mass = area * thickness * density
		self.__t_conductivity = t_conductivity
		self.__t_capacity = t_capacity
		self.__temperature = temperature

	def set_area(self, new_area: float):
		if new_area <= 0:
			raise ValueError("Negative area")
		self.__area = new_area
		self.__mass = new_area * self.__thickness * self.__density

	def set_thickness(self, new_thickness: float):
		if new_thickness <= 0:
			raise ValueError("Negative thickness")
		self.__thickness = new_thickness
		self.__mass = self.__area * new_thickness * self.__density

	def set_density(self, new_density: float):
		if new_density <= 0:
			raise ValueError("Negative density")
		self.__density = new_density
		self.__mass = self.__area * self.__thickness * new_density

	def set_conductivity(self, new_conductivity: float):
		if new_conductivity <= 0:
			raise ValueError("Negative conductivity")
		self.__t_conductivity = new_conductivity

	def set_capacity(self, new_capacity: float):
		if new_capacity <= 0:
			raise ValueError("Negative capacity")
		self.__t_capacity = new_capacity

	def set_temperature(self, new_temperature: float):
		self.__temperature = new_temperature

	def get_area(self):
		return self.__area

	def get_thickness(self):
		return self.__thickness

	def get_density(self):
		return self.__density

	def get_mass(self):
		return self.__mass

	def get_conductivity(self):
		return self.__t_conductivity

	def get_capacity(self):
		return self.__t_capacity

	def get_temperature(self):
		return self.__temperature


class Oven:
	def __init__(
			self, upper_plate: OvenPlate, lower_plate: OvenPlate, waffle: wm.Waffle = None,
			is_upper_temp_stable: bool = True, is_lower_temp_stable: bool = False):
		self.__upper_plate = upper_plate
		self.__lower_plate = lower_plate
		self.__upper_plate_default_temp = upper_plate.get_temperature()
		self.__lower_plate_default_temp = lower_plate.get_temperature()
		self.__is_upper_temp_stable = is_upper_temp_stable
		self.__is_lower_temp_stable = is_lower_temp_stable
		self.__waffle = waffle
		self.__baking_tick_time = 1
		self.__baking_time = 0

	def set_baking_tick(self, time: int):
		if time <= 0:
			raise ValueError("Time attribute is negative or zero")
		self.__baking_tick_time = time

	def replace_plate(self, plate: OvenPlate, is_stable_temperature: bool, is_upper: bool):
		if is_upper:
			self.__upper_plate = plate
			self.__upper_plate_default_temp = plate.get_temperature()
			self.__is_upper_temp_stable = is_stable_temperature
		else:
			self.__lower_plate = plate
			self.__lower_plate_default_temp = plate.get_temperature()
			self.__is_lower_temp_stable = is_stable_temperature

	def set_plate_temperature(self, temperature: float, is_stable: bool, is_upper: bool):
		if is_upper:
			self.__upper_plate.set_temperature(temperature)
			self.__is_upper_temp_stable = is_stable
		else:
			self.__lower_plate.set_temperature(temperature)
			self.__is_lower_temp_stable = is_stable

	def put_new_waffle(self, new_waffle: wm.Waffle):
		self.__waffle = new_waffle

	def bake_waffle(self, cycles: int = 1, time: int = 1):
		if type(self.__waffle) is not wm.Waffle:
			raise AttributeError("Oven has no Waffle")
		for _ in range(cycles):
			# We calculate in/out going flux from plates if their temperature is unstable
			flux = self.__waffle.expose_layer(
				self.__upper_plate.get_temperature(), self.__upper_plate.get_conductivity(),
				self.__upper_plate.get_thickness(), time, 0)
			if not self.__is_upper_temp_stable:
				self.__upper_plate.set_temperature(
					self.__upper_plate.get_temperature() +
					tf.temperature_change_from_energy(
						flux, self.__upper_plate.get_capacity(), self.__upper_plate.get_mass()))
			flux = self.__waffle.expose_layer(
				self.__lower_plate.get_temperature(), self.__lower_plate.get_conductivity(),
				self.__lower_plate.get_thickness(), time, -1)
			if not self.__is_lower_temp_stable:
				self.__lower_plate.set_temperature(
					self.__lower_plate.get_temperature() +
					tf.temperature_change_from_energy(
						flux, self.__lower_plate.get_capacity(), self.__lower_plate.get_mass()))
			self.__waffle.conduct_layer_temperature(time)
			self.__waffle.apply_energy_change()
			self.__baking_time += time

	def bake_until_ready(self) -> bool:
		if type(self.__waffle) is not wm.Waffle:
			raise AttributeError("Oven has no Waffle")
		temperature_change = self.__waffle.get_layer_temperature(-1)
		humidity_change = self.__waffle.get_layer_humidity(-1)
		self.bake_waffle(cycles=self.__waffle.get_layer_amount())
		temperature_change = self.__waffle.get_layer_temperature(-1) - temperature_change
		humidity_change = humidity_change - self.__waffle.get_layer_humidity(-1)
		while not self.is_waffle_burnt() and (self.__baking_time < BAKING_TIME_CAP):
			if self.is_waffle_ready():
				return True
			temperature_change = self.__waffle.get_layer_temperature(-1)
			humidity_change = self.__waffle.get_layer_humidity(-1)
			self.bake_waffle(time=self.__baking_tick_time)
			temperature_change = self.__waffle.get_layer_temperature(-1) - temperature_change
			humidity_change = humidity_change - self.__waffle.get_layer_humidity(-1)
		return False

	def is_waffle_burnt(self):
		if type(self.__waffle) is not wm.Waffle:
			raise AttributeError("Oven has no Waffle")
		return self.__waffle.get_layer_temperature(0) >= 180 or (self.__waffle.get_layer_temperature(-1) >= 180)

	def is_waffle_ready(self):
		if type(self.__waffle) is not wm.Waffle:
			raise AttributeError("Oven has no Waffle")
		for layer_id in range(self.__waffle.get_layer_amount()):
			if self.__waffle.get_layer_humidity(layer_id) > 0.01:
				return False
		return not self.is_waffle_burnt()

	def reset_oven(self):
		self.__upper_plate.set_temperature(self.__upper_plate_default_temp)
		self.__lower_plate.set_temperature(self.__lower_plate_default_temp)
		self.reset_time()

	def reset_time(self):
		self.__baking_time = 0

	def get_time(self):
		return self.__baking_time
