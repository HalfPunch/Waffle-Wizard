class DBLink:
	def __init__(self, login: str, password: str, address: str):
		self.__login = login
		self.__password = password
		self.__address = address

	def open_connection(self) -> bool:
		pass

	def check_connection(self) -> bool:
		pass

	def select_from_db(self, request) -> dict:
		pass

	def insert_into_db(self, request) -> bool:
		pass

	def close_connection(self) -> bool:
		pass
