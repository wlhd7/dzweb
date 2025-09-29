drop table if exists messages;

create table if not exists users (
	id integer primary key autoincrement,
	username text unique not null,
	password text not null,
	color text,
	applist text
);

create table if not exists products (
	id integer primary key autoincrement,
	productname text not null,
	brief text,
	created timestamp not null default (datetime('now', 'localtime')),
	category text not null,
	filename text not null
);

create table if not exists positions (
	id integer primary key autoincrement,
	position text not null,
	salary text not null,
	created timestamp not null default current_timestamp,
	requirement text not null
);

create table if not exists messages (
	id integer primary key autoincrement,
	author_id integer,
	message text not null,
	created timestamp not null default (datetime('now', 'localtime')),
	foreign key (author_id) references users (id)
);

create table if not exists apps (
	id integer primary key autoincrement,
	appname text not null,
	apppassword text not null,
	appurl text not null
);

create table if not exists staffs (
	id integer primary key autoincrement,
	name text unique not null,
	department text not null,
	sub_department text
);
