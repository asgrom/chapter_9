import os
import sqlite3 as sql


def create_tables(database):
    database = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'sqlite',
        database
    )
    conn = sql.connect(database)
    with open(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'sqlite',
            'create_tables.sql')) as f:
        script = f.read()
    try:
        with conn:
            conn.executescript(script)
    except sql.Error as e:
        print(e)
        exit()
    finally:
        conn.close()


def get_data(database):
    print(database)
    conn = sql.connect(database)
    with conn:
        conn.executescript('''
            pragma foreign_keys=on;
            insert into actors (name)
            values ('Джон Траволта');
            insert into actors (name)
            values ('Киану Ривз');

            insert into films (title)
            values ('bla-bla-bla');

            insert into film_actors (id_film, id_actor)
            VALUES (1, 1);
            insert into film_actors (id_film, id_actor)
            VALUES (1, '');

            insert into film_actors (id_film, id_actor)
            values (1, 3);

            select name
            from actors
            where id =
                  (select id_actor from film_actors where id_film = 1);

            insert into film_actors (id_film, id_actor) VALUES (22,33);
            delete from films where id=1;
        ''')
    for i in conn.execute('select * from films'):
        print(i)
    conn.close()


if __name__ == '__main__':
    import sys

    create_tables(sys.argv[1])
    # get_data(os.path.abspath(sys.argv[1]))
