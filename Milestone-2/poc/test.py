from jira import JIRA
import psycopg2
from postgresConfig import config
 
class MyDB(object):

    def __init__(self):
    	
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        self.conn = psycopg2.connect(**params)
        self.cur = self.conn.cursor()
        #print(self.conn, self.cursor)

    def query(self, query, params):
    	#print(self.conn, self.cur)
        self.cur.execute(query, params)
        return self.cur
        

    def __del__(self):
        self.conn.close()

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        print(conn)
      
        # create a cursor
        cur = conn.cursor()
   #      print(cur)
   # # execute a statement
   #      print('PostgreSQL database version:')
   #      cur.execute('SELECT version()')
 
   #      # display the PostgreSQL database server version
   #      db_version = cur.fetchone()
   #      print(db_version)

       
        print("Print tables: ")
        

        conn.commit()
        cur.execute("SELECT activetask FROM usermetadata WHERE userid = pbhalas")
        print(cur.fetchone())
        #cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        # for table in cur.fetchall():
        #     print(table)

       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
 
 
def check(db):
    a = "activetask"
    cur = db.query("SELECT "+a+" FROM usermetadata WHERE userid = %s", ("pbhalas",))
    if "NULL" in cur.fetchone():
        print("TRUE")
    print(cur.fetchone())
    # if cur.fetchone() is not None:
    #     # output = db.query("INSERT INTO usermapping (slackid, jiraid) VALUES (%s,%s)", ("slackID2", "jiraID2"))
    #     # print(db.cur.fetchone())
    #     # db.conn.commit()
    #     aa ="jiraid"
    #     output = db.query("Update usermapping set "+aa+" = %s where slackid = %s",("test","slackID1"))
    #     print(output)
    #     db.conn.commit()

    # cur = db.query('SELECT version()', None)
    # print('PostgreSQL database version:')
    # db_version = cur.fetchone()
    # print(db_version)

if __name__ == '__main__':
    #connect()
    db = MyDB()
    #connect()
    #check(db)


    jira = JIRA(basic_auth=('jcheruk@ncsu.edu', 'NlVW7BXchvw2x0gn2SlQC60E'),
                    options={'server': 'https://focus-bot.atlassian.net'})
    issue = jira.issue('SF-19')
    print(issue.raw)

#[(u'11', u'To Do'), (u'21', u'In Progress'), (u'31', u'Done')]
    
# try:
# 	issue = jira.issue('SF-4')
# 	print(issue)
# 	transitions = jira.transitions(issue)
# 	print([(t['id'], t['name']) for t in transitions])
# 	jira.transition_issue(issue, '111')
# 	issue = jira.issue('SF-4')
# 	print(issue.fields.status.name)
# except Exception as e:
# 	print("type error: " + str(e.text))