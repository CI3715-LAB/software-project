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

-- Default roles
Insert into app_role (name) values('admin');
Insert into app_role (name) values('gerente de operaciones');
Insert into app_role (name) values('supervisor de mecánica');
Insert into app_role (name) values('supervisor de latonería y pintura');
Insert into app_role (name) values('especialista en mecánica');
Insert into app_role (name) values('especialista en electronica');
Insert into app_role (name) values('especialista en electricidad');

-- Default departments
Insert into app_department (id, name) values(0, 'Undefined');
Insert into app_department (name) values('Mecánica');
Insert into app_department (name) values('Estructura');
Insert into app_department (name) values ('Revestimiento');
Insert into app_department (name) values ('Electricidad');
Insert into app_department (name) values ('Electronica');

-- Default modules
Insert into app_module (id, name) values(0, 'Undefined');
Insert into app_module (name) values('Usuarios');
Insert into app_module (name) values('Proyectos');
Insert into app_module (name) values('Clientes');
Insert into app_module (name) values('Vehículos');
Insert into app_module (name) values('Departamentos');

-- Default permissions
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

-- Default types
Insert into app_type (name) values('Agregar');
Insert into app_type (name) values('Buscar');
Insert into app_type (name) values('Modificar');
Insert into app_type (name) values('Eliminar');

-- Default Vehicle Brands
Insert into app_vehicle_brand (name) values('Toyota');
Insert into app_vehicle_brand (name) values('Chevrolet');
Insert into app_vehicle_brand (name) values('Chery');
Insert into app_vehicle_brand (name) values('Ford');

-- Default Vehicle Models
Insert into app_vehicle_model (brand_id, name) values(1, 'Yaris');
Insert into app_vehicle_model (brand_id, name) values(1, 'Prado');
Insert into app_vehicle_model (brand_id, name) values(2, 'Cruze');
Insert into app_vehicle_model (brand_id, name) values(2, 'Aveo');
Insert into app_vehicle_model (brand_id, name) values(3, 'Tiggo');
Insert into app_vehicle_model (brand_id, name) values(3, 'Arauca');
Insert into app_vehicle_model (brand_id, name) values(4, 'Bronco');
Insert into app_vehicle_model (brand_id, name) values(4, 'Fiesta');

-- Default Vehicle Colors
Insert into app_vehicle_color (name) values('Azul');
Insert into app_vehicle_color (name) values('Rojo');
Insert into app_vehicle_color (name) values('Verde');
Insert into app_vehicle_color (name) values('Naranja');
Insert into app_vehicle_color (name) values('Plata');
Insert into app_vehicle_color (name) values('Negro');
Insert into app_vehicle_color (name) values('Blanco');
Insert into app_vehicle_color (name) values('Amarillo');
Insert into app_vehicle_color (name) values('Gris');

-- Default Clients
Insert into app_client (ci, name, lastname, birth_date, contact_number, email, address) values ('25867689', 'carlos', 'sivira', '1998-07-12', '22222222222', 'example@example.com', 'dir');
Insert into app_client (ci, name, lastname, birth_date, contact_number, email, address) values ('25867680', 'carlos2', 'sivira2', '1998-07-12', '22222222222', 'example@example.com', 'dir');
Insert into app_client (ci, name, lastname, birth_date, contact_number, email, address) values ('25867681', 'carlos3', 'sivira3', '1998-07-12', '22222222222', 'example@example.com', 'dir');
Insert into app_client (ci, name, lastname, birth_date, contact_number, email, address) values ('25867682', 'carlos4', 'sivira4', '1998-07-12', '22222222222', 'example@example.com', 'dir');

-- Default Vehicles
Insert into app_vehicle (plate, brand_id, model_id, year, chasis_serial, motor_serial, color_id, problem, client_id) values ('1234567', 1, 1, '2007', '123456781', '987654329', 1, 'Mantenimiento', 1);
Insert into app_vehicle (plate, brand_id, model_id, year, chasis_serial, motor_serial, color_id, problem, client_id) values ('1234568', 1, 2, '2007', '123456782', '987654328', 2, 'Cambio cauchos', 1);
Insert into app_vehicle (plate, brand_id, model_id, year, chasis_serial, motor_serial, color_id, problem, client_id) values ('1234569', 2, 3, '2007', '123456783', '987654327', 3, 'Alineación', 2);
Insert into app_vehicle (plate, brand_id, model_id, year, chasis_serial, motor_serial, color_id, problem, client_id) values ('1234560', 2, 4, '2007', '123456784', '987654326', 4, 'Aire acondicionado', 2);
Insert into app_vehicle (plate, brand_id, model_id, year, chasis_serial, motor_serial, color_id, problem, client_id) values ('1234561', 3, 5, '2007', '123456785', '987654325', 5, 'Cambio cauchos', 3);
Insert into app_vehicle (plate, brand_id, model_id, year, chasis_serial, motor_serial, color_id, problem, client_id) values ('1234562', 3, 6, '2007', '123456786', '987654324', 6, 'Alineación', 3);
Insert into app_vehicle (plate, brand_id, model_id, year, chasis_serial, motor_serial, color_id, problem, client_id) values ('1234563', 4, 7, '2007', '123456787', '987654323', 7, 'Aire acondicionado', 4);
Insert into app_vehicle (plate, brand_id, model_id, year, chasis_serial, motor_serial, color_id, problem, client_id) values ('1234564', 4, 8, '2007', '123456788', '987654322', 9, 'Mantenimiento', 4);

