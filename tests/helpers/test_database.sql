-- SQLite
DELETE FROM app_project;
DELETE FROM app_type;
DELETE FROM app_module;
DELETE FROM app_role;
DELETE FROM app_log;
DELETE FROM app_user;
DELETE FROM app_vehicle_brand;
DELETE FROM app_vehicle_model;
DELETE FROM app_vehicle_color;
DELETE FROM app_client;
DELETE FROM app_vehicle;
DELETE from app_department;
DELETE from app_permission;
DELETE from app_role_permission;


-- #############################################################################
-- 									FIXED TABLES
-- #############################################################################
-- MODULE
Insert into app_module (id, name) values(0, 'Undefined');
Insert into app_module (name) values('Usuarios');
Insert into app_module (name) values('Proyectos');
Insert into app_module (name) values('Clientes');
Insert into app_module (name) values('Vehiculos');
Insert into app_module (name) values('Departamentos');


-- TYPE
Insert into app_type (name) values('Agregar');
Insert into app_type (name) values('Buscar');
Insert into app_type (name) values('Modificar');
Insert into app_type (name) values('Eliminar');


-- ROLE
Insert into app_role (name) values('admin');
-- Insert into app_role (name) values('test role1');
-- Insert into app_role (name) values('test role2');


-- PERMISSIONS
Insert into app_permission (id, type, module_id) values(0, 0, 0);
Insert into app_permission (type, module_id) values(0, 1);
Insert into app_permission (type, module_id) values(0, 2);
Insert into app_permission (type, module_id) values(0, 3);
Insert into app_permission (type, module_id) values(0, 4);
Insert into app_permission (type, module_id) values(0, 5);
Insert into app_permission (type, module_id) values(1, 1);
Insert into app_permission (type, module_id) values(1, 2);
Insert into app_permission (type, module_id) values(1, 3);
Insert into app_permission (type, module_id) values(1, 4);
Insert into app_permission (type, module_id) values(1, 5);
Insert into app_permission (type, module_id) values(2, 1);
Insert into app_permission (type, module_id) values(2, 2);
Insert into app_permission (type, module_id) values(2, 3);
Insert into app_permission (type, module_id) values(2, 4);
Insert into app_permission (type, module_id) values(2, 5);


-- VEHICLE BRAND
Insert into app_vehicle_brand (name) values('Toyota');
Insert into app_vehicle_brand (name) values('Chevrolet');
Insert into app_vehicle_brand (name) values('Chery');
Insert into app_vehicle_brand (name) values('Ford');


-- VEHICLE MODEL
Insert into app_vehicle_model (brand_id, name) values(1, 'Yaris');
Insert into app_vehicle_model (brand_id, name) values(1, 'Prado');
Insert into app_vehicle_model (brand_id, name) values(2, 'Cruze');
Insert into app_vehicle_model (brand_id, name) values(2, 'Aveo');
Insert into app_vehicle_model (brand_id, name) values(3, 'Tiggo');
Insert into app_vehicle_model (brand_id, name) values(3, 'Arauca');
Insert into app_vehicle_model (brand_id, name) values(4, 'Bronco');
Insert into app_vehicle_model (brand_id, name) values(4, 'Fiesta');


-- VEHICLE COLOR
Insert into app_vehicle_color (name) values('Azul');
Insert into app_vehicle_color (name) values('Rojo');
Insert into app_vehicle_color (name) values('Verde');
Insert into app_vehicle_color (name) values('Naranja');
Insert into app_vehicle_color (name) values('Plata');
Insert into app_vehicle_color (name) values('Negro');
Insert into app_vehicle_color (name) values('Blanco');
Insert into app_vehicle_color (name) values('Amarillo');
Insert into app_vehicle_color (name) values('Gris');



-- #############################################################################
-- 									TEST TABLES
-- #############################################################################



-- PROJECT
insert into app_project (id, description, open_date, close_date, enabled, vehicle_id, department_id, solution, amount, observation) values (0, 'Undefined', '2023-01-01', '2023-12-31', 0, 1, 1, 'Undefined Solution', 00.00, 'Undefined Observation');
insert into app_project (description, open_date, close_date, enabled, vehicle_id, department_id, solution, amount, observation) values ('Test Project', '2023-01-01', '2023-12-31', 1, 2, 2, 'Limpieza de inyectores', 10.15, 'Modelo 16344');
insert into app_project (description, open_date, close_date, enabled, vehicle_id, department_id, solution, amount, observation) values ('Test Project 2', '2023-01-02', '2023-12-31', 1, 3, 3, 'Alineación y balanceo', 25.00, 'Observaciones pendientes');


-- DEPARTMENT
Insert into app_department (id, name) values(0, 'Undefined');
Insert into app_department (name) values('Test Department');
Insert into app_department (name) values('Test Department 2');


-- CLIENT
Insert into app_client (ci, name, lastname, birth_date, contact_number, email, address) values ('25867689', 'carlos', 'sivira', '1998-07-12', '22222222222', 'example@example.com', 'dir');
Insert into app_client (ci, name, lastname, birth_date, contact_number, email, address) values ('25867680', 'carlos2', 'sivira2', '1998-07-12', '22222222222', 'example@example.com', 'dir');
Insert into app_client (ci, name, lastname, birth_date, contact_number, email, address) values ('25867681', 'carlos3', 'sivira3', '1998-07-12', '22222222222', 'example@example.com', 'dir');
Insert into app_client (ci, name, lastname, birth_date, contact_number, email, address) values ('25867682', 'carlos4', 'sivira4', '1998-07-12', '22222222222', 'example@example.com', 'dir');


-- VEHICLE
Insert into app_vehicle (plate, brand_id, model_id, year, chasis_serial, motor_serial, color_id, problem, client_id) values ('1234567', 1, 1, '2007', '123456781', '987654329', 1, 'Mantenimiento', 1);
Insert into app_vehicle (plate, brand_id, model_id, year, chasis_serial, motor_serial, color_id, problem, client_id) values ('1234568', 1, 2, '2007', '123456782', '987654328', 2, 'Cambio cauchos', 1);
Insert into app_vehicle (plate, brand_id, model_id, year, chasis_serial, motor_serial, color_id, problem, client_id) values ('1234569', 2, 3, '2007', '123456783', '987654327', 3, 'Alineación', 2);
Insert into app_vehicle (plate, brand_id, model_id, year, chasis_serial, motor_serial, color_id, problem, client_id) values ('1234560', 2, 4, '2007', '123456784', '987654326', 4, 'Aire acondicionado', 2);
Insert into app_vehicle (plate, brand_id, model_id, year, chasis_serial, motor_serial, color_id, problem, client_id) values ('1234561', 3, 5, '2007', '123456785', '987654325', 5, 'Cambio cauchos', 3);
Insert into app_vehicle (plate, brand_id, model_id, year, chasis_serial, motor_serial, color_id, problem, client_id) values ('1234562', 3, 6, '2007', '123456786', '987654324', 6, 'Alineación', 3);
Insert into app_vehicle (plate, brand_id, model_id, year, chasis_serial, motor_serial, color_id, problem, client_id) values ('1234563', 4, 7, '2007', '123456787', '987654323', 7, 'Aire acondicionado', 4);
Insert into app_vehicle (plate, brand_id, model_id, year, chasis_serial, motor_serial, color_id, problem, client_id) values ('1234564', 4, 8, '2007', '123456788', '987654322', 9, 'Mantenimiento', 4);