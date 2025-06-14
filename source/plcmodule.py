class PLCLink:
	def __init__(self, login: str, password: str, address: str):
		self.__login = login
		self.__password = password
		self.__address = address

	def open_connection(self) -> bool:
		pass

	def check_connection(self) -> bool:
		pass

	def request_data(self, request) -> dict:
		pass

	def write_register(self, request) -> bool:
		pass

	def close_connection(self) -> bool:
		pass
