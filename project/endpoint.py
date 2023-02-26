from flask import Blueprint, request, render_template, redirect, url_for, session
from sqlalchemy import or_
from datetime import datetime
from config.setup import db
from .model import Project

project_blueprint = Blueprint('project', __name__)

@project_blueprint.route('/')
def retrieve_projects():
    # if no parameters are given return all projects
	if not request.args:
		projects = Project.query.all()
		return render_template('/project/project_list.html',
			projects=projects, loggedIn= 'user' in session,
	        user=session.get('user')
	    )

    # look for projects with a similar description to the one given
	description = request.args.get('description')
	projects = Project.query.filter(
        Project.description.like('%' + description + '%')
    ).all()
	return render_template('/project/project_list.html',
        projects=projects, loggedIn= 'user' in session,
        user=session.get('user'), description=description
    )
    
	

@project_blueprint.route('/add', methods=['GET', 'POST'])
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
        return redirect(url_for('project.retrieve_projects'))
    
# update project
@project_blueprint.route('/update', methods=['POST'])
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
    return redirect(url_for('project.retrieve_projects'))
    
# enable/disable project
@project_blueprint.route('/toggle', methods=['POST'])
def enable_project():
    id = request.form['id']

    # Project exists
    project = Project.query.filter_by(id = id).first()
    if project:
        project.enabled = not project.enabled
        db.session.commit()

    return redirect(url_for('project.retrieve_projects'))

# delete project
@project_blueprint.route('/delete', methods=['POST'])
def delete_project():
    id = request.form['id']

    # Project exists
    project = Project.query.filter_by(id = id).first()
    if project:
        for user in project.users:
            user.project = Project.query.get(0)
        db.session.delete(project)
        db.session.commit()

    return redirect(url_for('project.retrieve_projects'))

@project_blueprint.route('/search', methods=['GET'])
def search_project():
    phrase = request.args.get('phrase')

    search = Project.query.filter(
        or_(
            Project.id.like('%' + phrase + '%'),
            Project.description.like('%' + phrase + '%'),
            Project.open_date.like('%' + phrase + '%'),
            Project.close_date.like('%' + phrase + '%')
        )
    )

    return render_template('/project/project_list.html', projects=search.all())