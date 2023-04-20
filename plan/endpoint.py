from flask import Blueprint, request, render_template, redirect, url_for, session
from sqlalchemy import or_
from datetime import datetime
from config.setup import db, logger
from log.utils import LogType, LogModule
from werkzeug.exceptions import BadRequest
from user.utils import login_required
from user.model import User
from project.model import Project
from plan.model import Plan, Action, Activity
from material.model import Material

activity_blueprint = Blueprint('activity', __name__)
action_blueprint = Blueprint('action', __name__)
plan_blueprint = Blueprint('plan', __name__)

@action_blueprint.route('/<int:id>', methods=['GET'])
@login_required
def retrieve_actions(id):
    actions = Action.query.filter(Action.id != 0).join(Plan).filter(Plan.project_id == id).all()
    plans = Plan.query.filter(Plan.id != 0).all()

    return render_template('plan/action_list.html',
        loggedIn= 'user' in session,
        actions=actions,
        plans=plans,
        id=id,
        user=session.get('user')
    )

@activity_blueprint.route('/<int:id>', methods=['GET'])
@login_required
def retrieve_activities(id):
    activities = Activity.query.filter(Activity.id != 0).join(Action).filter(Activity.action_id == id).join(Plan).filter(Plan.project_id == id).all()
    actions = Action.query.filter(Action.id != 0).join(Plan).filter(Plan.project_id == id).all()

    return render_template('plan/activity_list.html',
        loggedIn= 'user' in session,
        activities=activities,
        actions=actions,
        id=id,
        user=session.get('user')
    )

@plan_blueprint.route('/<int:id>', methods=['GET'])
@login_required
def retrieve_plans(id):
    actions = Action.query.filter(Action.id != 0).join(Plan).filter(Plan.project_id == id).all()
    activities = Activity.query.join(Action).filter(Action.id != 0).filter(Activity.action_id == Action.id).all()
    plans = Plan.query.filter(Plan.id != 0).filter(Plan.project_id == id).all()
    users = User.query.filter(User.id != 0).all()
    project = Project.query.filter_by(id = id).first()
    materials = Material.query.filter(Material.id != 0).all()

    amount = 0
    for plan in plans:
        amount += plan.amount

    return render_template('plan/plan_list.html',
        loggedIn= 'user' in session,
        plans=plans,
        users=users,
        actions=actions,
        activities=activities,
        project=project,
        materials=materials,
        amount=amount,
        user=session.get('user')
    )

@plan_blueprint.route('/human/<int:id>', methods=['GET'])
@login_required
def retrieve_human_plans(id):
    actions = Action.query.filter(Action.id != 0).all()
    activities = Activity.query.filter(Activity.id != 0).all()
    plans = Plan.query.filter(Plan.id != 0).filter(Plan.id == id).all()
    project = Project.query.join(Plan).filter(Plan.id == id).first()
    users = User.query.filter(User.id != 0).all()

    personnel_amount = 0
    for plan in plans:
        personnel_amount += plan.personnel_amount

    return render_template('plan/plan_human_list.html',
        loggedIn= 'user' in session,
        plans=plans,
        project=project,
        users=users,
        actions=actions,
        activities=activities,
        amount=personnel_amount,
        user=session.get('user')
    )

@plan_blueprint.route('/material/<int:id>', methods=['GET'])
@login_required
def retrieve_material_plans(id):
    actions = Action.query.filter(Action.id != 0).all()
    activities = Activity.query.filter(Activity.id != 0).all()
    plans = Plan.query.filter(Plan.id != 0).filter(Plan.id == id).all()
    project = Project.query.join(Plan).filter(Plan.id == id).first()
    users = User.query.filter(User.id != 0).all()

    material_amount = 0
    for plan in plans:
        material_amount += plan.material_amount

    return render_template('plan/plan_material_list.html',
        loggedIn= 'user' in session,
        plans=plans,
        project=project,
        users=users,
        actions=actions,
        activities=activities,
        amount=material_amount,
        user=session.get('user')
    )

@action_blueprint.route('/add/<int:id>', methods=['GET','POST'])
@login_required
def add_action(id):
    plans = Plan.query.filter(Plan.id != 0).all()

    if request.method == 'GET':
        return render_template('plan/action_add.html',
            loggedIn= 'user' in session,
            plans=plans,
            actions=actions,
            id=id,
            user=session.get('user')
        )
    elif request.method == 'POST':
        name = request.form.get('name', None)

        action  = Action.query.filter(Action.name == name).first()
        if action != None:
            return render_template('/plan/action_add.html',
                error="Acción ya existente",
                loggedIn= 'user' in session, 
                plans=plans,
                id=id,
                user=session.get('user')
            )

        plan = Plan.query.filter_by(project_id = id).first()
        action = Action(name, plan.id)
        db.session.add(action)
        db.session.commit()

        description = f"Creación de acción \"{action.name}\""
        logger.catch(session['user']['username'], LogType.ADD.value, LogModule.ACTIONS.value, description)

        return redirect(url_for('action.retrieve_actions', id=id))

