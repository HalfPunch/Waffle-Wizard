import hashlib
from tkinter import *
from tkinter import ttk
from source.dbmodule import DBLink
from source.plcmodule import PLCLink
from mysql.connector import Error

H1_TEXT_FONT = ("Arial", 18)
TEXT_FONT = ("Arial", 12)


class UserInterface:
	def __init__(self):

		self.__main_window = Tk()
		self.__db_connector = DBLink("localhost", "admin", "admin")
		self.__plc_connector = PLCLink("192.168.1.9")
		self.__main_window.title("Waffle Wizard")
		self.__main_window.geometry("1080x960")
		self.__notebook_pages = dict()
		self.__ui_elements = dict()
		self.__notebook = ttk.Notebook()
		self.__notebook.pack(expand=True, fill=BOTH)
		self.__main_window.state('zoomed')
		self.__user_id = None
		self.__init_login()

	def __init_login(self):
		self.__notebook_pages["login"] = ttk.Frame(self.__notebook)
		self.__notebook_pages["login"].pack(fill=BOTH, expand=True)
		self.__notebook.add(self.__notebook_pages["login"], text="Login")

		# "Login page" label at the center of frame
		login_label = Label(self.__notebook_pages["login"], text="Login Page", font=H1_TEXT_FONT)
		login_label.place(relx=0.5, rely=0.5, anchor="center", y=-40)

		# Login and Password entry fields
		self.__ui_elements["login_entry_label"] = Label(
			self.__notebook_pages["login"], text="login:", font=TEXT_FONT)
		self.__ui_elements["login_entry_label"].place(relx=0.5, rely=0.5, anchor="e", y=20, x=-60)
		self.__ui_elements["login_entry"] = Entry(self.__notebook_pages["login"])
		self.__ui_elements["login_entry"].place(relx=0.5, rely=0.5, anchor="center", y=20)

		self.__ui_elements["password_entry_label"] = Label(
			self.__notebook_pages["login"], text="password:", font=TEXT_FONT)
		self.__ui_elements["password_entry_label"].place(relx=0.5, rely=0.5, anchor="e", y=50, x=-60)
		self.__ui_elements["password_entry"] = Entry(self.__notebook_pages["login"], show="*")
		self.__ui_elements["password_entry"].place(relx=0.5, rely=0.5, anchor="center", y=50)

		# Login confirmation button
		self.__ui_elements["login_confirmation_button"] = Button(
			self.__notebook_pages["login"], text="enter", font=TEXT_FONT, width=8,
			command=self.__button_logic_login_confirmation)
		self.__ui_elements["login_confirmation_button"].place(relx=0.5, rely=0.5, anchor="center", y=90)

		# Login or password error label
		self.__ui_elements["login_error_label"] = Label(
			self.__notebook_pages["login"], text="", font=TEXT_FONT, foreground="red")
		self.__ui_elements["login_error_label"].place(relx=0.5, rely=0.5, anchor="center", y=130)

		# Logout button
		self.__ui_elements["logout_button"] = Button(
			self.__notebook_pages["login"], text="Log out", font=TEXT_FONT, width=8, state="disabled",
			command=self.__button_logic_logout_button)
		self.__ui_elements["logout_button"].place(relx=1.0, rely=1.0, anchor="se", x=-5, y=-5)

	@staticmethod
	def __make_tuple_of_plc_monitoring_frames(master, frame_count) -> ():
		frame_var_list = [
			{f"frame": ttk.Frame(master, borderwidth=1, relief=SOLID)}
			for _ in range(frame_count)]
		for master_frame_id in range(frame_count):
			# Oven position label
			frame_var_list[master_frame_id]["position_label"] = Label(
				frame_var_list[master_frame_id]["frame"],
				text=f"Позиция: #{master_frame_id + 1}",
				font=H1_TEXT_FONT)
			frame_var_list[master_frame_id]["position_label"].pack()

			# Upper temperature label
			frame_var_list[master_frame_id]["upper_temp_label"] = Label(
				frame_var_list[master_frame_id]["frame"],
				text=f"T(Верх) = -C",
				font=TEXT_FONT,
				pady=10)
			frame_var_list[master_frame_id]["upper_temp_label"].pack()

			# Lower temperature label
			frame_var_list[master_frame_id]["lower_temp_label"] = Label(
				frame_var_list[master_frame_id]["frame"],
				text=f"T(Низ) = -C",
				font=TEXT_FONT)
			frame_var_list[master_frame_id]["lower_temp_label"].pack()

			# Display resulting frame
			frame_var_list[master_frame_id]["frame"].grid(row=0, column=master_frame_id, padx=5)
		return frame_var_list

	def __init_process_tab(self):
		self.__notebook_pages["process"] = ttk.Frame(self.__notebook)
		self.__notebook_pages["process"].pack(fill=BOTH, expand=True)
		self.__notebook.add(self.__notebook_pages["process"], text="Process")

		# Frame containing other frames
		self.__ui_elements["process_grid"] = ttk.Frame(
			self.__notebook_pages["process"], borderwidth=1, relief=SOLID, padding=(8, 10))
		self.__ui_elements["process_grid"].place(relx=0.5, rely=0.5, anchor="center")
		self.__ui_elements["process_grid_frame_var_list"] = UserInterface.__make_tuple_of_plc_monitoring_frames(
			self.__ui_elements["process_grid"], 4)
		self.__ui_elements["baking_time_label"] = Label(
			self.__notebook_pages["process"], text=f"Время выпечки - 00:00:000/00:00:000", font=TEXT_FONT)
		self.__ui_elements["baking_time_label"].place(
			relx=0.5, rely=0.5, anchor="center", y=-100)

	def __get_ingredients_from(self, db):
		pass

	def __init_recipe_tab(self):
		self.__notebook_pages["recipe"] = ttk.Frame(self.__notebook)
		self.__notebook_pages["recipe"].pack(fill=BOTH, expand=True)
		self.__notebook.add(self.__notebook_pages["recipe"], text="Recipe")

		self.__ui_elements["recipe_grid"] = ttk.Frame(self.__notebook_pages["recipe"])
		self.__ui_elements["recipe_grid"].place(relx=0.5, rely=0.5, anchor="center")

		self.__ui_elements["recipe_ingredient_grid"] = ttk.Frame(self.__ui_elements["recipe_grid"])
		self.__ui_elements["recipe_ingredient_grid"].grid(row=0, column=0, pady=10)

		self.__ui_elements["recipe_ingredient_add_list"] = ttk.Treeview(
			self.__ui_elements["recipe_ingredient_grid"], columns="name", show="headings")
		self.__ui_elements["recipe_ingredient_add_list"].grid(row=0, column=0, padx=20, rowspan=2)
		self.__ui_elements["recipe_ingredient_add_list"].heading("name", text="Ингредиент")
		for ingredient in (r"Мука,высший_сорт", r"Сахар,белый", "Молоко", "Яйцо", "Сода", "Соль"):
			self.__ui_elements["recipe_ingredient_add_list"].insert("", END, values=ingredient)

		self.__ui_elements["recipe_current_ingredient_list"] = ttk.Treeview(
			self.__ui_elements["recipe_ingredient_grid"], columns=("name", "mass"), show="headings")
		self.__ui_elements["recipe_current_ingredient_list"].grid(row=0, column=3, padx=20, rowspan=2)
		self.__ui_elements["recipe_current_ingredient_list"].heading("name", text="Ингредиент")
		self.__ui_elements["recipe_current_ingredient_list"].heading("mass", text="Масса, г")

		self.__ui_elements["recipe_mass_entry"] = Entry(
			self.__ui_elements["recipe_ingredient_grid"], font=TEXT_FONT, width=10)
		self.__ui_elements["recipe_mass_entry"].grid(row=0, column=1, padx=5, pady=5, sticky=SE)

		self.__ui_elements["recipe_add_button"] = Button(
			self.__ui_elements["recipe_ingredient_grid"], text="+", font=TEXT_FONT, height=1, width=2)
		self.__ui_elements["recipe_add_button"].grid(row=0, column=2, padx=5, pady=5, sticky=SW)

		self.__ui_elements["recipe_remove_button"] = Button(
			self.__ui_elements["recipe_ingredient_grid"], text="-", font=TEXT_FONT, height=1, width=2)
		self.__ui_elements["recipe_remove_button"].grid(row=1, column=1, columnspan=2, pady=5, sticky=N)

		self.__ui_elements["recipe_config_grid"] = ttk.Frame(self.__ui_elements["recipe_grid"])
		self.__ui_elements["recipe_config_grid"].grid(row=1, column=0, pady=10)

		self.__ui_elements["config_gap_label"] = Label(
			self.__ui_elements["recipe_config_grid"], text="Промежуток, мм")
		self.__ui_elements["config_gap_label"].grid(row=0, column=0, columnspan=2, padx=10, pady=10)
		self.__ui_elements["config_temperature_label"] = Label(
			self.__ui_elements["recipe_config_grid"], text="Температура, °C")
		self.__ui_elements["config_temperature_label"].grid(row=0, column=2, columnspan=2, padx=10, pady=10)
		self.__ui_elements["config_time_label"] = Label(
			self.__ui_elements["recipe_config_grid"], text="Время, мс")
		self.__ui_elements["config_time_label"].grid(row=0, column=4, columnspan=2, padx=10, pady=10)

		self.__ui_elements["config_gap"] = Entry(self.__ui_elements["recipe_config_grid"])
		self.__ui_elements["config_gap"].grid(row=1, column=0, columnspan=2, padx=10, pady=10)
		self.__ui_elements["config_temperature"] = Entry(self.__ui_elements["recipe_config_grid"], state="disabled")
		self.__ui_elements["config_temperature"].grid(row=1, column=2, columnspan=2, padx=10, pady=10)
		self.__ui_elements["config_time"] = Entry(self.__ui_elements["recipe_config_grid"], state="disabled")
		self.__ui_elements["config_time"].grid(row=1, column=4, columnspan=2, padx=10, pady=10)

		self.__ui_elements["config_new_config_button"] = Button(
			self.__ui_elements["recipe_config_grid"], text="Подготовить конфигурацию")
		self.__ui_elements["config_new_config_button"].grid(row=2, column=0, columnspan=3, padx=10, pady=10)
		self.__ui_elements["config_load_config_button"] = Button(
			self.__ui_elements["recipe_config_grid"], text="Загрузить конфигурацию", state="disabled")
		self.__ui_elements["config_load_config_button"].grid(row=2, column=3, columnspan=3, padx=10, pady=10)

	def __destroy_secured_tabs(self):
		self.__notebook_pages["process"].destroy()
		del self.__notebook_pages["process"]
		self.__notebook_pages["recipe"].destroy()
		del self.__notebook_pages["recipe"]

	def __check_login(self, login: str, password: str) -> int:
		try:
			user_id = self.__db_connector.db_request_data(
				f"SELECT id FROM user "
				f"WHERE login=\"{login}\" AND password_hash=\"{hashlib.md5(password.encode()).hexdigest()}\"")[0][0]
			return user_id
		except Error:
			# No DB connection
			return -1
		except IndexError:
			return -1

	def __button_logic_login_confirmation(self):
		login_id = self.__check_login(
			self.__ui_elements["login_entry"].get(),
			self.__ui_elements["password_entry"].get())
		if login_id != -1:
			if "process" not in self.__notebook_pages:
				self.__init_process_tab()
				self.__init_recipe_tab()
				self.__ui_elements["login_confirmation_button"].configure(state="disabled")
				self.__ui_elements["login_entry"].configure(state="disabled")
				self.__ui_elements["password_entry"].configure(state="disabled")
				self.__ui_elements["login_error_label"].configure(text="")
				self.__ui_elements["logout_button"].configure(state="normal")
		else:
			self.__ui_elements["login_error_label"].configure(text="incorrect login or password")

	def __button_logic_logout_button(self):
		self.__ui_elements["login_confirmation_button"].configure(state="normal")
		self.__ui_elements["login_entry"].configure(state="normal")
		self.__ui_elements["password_entry"].configure(state="normal")
		self.__ui_elements["logout_button"].configure(state="disabled")
		self.__destroy_secured_tabs()

	def start_ui(self):
		self.__main_window.mainloop()
