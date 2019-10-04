PRAGMA foreign_keys= on;
create table films
(
    id            integer primary key autoincrement,
    title         text unique not null,
--     альтернативное название
    title1        text,
--     описание фильма
    desc          text,
--     факты о фильме
    facts         text,
    year          text,
--     ограничение по возрасту
    ageLimit      text,
--     продолжительность фильма
    duration      text,
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
    releaseDVDUsa text,
    releaseBluRay text,
--     ошибки в фильме
    error         text,
    rating        text,
    critics       text,
    digitRelease  text,
    marketing     text,
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
create table directors
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
create table artDirectors
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
    id_actor integer,
    constraint fk_films_id foreign key (id_film) references films (id),
    constraint fk_actors_id foreign key (id_actor) references actors (id)
);
create table film_producer
(
    id_film     integer,
    id_producer integer,
    constraint fk_films_id foreign key (id_film) references films (id),
    constraint fk_producers_id foreign key (id_producer) references producers (id)
);
create table film_genre
(
    id_film  integer,
    id_genre integer,
    constraint fk_films_id foreign key (id_film) references films (id),
    constraint fk_genres_id foreign key (id_genre) references genres (id)
);
create table film_director
(
    id_film     integer,
    id_director integer,
    constraint fk_films_id foreign key (id_film) references films (id),
    constraint fk_directors_id foreign key (id_director) references directors (id)
);
create table film_operator
(
    id_film     integer,
    id_operator integer,
    constraint fk_films_id foreign key (id_film) references films (id),
    constraint fk_operators_id foreign key (id_operator) references operators (id)
);
create table film_editor
(
    id_film   integer,
    id_editor integer,
    constraint fk_films_id foreign key (id_film) references films (id),
    constraint fk_editors_id foreign key (id_editor) references operators (id)
);
create table film_artDirector
(
    id_film        integer,
    id_artDirector integer,
    constraint fk_films_id foreign key (id_film) references films (id),
    constraint fk_artDirectors_id foreign key (id_artDirector) references artDirectors (id)
);
create table film_composer
(
    id_film     integer,
    id_composer integer,
    constraint fk_films_id foreign key (id_film) references films (id),
    constraint fk_composers_id foreign key (id_composer) references composers (id)
);
create table film_country
(
    id_film    integer not null,
    id_country integer not null,
    constraint fk_films_id foreign key (id_film) references films (id),
    constraint fk_countries_id foreign key (id_country) references countries (id)
);
create table film_dubbing
(
    id_film integer,
    id_dub  integer,
    constraint fk_films_id foreign key (id_film) references films (id),
    constraint fk_dubbing_id foreign key (id_dub) references dubbing (id)
);
create table film_writer
(
    id_film   integer,
    id_writer integer,
    constraint fk_films_id foreign key (id_film) references films (id),
    constraint fk_writers_id foreign key (id_writer) references writers (id)
)