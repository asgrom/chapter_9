import os
import sqlite3 as sql


def create_tables(database):
    database = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'sqlite',
        database
    )
    print(database)
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
    # with conn:
    #     conn.execute('insert into films (title) values ("bla-bla-bla")')
    # conn.close()


def get_data(database):
    conn = sql.connect(database)
    for i in conn.execute('select * from films'):
        print(i)
    conn.close()


if __name__ == '__main__':
    import sys

    create_tables(sys.argv[1])
    # get_data(os.path.abspath((sys.argv[1])))
