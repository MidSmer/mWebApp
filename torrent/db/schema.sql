drop table if exists torrent;
create table torrent (
  id integer primary key autoincrement,
  status integer not null,
  magnet string not null,
  name string,
  torrent BLOB
);
