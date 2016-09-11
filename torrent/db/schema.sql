drop table if exists user;
create table user (
  id integer primary key autoincrement,
  name string not null,
  passwd string not null,
  status integer not null
);

drop table if exists torrent;
create table torrent (
  id integer primary key autoincrement,
  status integer not null,
  magnet string not null,
  name string,
  torrent TEXT
);

drop table if exists join_user_torrent;
create table join_user_torrent (
  id integer primary key autoincrement,
  user_id integer not null,
  torrent_id integer not null
);
