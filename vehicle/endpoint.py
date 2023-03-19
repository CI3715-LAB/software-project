import re

from flask import Blueprint, request, render_template, redirect, url_for, session
from sqlalchemy import or_, select
from datetime import datetime
from config.setup import db, logger
from log.utils import LogType, LogModule
from .model import Vehicle, VehicleBrand, VehicleModel, VehicleColor
from client.model import Client
from user.model import User
from werkzeug.exceptions import BadRequest

from user.utils import login_required

vehicle_blueprint = Blueprint('vehicle', __name__)

@vehicle_blueprint.route('/')
@login_required
def retrieve_vehicles():
    # return all vehicle with an id different than 0
    vehicles = Vehicle.query.all()

    return render_template('/vehicle/vehicle_list.html',
        vehicles=vehicles, loggedIn= 'user' in session,
        brands=VehicleBrand.query.all(),
        models=VehicleModel.query.all(),
        colors=VehicleColor.query.all(),
        clients=Client.query.all(),
        user=session.get('user')
    )

@vehicle_blueprint.route('/client/<int:id>')
@login_required
def retrieve_vehicles_by_client(id):
    # return all vehicle with an id different than 0
    vehicles = Vehicle.query.filter_by(client_id = id)

    return render_template('/vehicle/vehicle_list.html',
        vehicles=vehicles, loggedIn= 'user' in session,
        brands=VehicleBrand.query.all(),
        models=VehicleModel.query.all(),
        colors=VehicleColor.query.all(),
        fixed_client=id,
        clients=Client.query.all(),
        user=session.get('user')
    )
    
@vehicle_blueprint.route('/add/<int:id>', methods=['GET', 'POST'])
@login_required
def add_vehicle_by_client_id(id):
    if request.method == 'GET':
        return render_template('/vehicle/vehicle_add.html',
            brands=VehicleBrand.query.all(),
            models=VehicleModel.query.all(),
            colors=VehicleColor.query.all(),
            fixed_client=id,
            clients=Client.query.all(),
            loggedIn= 'user' in session,
            user=session.get('user')                       
        )

    if request.method == 'POST':
        plate = request.form['plate']
        brand_id = request.form['brand']
        model_id = request.form['model']
        year = request.form['year']
        chasis_serial = request.form['chasis_serial']
        motor_serial = request.form['motor_serial']
        color_id = request.form['color']
        problem = request.form['problem']
        client_id = request.form['client']

        # Return payload to template in case of error
        def error_response(msg):
            return render_template('/vehicle/vehicle_add.html',
                error=msg,
                plate = plate,
                brand_id = brand_id,
                model_id = model_id,
                year = year,
                chasis_serial = chasis_serial,
                motor_serial = motor_serial,
                color_id = color_id,
                problem = problem,
                client = client_id,
                brands=VehicleBrand.query.all(),
                models=VehicleModel.query.all(),
                colors=VehicleColor.query.all(),
                fixed_client=id,
                clients=Client.query.all(),
                loggedIn= 'user' in session,
                user=session.get('user')
            )

        # Check if plate is new and different 
        plate_check = Vehicle.query.filter_by(plate=plate).first()
        if plate_check:
            return error_response('The given plate already exists') 

        # Check if chasis_serial is new and different 
        chasis_check = Vehicle.query.filter_by(chasis_serial=chasis_serial).first()
        if chasis_check:
            return error_response('The given chasis serial already exists') 

        # Check if motor_serial is new and different 
        motor_check = Vehicle.query.filter_by(motor_serial=motor_serial).first()
        if motor_check:
            return error_response('The given motor serial already exists')

        # Validate plate format
        if not re.match("^[A-Z0-9]*$", plate):
            return error_response('Invalid plate format')

        # Validate plate length
        if len(plate) != 7:
            return error_response('Invalid plate length')

        # Validate if given brand exists
        if not VehicleBrand.query.filter_by(id =  brand_id).first():
            return error_response('Invalid brand Id')

        # Validate if given model exists
        if not VehicleModel.query.filter_by(id =  model_id).first():
            return error_response('Invalid model Id')

        # Validate if given color exists
        if not VehicleColor.query.filter_by(id =  color_id).first():
            return error_response('Invalid color Id')

        # Validate if year is in range
        if (int(year) < 1900 or int(year) > 2025):
            return error_response('Invalid year')
        
        # Validate chasis_serial format
        if not re.match("^[A-Z0-9]*$", chasis_serial):
            return error_response('Invalid plate format')

        # Validate chasis_motor format
        if not re.match("^[A-Z0-9]*$", motor_serial):
            return error_response('Invalid plate format')

        # create a new vehicle
        vehicle = Vehicle(plate, brand_id, model_id, year, chasis_serial, motor_serial, color_id, problem, id)
        db.session.add(vehicle)
        db.session.commit()

        description = f"Creación de vehiculo \"{vehicle.plate}\""
        logger.catch(session['user']['username'], LogType.ADD.value, LogModule.VEHICLES.value, description)

        return redirect(url_for('vehicle.retrieve_vehicles'))
    

