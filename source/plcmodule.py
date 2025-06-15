from pymodbus.client.tcp import ModbusTcpClient

TEMPERATURE_REGISTERS = (0, 2, 4, 6)
CURRENT_BAKING_TIME_REGISTER = 8
CONFIGURATION_BAKING_TIME_REGISTER = 9
CONFIGURATION_TEMPERATURE_REGISTER = 10
CONFIGURATION_GAP_REGISTER = 11


class PLCLink:
	def __init__(self, plc_id):
		self.__client = ModbusTcpClient(plc_id)

	def get_temperature(self) -> tuple:
		return tuple(
			tuple(
				self.__client.read_holding_registers(register, 2).registers
			) for register in TEMPERATURE_REGISTERS)

	def get_current_baking_time(self) -> int:
		return self.__client.read_holding_registers(CURRENT_BAKING_TIME_REGISTER, 1).registers[0]

	def get_config_baking_time(self) -> int:
		return self.__client.read_holding_registers(CONFIGURATION_BAKING_TIME_REGISTER, 1).registers[0]

	def upload_config(self, gap, temperature, time):
		self.__client.write_register(CONFIGURATION_GAP_REGISTER, gap)
		self.__client.write_register(CONFIGURATION_TEMPERATURE_REGISTER, temperature)
		self.__client.write_register(CONFIGURATION_BAKING_TIME_REGISTER, time)
