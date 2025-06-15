from mysql.connector import connect, Error


class DBLink:
	def __init__(self, host: str, user: str, password: str):
		self.__host = host
		self.__user = user
		self.__password = password
		self.__database = "waffle_management"

	def db_request_data(self, request) -> list:
		result: list
		with connect(host=self.__host, user=self.__user, password=self.__password) as connection:
			with connection.cursor() as cursor:
				cursor.execute(request)
				result = cursor.fetchall()
		return result

	def db_save_log(self, log, user_id):

		db_request = (
			f"INSERT INTO log (log_initiator_id, log_message, time) "
			f"VALUES ({user_id}, \"{log}\", NOW())")
		with connect(host=self.__host, user=self.__user, password=self.__password) as connection:
			with connection.cursor() as cursor:
				cursor.execute(db_request)