@vehicle_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add_vehicle():
    if request.method == 'GET':
        return render_template('/vehicle/vehicle_add.html',
            brands=VehicleBrand.query.all(),
            models=VehicleModel.query.all(),
            colors=VehicleColor.query.all(),
            clients=Client.query.all(),
            loggedIn= 'user' in session,
            user=session.get('user')                       
        )

    if request.method == 'POST':
        plate = request.form['plate']
        brand_id = request.form['brand']
        model_id = request.form['model']
        year = request.form['year']
        chasis_serial = request.form['chasis_serial']
        motor_serial = request.form['motor_serial']
        color_id = request.form['color']
        problem = request.form['problem']
        client_id = request.form['client']

        # Return payload to template in case of error
        def error_response(msg):
            return render_template('/vehicle/vehicle_add.html',
                error=msg,
                plate = plate,
                brand_id = brand_id,
                model_id = model_id,
                year = year,
                chasis_serial = chasis_serial,
                motor_serial = motor_serial,
                color_id = color_id,
                problem = problem,
                client = client_id,
                brands=VehicleBrand.query.all(),
                models=VehicleModel.query.all(),
                colors=VehicleColor.query.all(),
                clients=Client.query.all(),
                loggedIn= 'user' in session,
                user=session.get('user')
            )

        # Check if plate is new and different 
        plate_check = Vehicle.query.filter_by(plate=plate).first()
        if plate_check:
            return error_response('The given plate already exists') 

        # Check if chasis_serial is new and different 
        chasis_check = Vehicle.query.filter_by(chasis_serial=chasis_serial).first()
        if chasis_check:
            return error_response('The given chasis serial already exists') 

        # Check if motor_serial is new and different 
        motor_check = Vehicle.query.filter_by(motor_serial=motor_serial).first()
        if motor_check:
            return error_response('The given motor serial already exists')

        # Validate plate format
        if not re.match("^[A-Z0-9]*$", plate):
            return error_response('Invalid plate format')

        # Validate plate length
        if len(plate) != 7:
            return error_response('Invalid plate length')

        # Validate if given brand exists
        if not VehicleBrand.query.filter_by(id =  brand_id).first():
            return error_response('Invalid brand Id')

        # Validate if given model exists
        if not VehicleModel.query.filter_by(id =  model_id).first():
            return error_response('Invalid model Id')

        # Validate if given color exists
        if not VehicleColor.query.filter_by(id =  color_id).first():
            return error_response('Invalid color Id')

        # Validate if year is in range
        if (int(year) < 1900 or int(year) > 2025):
            return error_response('Invalid year')
        
        # Validate chasis_serial format
        if not re.match("^[A-Z0-9]*$", chasis_serial):
            return error_response('Invalid plate format')

        # Validate chasis_motor format
        if not re.match("^[A-Z0-9]*$", motor_serial):
            return error_response('Invalid plate format')

        # create a new vehicle
        vehicle = Vehicle(plate, brand_id, model_id, year, chasis_serial, motor_serial, color_id, problem, client_id)
        db.session.add(vehicle)
        db.session.commit()

        description = f"Creación de vehiculo \"{vehicle.plate}\""
        logger.catch(session['user']['username'], LogType.ADD.value, LogModule.VEHICLES.value, description)

        return redirect(url_for('vehicle.retrieve_vehicles'))
    
