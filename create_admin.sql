-- SQLite

-- admin user
Insert into app_role (name) values('admin');
Insert into app_user (username, password, role_id) values('admin', 'pbkdf2:sha256:260000$M3v7eshrYq1Gh75f$d30f916145065b1bd5bf040f48251bc5c3ac3b1d9b5b09931b66892683281b0e', 1);

-- 4 random projects
insert into app_project (description, open_date, close_date, enabled) values ('Project 1', '2018-01-01', '2018-12-31', 1);
insert into app_project (description, open_date, close_date, enabled) values ('Project 2', '2018-01-02', '2018-12-31', 1);
insert into app_project (description, open_date, close_date, enabled) values ('Project 3', '2018-01-03', '2018-12-31', 0);
insert into app_project (description, open_date, close_date, enabled) values ('Project 4', '2018-01-04', '2018-12-31', 0);