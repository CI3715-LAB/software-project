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

    return render_template('/material/material_list.html',
        materials=materials, loggedIn= 'user' in session,
        user=session.get('user')
    )

@unit_blueprint.route('/')
@login_required
def retrieve_units():
    units = Unit.query.all()

    return render_template('/material/unit_list.html',
        units=units, loggedIn= 'user' in session,
        user=session.get('user')
    )

@category_blueprint.route('/')
@login_required
def retrieve_categories():
    categories = Category.query.all()

    return render_template('/material/category_list.html',
        categories=categories, loggedIn= 'user' in session,
        user=session.get('user')
    )