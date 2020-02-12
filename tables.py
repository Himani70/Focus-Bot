#!/usr/bin/python
 
import psycopg2
 
def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE FOCUSSESSION
      (
               userid VARCHAR(50) NOT NULL,
               weekid smallint NOT NULL,
               Session1 NUMERIC,
               Session2 NUMERIC,
               Session3 NUMERIC,
               Session4 NUMERIC,
               Session5 NUMERIC,
               Session6 NUMERIC,
               Session7 NUMERIC,
               Session8 NUMERIC,
               Session9 NUMERIC,
               Session10 NUMERIC,
               Session11 NUMERIC,
               Session12 NUMERIC,
               Session13 NUMERIC,
               Session14 NUMERIC,
               Session15 NUMERIC,
               Session16 NUMERIC,
               Session17 NUMERIC,
               Session18 NUMERIC,
               Session19 NUMERIC,
               Session20 NUMERIC,
               Session21 NUMERIC,
               Session22 NUMERIC,
               Session23 NUMERIC,
               Session24 NUMERIC,
               Session25 NUMERIC,
               Session26 NUMERIC,
               Session27 NUMERIC,
               Session28 NUMERIC,
               Session29 NUMERIC,
               Session30 NUMERIC,
               Session31 NUMERIC,
               Session32 NUMERIC,
               Session33 NUMERIC,
               Session34 NUMERIC,
               Session35 NUMERIC,
               Session36 NUMERIC,
               Session37 NUMERIC,
               Session38 NUMERIC,
               Session39 NUMERIC,
               Session40 NUMERIC,
               PRIMARY KEY(UserId, WeekId) 
      )
        """,
        """ CREATE TABLE USERMETADATA(userid VARCHAR(50) PRIMARY KEY, 
Monday bigint ,
Tuesday bigint ,
Wednesday bigint ,
Thursday bigint ,
Friday bigint ,
activeTask VARCHAR(50) )
        """,
        """ INSERT INTO USERMETADATA VALUES ('pkannia',0,0,0,0,0, '-1')""",
        """ INSERT INTO USERMETADATA VALUES ('hjangam',0,0,0,0,0, '-1')""",
        """ INSERT INTO USERMETADATA VALUES ('pbhalas',0,0,0,0,0, '-1')""",
        """ INSERT INTO USERMETADATA VALUES ('jcheruk' ,0,0,0,0,0, '-1')""",
        """ INSERT INTO USERMETADATA VALUES ('cjparnin',0,0,0,0,0, '-1')""",
        """ INSERT INTO USERMETADATA VALUES ('ffhamid',0,0,0,0,0, '-1')""",
        """ INSERT INTO USERMETADATA VALUES ('yshi26',0,0,0,0,0, '-1')""",
        """ INSERT INTO USERMETADATA VALUES ('focusbotuser',0,0,0,0,0, '-1')""")
    conn = None
    try:
        # read the connection parameters
        # connect to the PostgreSQL server
        #conn = psycopg2.connect(**params)
        conn = psycopg2.connect(host="localhost",database="focusbotDB", user="focusbot", password="focusbot")
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
          
        cur.execute("""SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'""")
        for table in cur.fetchall():
            print(table)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
 
 
if __name__ == '__main__':
    create_tables()
