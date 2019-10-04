create table films
(
    id            integer primary key autoincrement,
    title         text unique not null,
--     описание фильма
    desc          text,
--     факты о фильме
    facts         text,
    year          integer,
--     ограничение по возрасту
    ageLimit      text,
--     продолжительность фильма
    runtime       text,
--     ограничение по возрасту от MPAA
    rateMPAA      text,
--     бюджет
    budget        text,
--     сборы фильма по странам
    moneyUSA      text,
    moneyWorld    text,
    moneyRussia   text,
--     слоган
    slogan        text,
--     количество просмотров
    people        text,
    releaseWorld  text,
    releaseRussia text,
    reliaseDVD    text,
    releaseBluRay text,
--     ошибки в фильме
    error         text,
    rating        text,
    critics       text,
--     постер
    image         blob
);
create table actors
-- актеры
(
    id   integer primary key autoincrement,
    name text not null unique
);
create table composers
-- композитор
(
    id   integer primary key autoincrement,
    name text unique not null
);
create table producers
-- продюссер
(
    id   integer primary key autoincrement,
    name text unique not null
);
create table director
-- режиссер
(
    id   integer primary key autoincrement,
    name text unique not null
);
create table writers
-- сценарист
(
    id   integer primary key autoincrement,
    name text not null unique
);
create table operators
-- оператор
(
    id   integer primary key autoincrement,
    name text not null unique
);
create table artDirector
-- художник
(
    id   integer primary key autoincrement,
    name text not null unique

);
create table editors
-- монтажер
(
    id   integer primary key autoincrement,
    name text not null unique
);
create table countries
-- страна
(
    id   integer primary key autoincrement,
    name text unique not null
);
create table genres
-- жанр
(
    id    integer primary key autoincrement,
    genre text not null unique
);
create table dubbing
-- роли дублировали
(
    id   integer primary key autoincrement,
    name text unique not null
);
create table film_actors
(
    id_film  integer,
    id_actor integer
);
create table film_producer
(
    id_film     integer,
    id_producer integer
);
create table film_genre
(
    id_film  integer,
    id_genre integer
);
create table film_director
(
    id_film     integer,
    id_director integer
);
create table film_operator
(
    id_film     integer,
    id_operator integer
);
create table film_editor
(
    id_film   integer,
    id_editor integer
);
create table film_artDirector
(
    id_film        integer,
    id_artDirector integer
);
create table film_composer
(
    id_film     integer,
    id_composer integer
);
create table film_country
(
    id_film    integer,
    id_country integer
);
create table film_dubbing
(
    id_film integer,
    id_dub  integer
);
create table film_writer
(
    id_film   integer,
    id_writer integer
)