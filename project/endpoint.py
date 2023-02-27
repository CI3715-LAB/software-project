from flask import Blueprint, request, render_template, redirect, url_for, session
from sqlalchemy import or_, select
from datetime import datetime
from config.setup import db, logger
from log.utils import LogType, LogModule
from .model import Project
from user.model import User
from werkzeug.exceptions import BadRequest

from user.utils import login_required

project_blueprint = Blueprint('project', __name__)

@project_blueprint.route('/')
@login_required
def retrieve_projects():
    # return all projects with an id different than 0
    projects = Project.query.filter(Project.id != 0).all()

    # description = "Busqueda de proyectos"
    # logger.catch(session['user']['username'], LogType.SEARCH.value, LogModule.PROJECTS.value, description)

    return render_template('/project/project_list.html',
        projects=projects, loggedIn= 'user' in session,
        user=session.get('user')
    )
    

@project_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add_project():
    # get today's date
    today = datetime.today().strftime('%Y-%m-%d')
    
    if request.method == 'GET':
        return render_template('/project/project_add.html',
            today=today, loggedIn= 'user' in session,
            user=session.get('user')                       
        )

    if request.method == 'POST':
        # get description, open date and close date
        description = request.form['description']
        open_date = request.form['open_date']
        close_date = request.form['close_date']
        enabled = request.form.get('enabled', False, bool)

        # turn open date and close date into datetime objects
        open_date = datetime.strptime(open_date, '%Y-%m-%d')
        close_date = datetime.strptime(close_date, '%Y-%m-%d')

        # make sure open date is before close date
        if open_date > close_date:
            return render_template('/project/project_add.html',
                error="Open date must be before close date",
                description=description, open_date=request.form['open_date'],
                close_date=request.form['close_date'], enabled=enabled,
                loggedIn= 'user' in session,
                user=session.get('user')
            )

        # create a new project
        project = Project(description, open_date, close_date, enabled)
        db.session.add(project)
        db.session.commit()

        description = f"Creación de proyecto \"{project.description}\""
        logger.catch(session['user']['username'], LogType.ADD.value, LogModule.PROJECTS.value, description)

        return redirect(url_for('project.retrieve_projects'))
    
# update project
@project_blueprint.route('/update', methods=['POST'])
@login_required
def update_project():
    # get description, open date and close date
    id = request.form['id']
    description = request.form['description']
    open_date = request.form['open_date']
    close_date = request.form['close_date']
    enabled = request.form.get('enabled', False, bool)

    # turn open date and close date into datetime objects
    open_date = datetime.strptime(open_date, '%Y-%m-%d')
    close_date = datetime.strptime(close_date, '%Y-%m-%d')

    # Project exists
    project = Project.query.filter_by(id = id).first()
    if project == None:
        error = "El proyecto suministrado no existe en la base de datos"
        return redirect('/project')

    # make sure open date is before close date
    if open_date > close_date:
        return render_template('/project/project_list.html',
            error="Open date must be before close date",
            user=session.get('user')
        )

    # update project
    project.description = description
    project.open_date = open_date
    project.close_date = close_date
    project.enabled = enabled
    db.session.commit()

    description = f"Modificación de proyecto \"{project.description}\""
    logger.catch(session['user']['username'], LogType.MODIFY.value, LogModule.PROJECTS.value, description)

    return redirect(url_for('project.retrieve_projects'))
    
# enable/disable project
@project_blueprint.route('/toggle', methods=['POST'])
@login_required
def enable_project():
    id = request.form['id']

    # Project exists
    project = Project.query.filter_by(id = id).first()
    if project:
        project.enabled = not project.enabled
        db.session.commit()

    description = f"Actualización de estado de proyecto \"{project.description}\""
    logger.catch(session['user']['username'], LogType.MODIFY.value, LogModule.PROJECTS.value, description)

    return redirect(url_for('project.retrieve_projects'))

# delete project
@project_blueprint.route('/delete', methods=['POST'])
@login_required
def delete_project():
    id = request.form['id']

    if id == '0':
        raise BadRequest("Undefined project cannot be deleted")

    # Project exists
    project = Project.query.filter_by(id = id).first()
    if project:
        for user in project.users:
            user.project_id = 0
            user.project = Project.query.get(0)
            db.session.commit()
        db.session.delete(project)
        db.session.commit()

    description = f"Eliminado de proyecto \"{project.description}\""
    logger.catch(session['user']['username'], LogType.DELETE.value, LogModule.PROJECTS.value, description)

    return redirect(url_for('project.retrieve_projects'))

@project_blueprint.route('/search', methods=['GET'])
@login_required
def search_project():
    phrase = request.args.get('phrase')
    projects = db.session.query(Project).select_from(Project).join(User).filter(
        or_(
            Project.id.like('%' + phrase + '%'),
            Project.description.like('%' + phrase + '%'),
            Project.open_date.like('%' + phrase + '%'),
            Project.close_date.like('%' + phrase + '%'),
            User.name.like('%' + phrase + '%')
        )
    ).filter(id != 0)

    description = f"Busqueda de proyectos por frase \"{phrase}\""
    logger.catch(session['user']['username'], LogType.SEARCH.value, LogModule.PROJECTS.value, description)

    return render_template('/project/project_list.html', projects=projects, phrase=phrase)