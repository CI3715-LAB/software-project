from flask import Blueprint, request, render_template, redirect, url_for, session
from sqlalchemy import or_
from datetime import datetime
from config.setup import db, logger
from log.utils import LogType, LogModule
from werkzeug.exceptions import BadRequest
from user.utils import login_required
from material.model import Material, Unit, Category

material_blueprint = Blueprint('material', __name__)
unit_blueprint = Blueprint('unit', __name__)
category_blueprint = Blueprint('category', __name__)


@material_blueprint.route('/')
@login_required
def retrieve_materials():
    materials = Material.query.filter(Material.id != 0).all()
    units = Unit.query.filter(Unit.id != 0).all()
    categories = Category.query.filter(Category.id != 0).all()

    return render_template('/material/material_list.html',
        loggedIn= 'user' in session,
        materials=materials,
        units=units,
        categories=categories,
        user=session.get('user')
    )

@unit_blueprint.route('/')
@login_required
def retrieve_units():
    units = Unit.query.filter(Unit.id != 0).all()

    return render_template('/material/unit_list.html',
        units=units, loggedIn= 'user' in session,
        user=session.get('user')
    )

@category_blueprint.route('/')
@login_required
def retrieve_categories():
    categories = Category.query.filter(Category.id != 0).all()

    return render_template('/material/category_list.html',
        categories=categories, loggedIn= 'user' in session,
        user=session.get('user')
    )

@material_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add_material():
    materials = Material.query.filter(Material.id != 0).all()
    units = Unit.query.filter(Unit.id != 0).all()
    categories = Category.query.filter(Category.id != 0).all()

    if request.method == 'GET':
        return render_template('/material/material_add.html',
            loggedIn= 'user' in session, 
            materials=materials,
            units=units,
            categories=categories,
            user=session.get('user')
        )

    if request.method == 'POST':
        if not 'user' in session or not session['user']['admin']:
            return render_template('/material/material_add.html',
                error="No tienes los permisos necesarios para crear materiales",
                loggedIn= 'user' in session, 
                materials=materials,
                units=units,
                categories=categories,
                user=session.get('user')
            )

        description = request.form.get('description', None)
        cost = request.form.get('cost', None)
        unit_id = request.form.get('unit', None)
        category_id = request.form.get('category', None)

        material = Material.query.filter(Material.description == description).filter(Material.cost == cost).filter(Material.unit_id == unit_id).filter(Material.category_id == category_id).first()
        if material:
            return render_template('/material/material_add.html',
                error="Material ya existente",
                loggedIn= 'user' in session, 
                materials=materials,
                units=units,
                categories=categories,
                user=session.get('user')
            )

        material = Material(description, cost, unit_id, category_id)
        db.session.add(material)
        db.session.commit()

        description = f"Creación de material \"{material.description}\""
        logger.catch(session['user']['username'], LogType.ADD.value, LogModule.MATERIALS.value, description)

        return redirect(url_for('material.retrieve_materials'))

@unit_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add_unit():
    units = Unit.query.filter(Unit.id != 0).all()

    if request.method == 'GET':
        return render_template('/material/unit_add.html',
            loggedIn= 'user' in session, 
            units=units,
            user=session.get('user')
        )

    if request.method == 'POST':
        if not 'user' in session or not session['user']['admin']:
            return render_template('/material/unit_add.html',
                error="No tienes los permisos necesarios para crear unidades",
                loggedIn= 'user' in session, 
                units=units,
                user=session.get('user')
            )

        name = request.form.get('name', None)
        unit = Unit.query.filter_by(name=name).first()
        if unit:
            return render_template('/material/unit_add.html',
                error="Unidad ya existente",
                loggedIn= 'user' in session
            )

        unit = Unit(name)
        db.session.add(unit)
        db.session.commit()

        description = f"Creación de unidad \"{unit.name}\""
        logger.catch(session['user']['username'], LogType.ADD.value, LogModule.UNITS.value, description)

        return redirect(url_for('unit.retrieve_units'))