# update vehicle
@vehicle_blueprint.route('/update', methods=['POST'])
@login_required
def update_vehicle():
    # get description, open date and close date
    id = request.form['id']
    plate = request.form['plate']
    brand_id = request.form['brand']
    model_id = request.form['model']
    year = request.form['year']
    chasis_serial = request.form['chasis_serial']
    motor_serial = request.form['motor_serial']
    color_id = request.form['color']
    problem = request.form['problem']

    vehicle = Vehicle.query.filter_by(id=id).first()

    # Return payload to template in case of error
    def error_response(msg):
        return render_template('/vehicle/vehicle_list.html',
            error=msg,
            plate = plate,
            brand_id = brand_id,
            model_id = model_id,
            year = year,
            chasis_serial = chasis_serial,
            motor_serial = motor_serial,
            color_id = color_id,
            problem = problem,
            client = client_id,
            brands=VehicleBrand.query.all(),
            models=VehicleModel.query.all(),
            colors=VehicleColor.query.all(),
            clients=Client.query.all(),
            loggedIn= 'user' in session,
            user=session.get('user')
        )

    # Check if plate is new and different 
    plate_check = Vehicle.query.filter_by(plate=plate).first()
    if plate != vehicle.plate and plate_check:
        return error_response('The given plate already exists') 

    # Check if chasis_serial is new and different 
    chasis_serial_check = Vehicle.query.filter_by(chasis_serial=chasis_serial).first()
    if chasis_serial != vehicle.chasis_serial and chasis_serial_check:
        return error_response('The given chasis serial already exists') 

    # Check if motor_serial is new and different 
    motor_serial_check = Vehicle.query.filter_by(motor_serial=motor_serial).first()
    if motor_check != vehicle.motor_serial and motor_serial_check:
        return error_response('The given motor serial already exists')

    # Validate plate format
    if not re.match("^[A-Z0-9]*$", plate):
        return error_response('Invalid plate format')

    # Validate plate length
    if len(plate) != 7:
        return error_response('Invalid plate length')

    # Validate if given brand exists
    if not VehicleBrand.query.filter_by(id =  brand_id).first():
        return error_response('Invalid brand Id')

    # Validate if given model exists
    if not VehicleModel.query.filter_by(id =  model_id).first():
        return error_response('Invalid model Id')

    # Validate if given color exists
    if not VehicleColor.query.filter_by(id =  color_id).first():
        return error_response('Invalid color Id')

    # Validate if year is in range
    if (int(year) < 1900 or int(year) > 2025):
        return error_response('Invalid year')
    
    # Validate chasis_serial format
    if not re.match("^[A-Z0-9]*$", chasis_serial):
        return error_response('Invalid plate format')

    # Validate chasis_motor format
    if not re.match("^[A-Z0-9]*$", motor_serial):
        return error_response('Invalid plate format')
    
    # update vehicle
    if vehicle.plate != plate: vehicle.plate = plate
    if vehicle.brand_id != brand_id: vehicle.plate = plate
    if vehicle.model_id != model_id: vehicle.plate = plate
    if vehicle.year != year: vehicle.plate = plate
    if vehicle.chasis_serial != chasis_serial: vehicle.plate = plate
    if vehicle.motor_serial != motor_serial: vehicle.plate = plate
    if vehicle.color_id != color_id: vehicle.plate = plate
    if vehicle.problem != problem: vehicle.plate = plate

    db.session.commit()

    description = f"Modificación de vehiculo \"{vehicle.plate}\""
    logger.catch(session['user']['username'], LogType.MODIFY.value, LogModule.VEHICLES.value, description)

    return redirect(url_for('vehicle.retrieve_vehicles'))

# delete vehicle
@vehicle_blueprint.route('/delete', methods=['POST'])
@login_required
def delete_vehicle():
    id = request.form['id']

    # vehicle exists
    vehicle = db.session.get(Vehicle, id)
    if vehicle:
        db.session.delete(vehicle)
        db.session.commit()

    description = f"Eliminado de vehiculo \"{vehicle.plate}\""
    logger.catch(session['user']['username'], LogType.DELETE.value, LogModule.VEHICLES.value, description)

    return redirect(url_for('vehicle.retrieve_vehicles'))

@vehicle_blueprint.route('/search', methods=['GET'])
@login_required
def search_vehicle():
    phrase = request.args.get('phrase')
    vehicles = db.session.query(Vehicle).select_from(Vehicle).join(VehicleBrand).join(VehicleModel).join(VehicleColor).filter(
        or_(
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
    logger.catch(session['user']['username'], LogType.SEARCH.value, LogModule.VEHICLES.value, description)

    return render_template('/vehicle/vehicle_list.html', vehicles=vehicles, phrase=phrase)