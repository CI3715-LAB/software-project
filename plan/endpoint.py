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

activity_blueprint = Blueprint('activity', __name__)
action_blueprint = Blueprint('action', __name__)
plan_blueprint = Blueprint('plan', __name__)

@action_blueprint.route('/', methods=['GET'])
@login_required
def retrieve_actions():
    actions = Action.query.filter(Action.id != 0).all()
    plans = Plan.query.filter(Plan.id != 0).all()

    return render_template('plan/action_list.html',
        loggedIn= 'user' in session,
        actions=actions,
        plans=plans,
        user=session.get('user')
    )

@activity_blueprint.route('/', methods=['GET'])
@login_required
def retrieve_activities():
    activities = Activity.query.filter(Activity.id != 0).all()
    actions = Action.query.filter(Action.id != 0).all()

    return render_template('plan/activity_list.html',
        loggedIn= 'user' in session,
        activities=activities,
        actions=actions,
        user=session.get('user')
    )

@plan_blueprint.route('/', methods=['GET'])
@login_required
def retrieve_plans():
    plans = Plan.query.filter(Plan.id != 0).all()
    users = User.query.filter(User.id != 0).all()

    return render_template('plan/plan_list.html',
        loggedIn= 'user' in session,
        plans=plans,
        users=users,
        user=session.get('user')
    )

@plan_blueprint.route('/human', methods=['GET'])
@login_required
def retrieve_human_plans():
    plans = Plan.query.filter(Plan.id != 0).all()

    return render_template('plan/plan_list.html',
        loggedIn= 'user' in session,
        plans=plans,
        user=session.get('user')
    )

@plan_blueprint.route('/material', methods=['GET'])
@login_required
def retrieve_material_plans():
    plans = Plan.query.filter(Plan.id != 0).all()

    return render_template('plan/plan_list.html',
        loggedIn= 'user' in session,
        plans=plans,
        user=session.get('user')
    )