@category_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add_category():
    categories = Category.query.filter(Category.id != 0).all()

    if request.method == 'GET':
        return render_template('/material/category_add.html',
            loggedIn= 'user' in session, 
            categories=categories,
            user=session.get('user')
        )

    if request.method == 'POST':
        if not 'user' in session or not session['user']['admin']:
            return render_template('/material/category_add.html',
                error="No tienes los permisos necesarios para crear categorías",
                loggedIn= 'user' in session, 
                categories=categories,
                user=session.get('user')
            )

        name = request.form.get('name', None)
        category = Category.query.filter_by(name=name).first()
        if category:
            return render_template('/material/category_add.html',
                error="Categoría ya existente",
                loggedIn= 'user' in session
            )

        category = Category(name)
        db.session.add(category)
        db.session.commit()

        description = f"Creación de categoría \"{category.name}\""
        logger.catch(session['user']['username'], LogType.ADD.value, LogModule.CATEGORIES.value, description)

        return redirect(url_for('category.retrieve_categories'))

@material_blueprint.route('/update', methods=['POST'])
@login_required
def update_material():
    materials = Material.query.filter(Material.id != 0).all()
    units = Unit.query.filter(Unit.id != 0).all()
    categories = Category.query.filter(Category.id != 0).all()

    if not 'user' in session or not session['user']['admin']:
        return render_template('/material/material_list.html',
            error="No tienes los permisos necesarios para modificar materiales",
            loggedIn= 'user' in session, 
            materials=materials,
            units=units,
            categories=categories,
            user=session.get('user')
        )

    id = request.form.get('id', None)
    description = request.form.get('description', None)
    cost = request.form.get('cost', None)
    unit_id = request.form.get('unit', None)
    category_id = request.form.get('category', None)

    material = Material.query.filter(Material.id == id).first()
    if material == None:
        error = "El material suministrado no existe en la base de datos"
        return redirect('/material')

    if description != None: material.description = description
    if cost != None: material.cost = cost    
    if unit_id != None: material.unit_id = unit_id
    if category_id != None: material.category_id = category_id

    db.session.commit()

    description = f"Modificación de material \"{material.description}\""
    logger.catch(session['user']['username'], LogType.MODIFY.value, LogModule.MATERIALS.value, description)

    return redirect(url_for('material.retrieve_materials'))

@unit_blueprint.route('/update', methods=['POST'])
@login_required
def update_unit():
    units = Unit.query.filter(Unit.id != 0).all()

    if not 'user' in session or not session['user']['admin']:
        return render_template('/material/unit_list.html',
            error="No tienes los permisos necesarios para modificar unidades",
            loggedIn= 'user' in session,
            units=units,
            user=session.get('user')
        )

    id = request.form.get('id', None)
    name = request.form.get('name', None)

    unit = Unit.query.filter(Unit.id == id).first()
    if unit == None:
        error = "La unidad suministrada no existe en la base de datos"
        return redirect('/unit')

    if name != None: unit.name = name

    db.session.commit()

    description = f"Modificación de unidad \"{unit.name}\""
    logger.catch(session['user']['username'], LogType.MODIFY.value, LogModule.UNITS.value, description)

    return redirect(url_for('unit.retrieve_units'))

@category_blueprint.route('/update', methods=['POST'])
@login_required
def update_category():
    categories = Category.query.filter(Category.id != 0).all()

    if not 'user' in session or not session['user']['admin']:
        return render_template('/material/category_list.html',
            error="No tienes los permisos necesarios para modificar categorías",
            loggedIn= 'user' in session,
            categories=categories,
            user=session.get('user')
        )

    id = request.form.get('id', None)
    name = request.form.get('name', None)

    category = Category.query.filter(Category.id == id).first()
    if category == None:
        error = "La categoría suministrada no existe en la base de datos"
        return redirect('/category')

    if name != None: category.name = name

    db.session.commit()

    description = f"Modificación de categoría \"{category.name}\""
    logger.catch(session['user']['username'], LogType.MODIFY.value, LogModule.CATEGORIES.value, description)
    
    return redirect(url_for('category.retrieve_categories'))

