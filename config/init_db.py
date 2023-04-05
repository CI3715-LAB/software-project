from config.setup import db

from user.model import Role, Permission

#db.drop_all()
#db.create_all()

def init_roles_permissions():
    admin_role = Role.query.filter_by(name = 'admin').first()

    p1 = Permission.query.filter_by(id = 1).first()
    p2 = Permission.query.filter_by(id = 2).first()
    p3 = Permission.query.filter_by(id = 3).first()
    p4 = Permission.query.filter_by(id = 4).first()
    p5 = Permission.query.filter_by(id = 5).first()
    p6 = Permission.query.filter_by(id = 6).first()
    p7 = Permission.query.filter_by(id = 7).first()
    p8 = Permission.query.filter_by(id = 8).first()
    p9 = Permission.query.filter_by(id = 9).first()
    p10 = Permission.query.filter_by(id = 10).first()
    p11 = Permission.query.filter_by(id = 11).first()
    p12 = Permission.query.filter_by(id = 12).first()
    p13 = Permission.query.filter_by(id = 13).first()
    p14 = Permission.query.filter_by(id = 14).first()
    p15 = Permission.query.filter_by(id = 15).first()

    admin_role.permissions.append(p1)
    admin_role.permissions.append(p2)
    admin_role.permissions.append(p3)
    admin_role.permissions.append(p4)
    admin_role.permissions.append(p5)
    admin_role.permissions.append(p6)
    admin_role.permissions.append(p7)
    admin_role.permissions.append(p8)
    admin_role.permissions.append(p9)
    admin_role.permissions.append(p10)
    admin_role.permissions.append(p11)
    admin_role.permissions.append(p12)
    admin_role.permissions.append(p13)
    admin_role.permissions.append(p14)
    admin_role.permissions.append(p15)

    db.session.commit()