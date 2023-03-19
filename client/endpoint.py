import re

from flask import Blueprint, request, render_template, redirect, url_for, session
from sqlalchemy import or_, select
from datetime import datetime
from config.setup import db, logger
from log.utils import LogType, LogModule
from vehicle.model import Vehicle, VehicleBrand, VehicleModel, VehicleColor
from .model import Client
from user.model import User
from werkzeug.exceptions import BadRequest

from user.utils import login_required

client_blueprint = Blueprint('client', __name__)

@client_blueprint.route('/')
@login_required
def retrieve_clients():
    # return all clients with an id different than 0
    clients = Client.query.all()

    return render_template('/client/client_list.html',
        clients=clients, loggedIn= 'user' in session,
        user=session.get('user')
    )

@client_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add_client():
    if request.method == 'GET':
        return render_template('/client/client_add.html',
            loggedIn= 'user' in session,
            user=session.get('user')                       
        )

    if request.method == 'POST':
        ci = request.form['ci']
        name = request.form['name']
        lastname = request.form['lastname']
        birth_date = request.form['birth_date']
        contact_number = request.form['contact_number']
        email = request.form['email']
        address = request.form['address']

        # Return payload to template in case of error
        def error_response(msg):
            return render_template('/client/client_add.html',
                error="Esta cedula ya se encuentra registrada",
                ci = ci,
                name = name,
                lastname = lastname,
                birth_date = birth_date,
                contact_number = contact_number,
                email = email,
                address = address,
                loggedIn= 'user' in session,
                user=session.get('user')
            )

        # Validate unique ci
        ci_check = Client.query.filter_by(ci=ci).first()
        if ci_check: return error_response('Esta cedula ya se encuentra registrada')

        # Validate email
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            return error_response('El formato del correo electrónico es inválido')

        # create a new vehicle
        bdate = datetime.strptime(birth_date, '%Y-%m-%d')
        client = Client(ci, name, lastname, bdate, contact_number, email, address)
        db.session.add(client)
        db.session.commit()

        description = f"Creación de cliente \"{client.ci}\""
        logger.catch(session['user']['username'], LogType.ADD.value, LogModule.CLIENTS.value, description)

        return redirect(url_for('client.retrieve_clients'))

@client_blueprint.route('/update', methods=['POST'])
@login_required
def update_client():
    id = request.form['id']
    ci = request.form['ci']
    name = request.form['name']
    lastname = request.form['lastname']
    birth_date = request.form['birth_date']
    contact_number = request.form['contact_number']
    email = request.form['email']
    address = request.form['address']

    client = Client.query.filter_by(id=id).first()

    # Return payload to template in case of error
    def error_response(msg):
        return render_template('/client/client_add.html',
            error="Esta cedula ya se encuentra registrada",
            ci = ci,
            name = name,
            lastname = lastname,
            birth_date = birth_date,
            contact_number = contact_number,
            email = email,
            address = address,
            loggedIn= 'user' in session,
            user=session.get('user')
        )

    # Validate unique ci
    ci_check = Client.query.filter_by(ci=ci).first()
    if ci != client.ci and ci_check: 
        return error_response('Esta cedula ya se encuentra registrada')

    # Validate email
    if not re.match("[^@]+@[^@]+\.[^@]+", email):
        return error_response('El formato del correo electrónico es inválido')

    # update vehicle
    if client.ci != ci : client.ci = ci
    if client.name != name : client.name = name
    if client.lastname != lastname : client.lastname = lastname
    if client.birth_date != birth_date : 
        bdate = datetime.strptime(birth_date, '%Y-%m-%d')
        client.birth_date = bdate
    if client.contact_number != contact_number : client.contact_number = contact_number
    if client.email != email : client.email = email
    if client.address != address : client.address = address

    db.session.commit()

    description = f"Modificación de cliente \"{client.ci}\""
    logger.catch(session['user']['username'], LogType.MODIFY.value, LogModule.CLIENTS.value, description)

    return redirect(url_for('client.retrieve_clients'))

# delete client
@client_blueprint.route('/delete', methods=['POST'])
@login_required
def delete_vehicle():
    id = request.form['id']

    # client exists
    client = db.session.get(Client, id)
    if client:
        db.session.delete(client)
        db.session.commit()

    description = f"Eliminado de cliente \"{client.ci}\""
    logger.catch(session['user']['username'], LogType.DELETE.value, LogModule.CLIENTS.value, description)

    return redirect(url_for('client.retrieve_clients'))

@client_blueprint.route('/search', methods=['GET'])
@login_required
def search_vehicle():
    phrase = request.args.get('phrase')
    clients = db.session.query(Client).select_from(Client).join(Vehicle).join(VehicleBrand).join(VehicleModel).join(VehicleColor).filter(
        or_(
            Client.id.like('%' + phrase + '%'),
            Client.ci.like('%' + phrase + '%'),
            Client.name.like('%' + phrase + '%'),
            Client.lastname.like('%' + phrase + '%'),
            Client.birth_date.like('%' + phrase + '%'),
            Client.contact_number.like('%' + phrase + '%'),
            Client.email.like('%' + phrase + '%'),
            Client.address.like('%' + phrase + '%'),
            Vehicle.plate.like('%' + phrase + '%'),
            VehicleBrand.name.like('%' + phrase + '%'),
            VehicleModel.name.like('%' + phrase + '%'),
            Vehicle.year.like('%' + phrase + '%'),
            Vehicle.chasis_serial.like('%' + phrase + '%'),
            Vehicle.motor_serial.like('%' + phrase + '%'),
            VehicleColor.name.like('%' + phrase + '%'),
            Vehicle.problem.like('%' + phrase + '%')
        )
    )

    description = f"Busqueda de vehiculos por frase \"{phrase}\""
    logger.catch(session['user']['username'], LogType.SEARCH.value, LogModule.CLIENTS.value, description)

    return render_template('/client/client_list.html', clients=clients, phrase=phrase)