@material_blueprint.route('/delete', methods=['POST'])
@login_required
def delete_material():
    id = request.form['id']

    material = Material.query.filter(Material.id == id).first()
    if material == None:
        error = "El material suministrado no existe en la base de datos"
        return redirect('/material')

    # Salvar actions que referencias materiales

    db.session.delete(material)
    db.session.commit()

    description = f"Eliminación de material \"{material.description}\""
    logger.catch(session['user']['username'], LogType.DELETE.value, LogModule.MATERIALS.value, description)

    return redirect(url_for('material.retrieve_materials'))

@unit_blueprint.route('/delete', methods=['POST'])
@login_required
def delete_unit():
    id = request.form['id']

    unit = Unit.query.filter(Unit.id == id).first()
    if unit == None:
        error = "La unidad suministrada no existe en la base de datos"
        return redirect('/unit')

    materials = Material.query.filter(Material.unit_id == id).all()
    for material in materials:
        material.unit_id = 0
        material.unit = Unit.query.filter_by(id = 0).first()

    db.session.delete(unit)
    db.session.commit()

    description = f"Eliminación de unidad \"{unit.name}\""
    logger.catch(session['user']['username'], LogType.DELETE.value, LogModule.UNITS.value, description)

    return redirect(url_for('unit.retrieve_units'))

@category_blueprint.route('/delete', methods=['POST'])
@login_required
def delete_category():
    id = request.form['id']

    category = Category.query.filter(Category.id == id).first()
    if category == None:
        error = "La categoría suministrada no existe en la base de datos"
        return redirect('/category')

    materials = Material.query.filter(Material.category_id == id).all()
    for material in materials:
        material.category_id = 0
        material.category = Category.query.filter_by(id = 0).first()

    db.session.delete(category)
    db.session.commit()

    description = f"Eliminación de categoría \"{category.name}\""
    logger.catch(session['user']['username'], LogType.DELETE.value, LogModule.CATEGORIES.value, description)

    return redirect(url_for('category.retrieve_categories'))

@material_blueprint.route('/search', methods=['GET'])
@login_required
def search_material():
    phrase = request.args.get('phrase', None)

    if phrase == None:
        return redirect(url_for('materials.retrieve_materials'))

    materials = db.session.query(Material).select_from(Material).join(Unit).join(Category).join(Project).join(User).filter(
        or_(
            Material.description.like('%' + phrase + '%'),
            Material.cost.like('%' + phrase + '%'),
            Unit.name.like('%' + phrase + '%'),
            Category.name.like('%' + phrase + '%')
        )
    ).filter(Material.id != 0)

    description = f"BÚSQUEDA DE MATERIALES: \"{phrase}\""
    logger.catch(session['user']['username'], LogType.SEARCH.value, LogModule.MATERIALS.value, description)

    return render_template('/material/material_list.html', materials=materials, phrase=phrase)

@unit_blueprint.route('/search', methods=['GET'])
@login_required
def search_unit():
    phrase = request.args.get('phrase', None)

    if phrase == None:
        return redirect(url_for('units.retrieve_units'))

    units = db.session.query(Unit).filter(
        or_(
            Unit.name.like('%' + phrase + '%')
        )
    ).filter(Unit.id != 0)

    description = f"BÚSQUEDA DE UNIDADES: \"{phrase}\""
    logger.catch(session['user']['username'], LogType.SEARCH.value, LogModule.UNITS.value, description)

    return render_template('/material/unit_list.html', units=units, phrase=phrase)

@category_blueprint.route('/search', methods=['GET'])
@login_required
def search_category():
    phrase = request.args.get('phrase', None)

    if phrase == None:
        return redirect(url_for('category.retrieve_categories'))

    categories = db.session.query(Category).filter(
        or_(
            Category.name.like('%' + phrase + '%')
        )
    ).filter(Category.id != 0)

    description = f"BÚSQUEDA DE CATEGORÍAS: \"{phrase}\""
    logger.catch(session['user']['username'], LogType.SEARCH.value, LogModule.CATEGORIES.value, description)

    return render_template('/material/category_list.html', categories=categories, phrase=phrase)