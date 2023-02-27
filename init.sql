-- SQLite
DELETE FROM app_project;
DELETE FROM app_type;
DELETE FROM app_module;
DELETE FROM app_role;
DELETE FROM app_log;
DELETE FROM app_user;

-- Default roles
Insert into app_role (name) values('admin');
Insert into app_role (name) values('gerente de operaciones');
Insert into app_role (name) values('supervisor de mecanica');
Insert into app_role (name) values('supervisor de latoneria y pintura');
Insert into app_role (name) values('especialista en mecanica');
Insert into app_role (name) values('especialista en electronica');
Insert into app_role (name) values('especialista en electricidad');

-- Default modules
Insert into app_module (name) values('Usuarios');
Insert into app_module (name) values('Proyectos');

-- Default types
Insert into app_type (name) values('Agregar');
Insert into app_type (name) values('Buscar');
Insert into app_type (name) values('Modificar');
Insert into app_type (name) values('Eliminar');

-- admin user
Insert into app_user (username, password, name, lastname, role_id, project_id) values('admin', 'pbkdf2:sha256:260000$M3v7eshrYq1Gh75f$d30f916145065b1bd5bf040f48251bc5c3ac3b1d9b5b09931b66892683281b0e', 'admin', 'admin', 1, 1);

-- 4 random projects
insert into app_project (id, description, open_date, close_date, enabled) values (0, 'Undefined', '2023-01-01', '2023-12-31', 0);
insert into app_project (description, open_date, close_date, enabled) values ('Proyecto 1', '2023-01-01', '2023-12-31', 1);
insert into app_project (description, open_date, close_date, enabled) values ('Proyecto 2', '2023-01-02', '2023-12-31', 1);
insert into app_project (description, open_date, close_date, enabled) values ('Proyecto 3', '2023-01-03', '2023-12-31', 0);
insert into app_project (description, open_date, close_date, enabled) values ('Proyecto 4', '2023-01-04', '2023-12-31', 0);

-- 4 random users
insert into app_user (username, password, name, lastname, role_id, project_id) values('alejandra', '123', 'Alejandra', 'Perez', 2, 2);
insert into app_user (username, password, name, lastname, role_id, project_id) values('pedro', '123', 'Pedro', 'Rodriguez', 3, 3);
insert into app_user (username, password, name, lastname, role_id, project_id) values('carla', '123', 'Carla', 'Hernandez', 4, 4);
insert into app_user (username, password, name, lastname, role_id, project_id) values('juan', '123', 'Juan', 'Gonzalez', 5, 4);


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