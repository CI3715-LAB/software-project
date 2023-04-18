from flask import Blueprint, request, render_template, redirect, url_for, session
from sqlalchemy import or_
from datetime import datetime
from config.setup import db, logger
from log.utils import LogType, LogModule
from .model import Project
from user.model import User, Role
from werkzeug.exceptions import BadRequest

from user.utils import login_required
from vehicle.model import Vehicle
from department.model import Department

project_blueprint = Blueprint('project', __name__)

@project_blueprint.route('/')
@login_required
def retrieve_projects():
    # return all projects with an id different than 0
    projects = Project.query.filter(Project.id != 0).all()
    departments = Department.query.all()

    return render_template('/project/project_list.html',
        projects=projects, loggedIn= 'user' in session,
        departments=departments,
        user=session.get('user')
    )
    
@project_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add_project():
    today = datetime.today().strftime('%Y-%m-%d') # get today's date
    vehicles = Vehicle.query.all()
    departments = Department.query.all()
    manager_role = Role.query.filter_by(name = 'gerente de proyectos').first()
    managers = User.query.filter_by(role_id =  manager_role.id)

    if request.method == 'GET':

        return render_template('/project/project_add.html',
            today=today, loggedIn= 'user' in session, 
            vehicles=vehicles,
            managers=managers,
            departments=departments,
            user=session.get('user')                       
        )

    if request.method == 'POST':
        if not 'user' in session or not session['user']['admin']:
            return render_template('/project/project_add.html',
                error="No tienes los permisos necesarios para crear proyectos",
                today=today, loggedIn= 'user' in session, 
                vehicles=vehicles,
                managers=managers,
                departments=departments,
                user=session.get('user')              
            )

        # get description, open date and close date
        description = request.form['description']
        open_date = request.form['open_date']
        close_date = request.form['close_date']
        enabled = request.form.get('enabled', False, bool)
        vehicle = request.form['vehicle']
        department = request.form['department']
        manager = request.form['manager']
        # problem =  request.form['problem']
        # solution = request.form['solution']
        # amount = request.form['amount']
        # observation = request.form['observation']

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
        project = Project(description, open_date, close_date, enabled, vehicle, department, None, None, None, None)
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

    id = request.form.get('id', None)
    description = request.form.get('description', None)
    open_date = request.form.get('open_date', None)
    close_date = request.form.get('close_date', None)
    enabled = request.form.get('enabled', None, bool)
    vehicle = request.form.get('vehicle', None)
    department = request.form.get('department', None)
    manager = request.form.get('manager', None)
    problem =  request.form.get('problem', None)
    solution = request.form.get('solution', None)
    amount = request.form.get('amount', None)
    observation = request.form.get('observation', None)

    # Project exists
    project = Project.query.filter_by(id = id).first()
    if project == None:
        error = "El proyecto suministrado no existe en la base de datos"
        return redirect('/project')

    if open_date != None:
        # turn open date and close date into datetime objects
        open_date = datetime.strptime(open_date, '%Y-%m-%d')
        close_date = datetime.strptime(close_date, '%Y-%m-%d')

        # make sure open date is before close date
        if open_date > close_date:
            return render_template('/project/project_list.html',
                error="Open date must be before close date",
                user=session.get('user')
            )

    # update project
    if description != None: project.description = description
    if open_date != None: project.open_date = open_date
    if close_date != None: project.close_date = close_date
    if enabled != None: project.enabled = enabled
    if vehicle != None: project.vehicle_id = vehicle
    if department != None: project.department_id = department
    if problem != None: project.problem = problem
    if solution != None: project.solution = solution
    if amount != None: project.amount = amount
    if observation != None: project.observation = observation

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
    project = db.session.get(Project, id)
    if project:
        for user in project.users:
            user.project_id = 0
            user.project = Project.query.filter_by(id = 0).first()
            db.session.commit()
        db.session.delete(project)
        db.session.commit()

    description = f"Eliminado proyecto \"{project.description}\""
    logger.catch(session['user']['username'], LogType.DELETE.value, LogModule.PROJECTS.value, description)

    return redirect(url_for('project.retrieve_projects'))

@project_blueprint.route('/search', methods=['GET'])
@login_required
def search_project():
    phrase = request.args.get('phrase')

    if not phrase:
        return redirect(url_for('project.retrieve_projects'))

    projects = db.session.query(Project).select_from(Project).join(User).filter(
        or_(
            Project.id.like('%' + phrase + '%'),
            Project.description.like('%' + phrase + '%'),
            Project.open_date.like('%' + phrase + '%'),
            Project.close_date.like('%' + phrase + '%'),
            User.name.like('%' + phrase + '%'),
            User.username.like('%' + phrase + '%'),
        )
    ).filter(id != 0)

    description = f"Busqueda de proyectos por frase \"{phrase}\""
    logger.catch(session['user']['username'], LogType.SEARCH.value, LogModule.PROJECTS.value, description)

    return render_template('/project/project_list.html', projects=projects, phrase=phrase)