create table if not exists products (
	id integer primary key autoincrement,
	productname text not null,
	brief text,
	created timestamp not null default (datetime('now', 'localtime')),
	category text not null,
	class text,
	filename text not null
);

create table if not exists positions (
	id integer primary key autoincrement,
	position text not null,
	salary text not null,
	created timestamp not null default current_timestamp,
	requirement text not null
);

create table if not exists apps (
	id integer primary key autoincrement,
	appname text not null,
	appurl text not null
);

create table if not exists case_modules (
	id integer primary key autoincrement,
	slug text unique not null,
	title_zh text not null,
	title_en text,
	title_ja text,
	created timestamp not null default (datetime('now', 'localtime'))
);

create table if not exists case_contents (
	id integer primary key autoincrement,
	case_id integer not null,
	type text not null,  -- 'text' or 'image'
	content_zh text,     -- For text content
	content_en text,
	content_ja text,
	filename text,       -- For image content
	sort_order integer not null,
	foreign key (case_id) references case_modules (id) on delete cascade
);
