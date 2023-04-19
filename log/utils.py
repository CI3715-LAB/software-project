from enum import Enum
from datetime import datetime

from config.setup import db
from log.model import Log, Type, Module
from user.model import User

class Logger():
    # Type = Agregar, Eliminar, ...
    # Module = Usuario, Proyecto, ...

    def catch(self, username, type_name, module_name, description):
        user = User.query.filter_by(username = username).first()
        type = Type.query.filter_by(name = type_name).first()
        module = Module.query.filter_by(name = module_name).first()

        print("----------------------------------------------------------------------")
        print(user, type, module)
        if user and type and module:
            log = Log(user.id, description, type.id, module.id, datetime.utcnow().strftime("%H:%M:%S"))
            db.session.add(log)
            db.session.commit()

class LogType(Enum):
    ADD = "Agregar"
    SEARCH = "Buscar"   
    MODIFY = "Modificar"
    DELETE = "Eliminar"

class LogModule(Enum):
    USERS = "Usuarios"
    PROJECTS = "Proyectos"
    CLIENTS = "Clientes"
    VEHICLES = "Vehículos"
    DEPARTMENTS = "Departamentos"
    MATERIALS = "Materiales"
    UNITS = "Unidades"
    CATEGORIES = "Categorías"