import source.wafflemodel as wm
import source.ovenmodel as om

if __name__ == '__main__':
    # Here we read recipe
    print("READING DATA...")
    weights = []
    attributes = []

    # Calculating all waffle params
    print("COMPILING DATA...")

    # Initialising oven model with waffle
    print("WAFFLE INITIALISATION...")
    waffle_init = {
        "thickness": 0.002,
        "volume": 0.002,
        "temperature_capacity": 3000,
        "temperature_conductivity": 0.56,
        "layer_count": 5,
        "humidity": 0.56,
        "temperature": 20,
        "mass": 0.1
    }
    plate_init = {
        "area": waffle_init["volume"] / waffle_init["thickness"],
        "thickness": 0.02,
        "density": 7200,
        "conductivity": 50,
        "capacity": 500
    }
    new_waffle = wm.Waffle(
        waffle_init["thickness"], waffle_init["volume"], waffle_init["temperature_capacity"],
        waffle_init["temperature_conductivity"], waffle_init["layer_count"], waffle_init["humidity"],
        waffle_init["temperature"], waffle_init["mass"])
    upper_plate = om.OvenPlate(
        plate_init["area"], plate_init["thickness"], plate_init["density"], plate_init["conductivity"],
        plate_init["capacity"], 200)
    lower_plate = om.OvenPlate(
        plate_init["area"], plate_init["thickness"], plate_init["density"], plate_init["conductivity"],
        plate_init["capacity"], 200)
    oven = om.Oven(upper_plate, lower_plate, new_waffle, True, True)
    print("SIMULATING...")

    print("CALCULATING...")

    print("LOGGING...")

    for layer in new_waffle:
        print(layer.get_temperature())
