from project.model import Project
from user.model import User, Role
from log.model import Module, Type

def init_database(db):
	db.session.commit()
	db.drop_all()
	db.create_all()
	project_undefined = Project('Undefined', datetime.fromisoformat('2023-01-01'), datetime.fromisoformat('2023-01-01'), True)
	project_undefined.id = 0;
	db.session.add(project_undefined)
	db.session.add(Project('Test Project', datetime.fromisoformat('2023-01-01'), datetime.fromisoformat('2023-01-01'), True))
	db.session.add(Role('admin'))
	db.session.add(User('testUser', 'test', 'testName', 'testLastName', 1, 1))
	db.session.add(User('testUser2', 'test', 'testName2', 'testLastName2', 1, 1))
	db.session.add(Type('Usuarios'))
	db.session.add(Type('Proyectos'))
	db.session.add(Type('Vehiculos'))
	db.session.add(Type('Clientes'))
	db.session.add(Module('Agregar'))
	db.session.add(Module('Buscar'))
	db.session.add(Module('Modificar'))
	db.session.add(Module('Eliminar'))
	db.session.commit()