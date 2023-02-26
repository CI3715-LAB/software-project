-- SQLite
DELETE from app_project;
DELETE from app_user;
DELETE from app_role;

DELETE from app_log;
DELETE from app_type;

-- PROJECT UNDEFINED
insert into app_project (id, description, open_date, close_date, enabled) values (0, 'Proyecto sin definir', '1900-01-01', '1900-01-01', 0);

-- 4 random projects
insert into app_project (description, open_date, close_date, enabled) values ('Project 1', '2018-01-01', '2018-12-31', 1);
insert into app_project (description, open_date, close_date, enabled) values ('Project 2', '2018-01-02', '2018-12-31', 1);
insert into app_project (description, open_date, close_date, enabled) values ('Project 3', '2018-01-03', '2018-12-31', 0);
insert into app_project (description, open_date, close_date, enabled) values ('Project 4', '2018-01-04', '2018-12-31', 0);

-- admin user
Insert into app_role (name) values('admin');
Insert into app_user (username, password, role_id, project_id) values('admin', 'pbkdf2:sha256:260000$M3v7eshrYq1Gh75f$d30f916145065b1bd5bf040f48251bc5c3ac3b1d9b5b09931b66892683281b0e', 1, 1);

-- logs
INSERT INTO app_type (name) VALUES ('Proyecto');
INSERT INTO app_type (name) VALUES ('Usuario');

INSERT INTO app_log (user_id, description, date, time, type_id)
VALUES (1, 'Agregar usuario: {user_id:1, name...} Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', '2017-01-01', '00:00:00', 2);

INSERT INTO app_log (user_id, description, date, time, type_id)
VALUES (1, 'Agregar proyecto: {project_id:1, name...} Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', '2017-01-01', '00:00:00', 1);

INSERT INTO app_log (user_id, description, date, time, type_id)
VALUES (1, 'Agregar usuario: {user_id:2, name...} Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', '2017-01-01', '00:00:00', 2);

INSERT INTO app_log (user_id, description, date, time, type_id)
VALUES (1, 'Agregar proyecto: {project_id:2, name...} Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', '2017-01-01', '00:00:00', 1);

INSERT INTO app_log (user_id, description, date, time, type_id)
VALUES (1, 'Agregar usuario: {user_id:3, name...} Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', '2017-01-01', '00:00:00', 2);

INSERT INTO app_log (user_id, description, date, time, type_id)
VALUES (1, 'Eliminar proyecto: {project_id:3, name...} Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', '2017-01-01', '00:00:00', 1);

INSERT INTO app_log (user_id, description, date, time, type_id)
VALUES (1, 'Eliminar usuario: {user_id:4, name...} Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', '2017-01-01', '00:00:00', 2);

INSERT INTO app_log (user_id, description, date, time, type_id)
VALUES (1, 'Modificar proyecto: {project_id:4, name...} Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', '2017-01-01', '00:00:00', 1);
