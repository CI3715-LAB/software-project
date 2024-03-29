from user.model import User, Role, Permission
from log.model import Type, Module
from department.model import Department
from project.model import Project
from vehicle.model import VehicleBrand, VehicleModel, VehicleColor, Vehicle
from client.model import Client
from datetime import datetime
from time import sleep

USER_LOGIN_DATA = {
	'id': 1,
	'username': 'admin',
	'password': 'admin',
	'admin': True
}

TEST_USER_DATA = {
	'valid': {
		'test1': User(USER_LOGIN_DATA['username'], USER_LOGIN_DATA['password'], 'admin', 'admin', 1, 0, 0),
		'test2': User('gerente', 'admin', 'gerente', 'gerente', 3, 0, 0),
	},
	'invalidPassword': {
		"username": "admin",
		"password": "invalid_password"
	},
	'invalidUsername': {
		"username": "invalid_username",
		"password": "test"
	},
	'register': {
		"username": "testUser3",
		"password": "test",
		"name": "testName3",
		"lastname": "testLastname3",
		"role": "admin",
		"department": "Undefined",
		"project": "Proyecto 1"
	},
	'delete': {
		"id": 6,
		"username": "juan",
	},
}

FIXED_TABLES = {
	'module': [
		'Usuarios', 'Proyectos',
		'Clientes', 'Vehiculos', 'Departamentos'
	],
	'type': [
		'Agregar', 'Buscar', 'Modificar', 'Eliminar'
	],
	'role': [
		'admin', 'test role1', 'test role2'
	],
	'vehicleBrand': {
		'Toyota': ['Yaris', 'Prado'],
		'Chevrolet': ['Cruze', 'Aveo'],
		'Chery': ['Tiggo', 'Arauca'],
		'Ford': ['Bronco', 'Fiesta']
	},
	'vehicleColor': [
		'Azul', 'Rojo', 'Verde', 'Naranja', 'Plata', 'Negro',
		'Blanco', 'Amarillo', 'Gris'
	]
}

TEST_TABLES = {
	'vehicle': [
		('1234567', 1, 1, '2007', '123456781', '987654329', 1, 'Mantenimiento', 1),
		('1234568', 1, 2, '2007', '123456782', '987654328', 2, 'Cambio cauchos', 1),
		('1234569', 2, 3, '2007', '123456783', '987654327', 3, 'Alineación', 2),
		('1234560', 2, 4, '2007', '123456784', '987654326', 4, 'Aire acondicionado', 2),
		('1234561', 3, 5, '2007', '123456785', '987654325', 5, 'Cambio cauchos', 3),
		('1234562', 3, 6, '2007', '123456786', '987654324', 6, 'Alineación', 3),
		('1234563', 4, 7, '2007', '123456787', '987654323', 7, 'Aire acondicionado', 4),
		('1234564', 4, 8, '2007', '123456788', '987654322', 9, 'Mantenimiento', 4),
	],
	'department': [
		'Undefined',
		'Undefined 2',
	],
	'client': [
		('12345678', 'testNameClient1', 'testLastNameClient1', '2020-01-11', '11111111111', 'example1@example.com', 'dir1'),
		('23456789', 'testNameClient2', 'testLastNameClient2', '2020-02-12', '22222222222', 'example2@example.com', 'dir2'),
		('34567890', 'testNameClient3', 'testLastNameClient3', '2020-03-13', '33333333333', 'example3@example.com', 'dir3'),
		('45678901', 'testNameClient4', 'testLastNameClient4', '2020-04-14', '44444444444', 'example4@example.com', 'dir4'),
	],
	'project': [
		('Proyecto 1', '2023-01-01', '2023-12-31', 1, 2, 2, 'Limpieza de inyectores', 10.15, 'Modelo 16344'),
		('Proyecto 2', '2023-01-02', '2023-12-31', 1, 3, 3, 'Alineación y balanceo', 25.00, ''),
		('Proyecto 3', '2023-01-03', '2023-12-31', 0, 4, 4, 'Cambio de correa de tiempos', 20.00, 'Modelo 1314'),
		('Proyecto 4', '2023-01-04', '2023-12-31', 0, 5, 5, 'Cambio de pila de bomba de gasolina', 12.24, 'Modelo R2D2'),
	]
}


def init_database(self, db):
	self.test_user_data = TEST_USER_DATA
	# MODULE
	undefined_module = Module('Undefined')
	undefined_module.id = 0
	db.session.add(undefined_module)
	for name in FIXED_TABLES['module']:
		db.session.add(Module(name))
		
	# TYPE
	for name in FIXED_TABLES['type']:
		db.session.add(Type(name))

	# ROLE
	for name in FIXED_TABLES['role']:
		db.session.add(Role(name))

	# CLIENT
	for client in TEST_TABLES['client']:
		client_data = list(client)
		client_data[3] = datetime.fromisoformat(client_data[3])
		db.session.add(Client(*client_data))

	# VEHICLE BRAND AND MODEL
	brand_id = 0
	for brand in FIXED_TABLES['vehicleBrand']:
		vehicleBrand = VehicleBrand(brand)
		db.session.add(vehicleBrand)
		brand_id += 1
		for model in FIXED_TABLES['vehicleBrand'][brand]:
			db.session.add(VehicleModel(model, brand_id))

	# VEHICLE COLOR
	for color in FIXED_TABLES['vehicleColor']:
		db.session.add(VehicleColor(color))

	# VEHICLE
	for vehicle in TEST_TABLES['vehicle']:
		db.session.add(Vehicle(*vehicle))

	# DEPARTMENT
	undefined_department = Department('Undefined')
	undefined_department.id = 0
	db.session.add(undefined_department)
	for department in TEST_TABLES['department']:
		db.session.add(Department(department))

	# PROJECT
	data_undef_proj = ('Undefined', datetime.fromisoformat('2023-01-01'), datetime.fromisoformat('2023-12-31'), 0, 1, 1, 'Undefined ', 33.25, 'Aceite 15-40')
	undefined_project = Project(*data_undef_proj)
	undefined_project.id = 0
	db.session.add(undefined_project)
	for project in TEST_TABLES['project']:
		project_data = list(project)
		project_data[1] = datetime.fromisoformat(project_data[1])
		project_data[2] = datetime.fromisoformat(project_data[2])
		db.session.add(Project(*project_data))

	# USER
	for user in TEST_USER_DATA['valid'].values():
		db.session.add(user)

	db.session.commit()