@activity_blueprint.route('/add/<int:id>', methods=['GET','POST'])
@login_required
def add_activity(id):
    actions = Action.query.filter(Action.id != 0).join(Plan).filter(Plan.project_id == id).all()

    if request.method == 'GET':
        return render_template('plan/activity_add.html',
            loggedIn= 'user' in session,
            actions=actions,
            id=id,
            user=session.get('user')
        )
    elif request.method == 'POST':
        name = request.form.get('name', None)
        action_id = request.form.get('action', None)
        activity = Activity.query.filter(Activity.name == name).filter(Activity.action_id == action_id).first()

        if activity != None:
            return render_template('/plan/activity_add.html',
                error="Actividad ya existente",
                loggedIn= 'user' in session, 
                actions=actions,
                id=id,
                user=session.get('user')
            )

        activity = Activity(name, action_id)
        db.session.add(activity)
        db.session.commit()

        description = f"Creación de actividad \"{name}\""
        logger.catch(session['user']['username'], LogType.ADD.value, LogModule.ACTIVITIES.value, description)

        return redirect(url_for('activity.retrieve_activities', id=id))

@plan_blueprint.route('/add/<int:id>', methods=['GET','POST'])
@login_required
def add_plan(id):
    actions = Action.query.filter(Action.id != 0).join(Plan).filter(Plan.project_id == id).all()
    activities = Activity.query.join(Action).filter(Action.id != 0).filter(Activity.action_id == Action.id).all()
    plans = Plan.query.filter(Plan.id != 0).filter(Plan.project_id == id).all()
    users = User.query.filter(User.id != 0).all()
    projects = Project.query.filter(Project.id != 0).all()
    project = Project.query.filter_by(id = id).first()
    materials = Material.query.filter(Material.id != 0).all()

    if request.method == 'GET':
        return render_template('plan/plan_add.html',
            loggedIn= 'user' in session,
            plans=plans,
            users=users,
            actions=actions,
            activities=activities,
            project=project,
            projects=projects,
            materials=materials,
            user=session.get('user')
        )
    elif request.method == 'POST':
        start_date = request.form.get('start_date', None)
        end_date = request.form.get('end_date', None)
        responsible_id = request.form.get('responsible', None)
        personnel_count = request.form.get('personnel_count', None)
        personnel_hours = request.form.get('personnel_hours', None)
        personnel_cost = request.form.get('personnel_cost', None)
        material_count = request.form.get('material_count', None)
        material_cost = request.form.get('material_cost', None)
        material_id = request.form.get('material', None)

        plan = Plan.query.filter(Plan.responsible_id == responsible_id).filter(Plan.material_id == material_id).filter(Plan.start_date == start_date).filter(Plan.end_date == end_date).first()
        if plan != None:
            return render_template('/plan/plan_add.html',
                error="Plan ya existente",
                loggedIn= 'user' in session, 
                plans=plans,
                users=users,
                actions=actions,
                activities=activities,
                project=project,
                projects=projects,
                materials=materials,
                user=session.get('user')
            )

        if start_date != None and end_date != None:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        else:
            return render_template('/plan/plan_add.html',
                error="Fechas no suministradas",
                plans=plans,
                users=users,
                actions=actions,
                activities=activities,
                project=project,
                projects=projects,
                materials=materials,
                user=session.get('user')
            )

        if start_date > end_date:
            return render_template('/plan/plan_add.html',
                error="La fecha de inicio debe ser menor a la fecha de cierre",
                plans=plans,
                users=users,
                actions=actions,
                activities=activities,
                project=project,
                projects=projects,
                materials=materials,
                user=session.get('user')
            )

        """ if start_date < project.start_date:
            return render_template('/plan/plan_add.html',
                error="La fecha de inicio no puede ser menor a la fecha de inicio del proyecto",
                plans=plans,
                users=users,
                actions=actions,
                activities=activities,
                project=project,
                projects=projects,
                materials=materials,
                user=session.get('user')
            )

        if end_date > project.end_date:
            return render_template('/plan/plan_add.html',
                error="La fecha de cierre no puede ser mayor a la fecha de cierre del proyecto",
                plans=plans,
                users=users,
                actions=actions,
                activities=activities,
                project=project,
                projects=projects,
                materials=materials,
                user=session.get('user')
            ) """

        # Preps
        personnel_count = int(personnel_count)
        personnel_cost = float(personnel_cost)

        material_cost = float(material_cost)
        material_count = int(material_count)

        # Calculations
        days = (end_date - start_date)
        hours = days.days * 8
        personnel_amount = (days.days / personnel_count) * (personnel_cost * personnel_count)
        material_amount = (material_count * material_cost)
        amount = personnel_amount + material_amount

        plan = Plan(start_date, end_date, hours, amount, responsible_id, project.id, personnel_count, personnel_hours, personnel_cost, material_id, personnel_amount, material_count, material_cost, material_amount)
        db.session.add(plan)
        db.session.commit()

        description = f"Creación de plan \"Plan {project.description}\""
        logger.catch(session['user']['username'], LogType.ADD.value, LogModule.PLANS.value, description)

        return redirect(url_for('plan.retrieve_plans', id=project.id, plans=plans, users=users, actions=actions, activities=activities, project=project, materials=materials))
