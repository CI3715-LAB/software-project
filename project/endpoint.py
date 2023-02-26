from flask import Blueprint, request, render_template, redirect, url_for, session
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
@project_blueprint.route('/update/<int:id>', methods=['GET', 'POST'])
def update_project(id):
    if request.method == 'GET':
        project = Project.query.get(id)
        return render_template('/project/project_update.html',
            project=project, loggedIn= 'user' in session,
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
            project = Project.query.get(id)
            return render_template('/project/project_update.html',
                error="Open date must be before close date",
                description=description,
                open_date=request.form['open_date'],
                close_date=request.form['close_date'], enabled=enabled,
                loggedIn= 'user' in session,
                user=session.get('user')
            )

        # update project
        project = Project.query.get(id)
        project.description = description
        project.open_date = open_date
        project.close_date = close_date
        project.enabled = enabled
        db.session.commit()
        return redirect(url_for('project.retrieve_projects'))
    
# enable/disable project
@project_blueprint.route('/toggle/<int:id>')
def enable_project(id):
    project = Project.query.get(id)
    project.enabled = not project.enabled
    db.session.commit()
    return redirect(url_for('project.retrieve_projects'))

# delete project
@project_blueprint.route('/delete/<int:id>')
def delete_project(id):
    project = Project.query.get(id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('project.retrieve_projects'))