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
	return q / (m * c)


def	energy_from_temperature_change(t: float, c: float, m: float):
	return m * c * t


def evaporation_energy(m: float, evaporation_heat: float):
	return m * evaporation_heat


def evaporated_liquid_proportion(heat_energy_received: float, m: float, evaporation_heat: float):
	return heat_energy_received / (m * evaporation_heat)


def contact_temperature(t1: float, d1: float, k1: float, t2: float, d2: float, k2: float):
	return (t1 * (k1 / d1) + t2 * (k2 / d2)) / ((k1 / d1) + (k2 / d2))


def is_energy_boiling_water(t: float, m: float, c: float, q: float) -> bool:
	return (q / (m * c) + t) >= 100.0