-- admin user
Insert into app_user (username, password, name, lastname, role_id, project_id, department_id) values('admin', 'pbkdf2:sha256:260000$M3v7eshrYq1Gh75f$d30f916145065b1bd5bf040f48251bc5c3ac3b1d9b5b09931b66892683281b0e', 'admin', 'admin', 1, 1, 0);

-- 4 random projects
insert into app_project (id, description, open_date, close_date, enabled, vehicle_id, department_id, solution, amount, observation) values (0, 'Undefined', '2023-01-01', '2023-12-31', 0, 1, 1, 'Cambio de aceite', 33.25, 'Aceite 15-40');
insert into app_project (description, open_date, close_date, enabled, vehicle_id, department_id, solution, amount, observation) values ('Proyecto 1', '2023-01-01', '2023-12-31', 1, 2, 2, 'Limpieza de inyectores', 10.15, 'Modelo 16344');
insert into app_project (description, open_date, close_date, enabled, vehicle_id, department_id, solution, amount, observation) values ('Proyecto 2', '2023-01-02', '2023-12-31', 1, 3, 3, 'Alineación y balanceo', 25.00, '');
insert into app_project (description, open_date, close_date, enabled, vehicle_id, department_id, solution, amount, observation) values ('Proyecto 3', '2023-01-03', '2023-12-31', 0, 4, 4, 'Cambio de correa de tiempos', 20.00, 'Modelo 1314');
insert into app_project (description, open_date, close_date, enabled, vehicle_id, department_id, solution, amount, observation) values ('Proyecto 4', '2023-01-04', '2023-12-31', 0, 5, 5, 'Cambio de pila de bomba de gasolina', 12.24, 'Modelo R2D2');

-- 4 random users
insert into app_user (username, password, name, lastname, role_id, project_id, department_id) values('alejandra', '123', 'Alejandra', 'Perez', 2, 2, 2);
insert into app_user (username, password, name, lastname, role_id, project_id, department_id) values('pedro', '123', 'Pedro', 'Rodriguez', 3, 3, 3);
insert into app_user (username, password, name, lastname, role_id, project_id, department_id) values('carla', '123', 'Carla', 'Hernandez', 4, 4, 4);
insert into app_user (username, password, name, lastname, role_id, project_id, department_id) values('juan', '123', 'Juan', 'Gonzalez', 5, 4, 1);

-- -- 10 random logs
-- insert into app_log (user_id, module_id, type_id, description, date, time) values(1, 1, 1, 'Se creo el usuario alejandra', '2023-01-01', '10:05:00');
-- insert into app_log (user_id, module_id, type_id, description, date, time) values(1, 1, 2, 'Se busco el usuario pedro', '2023-01-02', '10:10:00');
-- insert into app_log (user_id, module_id, type_id, description, date, time) values(1, 2, 1, 'Se creo el proyecto Project 1', '2023-01-03', '10:15:00');
-- insert into app_log (user_id, module_id, type_id, description, date, time) values(1, 1, 3, 'Se modifico el usuario carla', '2023-01-03', '10:20:00');
-- insert into app_log (user_id, module_id, type_id, description, date, time) values(1, 2, 2, 'Se busco el proyecto Project 1', '2023-01-03', '10:25:00');
-- insert into app_log (user_id, module_id, type_id, description, date, time) values(1, 2, 3, 'Se modifico el proyecto Project 1', '2023-01-03', '10:30:00');
-- insert into app_log (user_id, module_id, type_id, description, date, time) values(1, 1, 1, 'Se creo el usuario jose', '2023-01-04', '10:35:00');
-- insert into app_log (user_id, module_id, type_id, description, date, time) values(1, 1, 4, 'Se elimino el usuario jose', '2023-01-04', '10:40:00');
-- insert into app_log (user_id, module_id, type_id, description, date, time) values(1, 2, 1, 'Se creo el proyecto Project 5', '2023-01-04', '10:45:00');
-- insert into app_log (user_id, module_id, type_id, description, date, time) values(1, 2, 4, 'Se elimino el proyecto Project 5', '2023-01-05', '11:15:00');