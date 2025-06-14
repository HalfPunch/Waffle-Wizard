def thermal_resistance(thickness: float, conductivity: float, area: float) -> float:
	if thickness < 0.0 or conductivity <= 0 or area <= 0:
		raise ValueError("Incorrect attribute value")
	return thickness / (conductivity * area)


def temperature_flux(first_face_temperature: float, second_face_temperature: float, resistance: float):
	if resistance <= 0.0:
		raise ValueError("Incorrect resistance value")
	temp_dif = first_face_temperature - second_face_temperature
	return abs(temp_dif / resistance)


def temperature_change_from_energy(q: float, c: float, m: float):
	"""
	:param q: Energy that body received/emitted
	:param c: Body's temperature capacity
	:param m: Body's mass
	:return: Temperature change in body
	"""
	return q / (m * c)


def	energy_from_temperature_change(t: float, c: float, m: float):
	"""
	:param t: temperature change in body
	:param c: Body's temperature capacity
	:param m: Body's mass
	:return: Energy change in body
	"""
	return m * c * t


def evaporation_energy(m: float, evaporation_heat: float):
	"""
	:param m: Liquid mass
	:param evaporation_heat: Specific heat of evaporation for liquid
	:return: energy for portion of liquid to be evaporated
	"""
	return m * evaporation_heat


def evaporated_liquid_proportion(heat_energy_received: float, m: float, evaporation_heat: float):
	"""
	:param heat_energy_received: Energy that liquid received
	:param m: Liquid mass
	:param evaporation_heat: Specific heat of evaporation for liquid
	:return: proportion of liquid's mass that will be evaporated on energy gain
	"""
	return heat_energy_received / (m * evaporation_heat)


def contact_temperature(t1: float, d1: float, k1: float, t2: float, d2: float, k2: float):
	"""
	:param t1: First body temperature
	:param d1: First body thickness
	:param k1: First body temperature conductivity
	:param t2: Second body temperature
	:param d2: Second body thickness
	:param k2: Second body temperature conductivity
	:return: Contact temperature
	"""
	return (t1 * (k1 / d1) + t2 * (k2 / d2)) / ((k1 / d1) + (k2 / d2))


def is_energy_boiling_water(t: float, m: float, c: float, q: float) -> bool:
	"""
	:param t: starting temperature (Celsius)
	:param m: object's mass (Kilogram)
	:param c: temperature capacity
	:param q: energy acquired (Joules)
	:return: True if energy is enough to start boiling process, False otherwise
	"""
	return (q / (m * c) + t) >= 100.0
