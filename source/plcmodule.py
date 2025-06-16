from pymodbus.client.tcp import ModbusTcpClient
from random import randint

TEMPERATURE_REGISTERS = (0, 2, 4, 6)
CURRENT_BAKING_TIME_REGISTER = 8
CONFIGURATION_BAKING_TIME_REGISTER = 9
CONFIGURATION_TEMPERATURE_REGISTER = 10
CONFIGURATION_GAP_REGISTER = 11


class PLCLink:
	def __init__(self, plc_id):
		self.__client = ModbusTcpClient(plc_id)

	def get_temperature(self) -> tuple:
		result = (
			(randint(200, 220), randint(200, 220)),
			(randint(200, 220), randint(200, 220)),
			(randint(200, 220), randint(200, 220)),
			(randint(200, 220), randint(200, 220)))
		'''		
		result = tuple(
			tuple(
				self.__client.read_holding_registers(register, 2).registers
			) for register in TEMPERATURE_REGISTERS)
		'''
		return result

	def get_current_baking_time(self) -> str:
		# time = self.__client.read_holding_registers(CURRENT_BAKING_TIME_REGISTER, 1).registers[0]
		time = 150000
		return f"{(time // 60000) % 60}:{(time // 1000) % 60}:{time % 1000}"

	def get_config_baking_time(self) -> str:
		# time = self.__client.read_holding_registers(CONFIGURATION_BAKING_TIME_REGISTER, 1).registers[0]
		time = 240000
		return f"{(time // 60000) % 60}:{(time // 1000) % 60}:{time % 1000}"

	def upload_config(self, gap: int, temperature: int, time: int):
		pass
		'''
		self.__client.write_register(CONFIGURATION_GAP_REGISTER, gap)
		self.__client.write_register(CONFIGURATION_TEMPERATURE_REGISTER, temperature)
		self.__client.write_register(CONFIGURATION_BAKING_TIME_REGISTER, time)
		'''