import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, url_for, request
from flask import Response, make_response
import sys
from slackclient import SlackClient
import json
import requests
import threading
import datetime
from datetime import date, datetime
import os
import math
import time
from jira import JIRA
import psycopg2
import seaborn as sns
import pandas as pd
import numpy as np
import pdb

app = Flask(__name__)

tokens = {}
filePath = sys.argv[1]
with open(filePath) as json_data:
    tokens = json.load(json_data)

slackEvent = None
slack_client = SlackClient(tokens.get("slack_bot_token"))
jira = JIRA(basic_auth=(tokens.get("userId"), tokens.get("userToken")),
                    options={'server': tokens.get("serverEndPoint")})

class DBConnection(object):

    def __init__(self):
        
        # read connection parameters
        #params = config()
        # connect to the PostgreSQL server
        self.conn = psycopg2.connect(host=tokens['host'], database=tokens['database'], user=tokens['user'], password=tokens['password'])
        self.cur = self.conn.cursor()

    def query(self, query, params):
        self.cur.execute(query, params)
        return self.cur
        
    def __del__(self):
        self.conn.close()


#only created once per session
db = DBConnection()


def getCurrentWeek():
    return date.today().isocalendar()[1]


def readJson(filename):
    with open(filename) as file:
       return(json.load(file))

def getCurrentDay():
    return datetime.today().strftime('%A')

def get_user(user_id):
    payload = {'token': tokens.get("slack_bot_token"), 'user': user_id}
    r = requests.get('https://slack.com/api/users.info', params=payload)
    res = json.loads(r.text)
    return res['user']['name']


#this method will be called after the status is checked
def closeIssue(issueId):
    try:
        issue = jira.issue(issueId)
        #11-toDo 21-in progress 31-close issue
        issue.update(customfield_10016=0)
        jira.transition_issue(issue, '31')
    except Exception as e:
        return "Error"
    return "Success"

def changeTaskStatus(issueId):
    try:
        issue = jira.issue(issueId)
        #11-toDo 21-in progress 31-close issue
        jira.transition_issue(issue, '21')
    except Exception as e:
        return "Error"
    return "Success"



def updateTaskStatus(taskPercentage, issueId):
 
    issue = jira.issue(issueId)
    #u'customfield_10027 - total task point
    #print(issue.raw)

    totalPoint = issue.fields.customfield_10027
    currentPoint = issue.fields.customfield_10016
    if taskPercentage==100:
        closeIssue(issueId)
        return currentPoint-0.00
    if (((totalPoint-currentPoint)/totalPoint)*100) > taskPercentage:
        return -1
    else:
        pointsCompleted = (totalPoint * taskPercentage)/100
        issue.update(customfield_10016=round(totalPoint-pointsCompleted,2))
    print("CURRENT POINT :"+str(currentPoint))
    return currentPoint-(totalPoint-pointsCompleted)

def getProjects():
    projects = jira.projects()
    return projects

def CheckProjectKey(new_issue):
    projects = getProjects()
    for project in projects:
        if new_issue['project']['key'] == project.key:
            return True
    return False        
   
def CheckIssueSummary(new_issue,userId):
    project_key = new_issue['project']['key']
    issues_in_project = jira.search_issues("project = %s and assignee = %s" % (project_key, userId))
    issue_summary_list = []
    for issue in issues_in_project:
        issue_summary_list.append(issue.fields.summary)
    for issue_summary in issue_summary_list:
        if new_issue['summary'] == issue_summary:
            return True
    return False        

def CheckIssueType(new_issue):
    issuetype_list = ['Bug', 'Epic', 'Task', 'Story'] 
    #print(new_issue['issuetype']['name'])
    for issuetype in issuetype_list:
        #print(issuetype)
        if new_issue['issuetype']['name'] == issuetype:
            return True
    return False

def validateNewIssue(new_issue,userId):
    response = []
    if not CheckProjectKey(new_issue):
        response.append('Given project key does not exist! \n')
    
    if not CheckIssueType(new_issue):
        response.append('Given issuetype does not exist! Please choose from the following issuetypes: Bug, Epic, Task and Story \n')

    if not new_issue['summary']:
        response.append('Issue summary must not be empty! \n')
    else:
        if CheckProjectKey(new_issue):
            if CheckIssueSummary(new_issue,userId): 
                response.append('Issue with same name already exists! \n')

    if not new_issue['description']:
        response.append('Issue description must not be empty! \n')
    
    if not new_issue['customfield_10016'].isdigit():
        response.append('Task point estimate must be a positive integer only! \n')
    else: 
        if int(new_issue['customfield_10016']) not in range(1,11):
            response.append('Task point estimate can take values from 1 to 10 only! \n')

    return response

def sampleDBCall():
    cur = db.query("SELECT f FROM information_schema.tables WHERE table_schema='public'", None)
    #print('Tables :')
    tables = []
    for table in cur.fetchall():
        tables.append(table)
    return tables

def getValues(row,userid):
    x = np.reshape(row,(-1,8))
    x = np.transpose(x)
    plot(x,userid)

def plot(x,userid):
    df = pd.DataFrame(x, columns=["Mon","Tue","Wed","Thu","Fri"])
    ax=sns.heatmap(df,linewidths=1, linecolor='white', cmap="Greens", cbar=True, annot = False, vmin=0, vmax=1)
    bottom, top = ax.get_ylim()
    pos, textvals = plt.yticks()
    plt.yticks(pos, ('1', '2', '3', '4', '5', '6', '7','8'), rotation=0, fontsize="10", va="center")
    plt.ylabel("Sessions")
    ax.set_ylim(bottom , top)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    rel_path = '/ProgressGraph'
    abs_file_path = script_dir + rel_path + '/heat-map_{}.png'.format(userid)
    plt.savefig(abs_file_path)
    ShowProgressGraph(userid,abs_file_path)
    plt.close("all")
 
def GetDataFromDb(userid):
    weekNumber = getCurrentWeek()
    cursor = db.query("Select userid from focussession where userid = %s and weekid = %s",(userid,weekNumber))
    row_count = cursor.rowcount

    if row_count == 0:
       response = 'No current sprint exists!'
       slack_client.api_call("chat.postMessage", channel=slackEvent.get('channel'), text=response)
    else:    
        cur = db.query("Select cast(session1 as float), cast(session2 as float), cast(session3 as float),cast(session4 as float),cast(session5 as float),cast(session6 as float),cast(session7 as float),cast(session8 as float),cast(session9 as float),cast(session10 as float),cast(session11 as float),cast(session12 as float),cast(session13 as float),cast(session14 as float), cast(session15 as float),cast(session16 as float),cast(session17 as float),cast(session18 as float),cast(session19 as float),cast(session20 as float),cast(session21 as float), cast(session22 as float),cast(session23 as float),cast(session24 as float),cast(session25 as float),cast(session26 as float),cast(session27 as float),cast(session28 as float),cast(session29 as float), cast(session30 as float),cast(session31 as float),cast(session32 as float),cast(session33 as float),cast(session34 as float),cast(session35 as float),cast(session36 as float),cast(session37 as float),cast(session38 as float),cast(session39 as float),cast(session40 as float) from focussession where userid = %s and weekid = %s", (userid, weekNumber))
        row = cur.fetchall()
        getValues(row,userid)

def ShowProgressGraph(userid,path):
    channelId = slackEvent.get('channel')
    with open(path) as file_content: response = slack_client.api_call("files.upload", channels=[channelId],file=file_content, title="Weekly Progress Graph")
    


#@app.route('/focusbot1', methods=['POST', 'GET'])
def chalenge():
    r = Response(response=request.get_json().get('challenge'), status=200, mimetype="text/plain")
    r.headers["Content-Type"] = "text/plain"
    return r

#@app.route('/focusbot', methods=['POST', 'GET'])
def processMessage():
    # slack_event = request.get_json()
    # print(slack_event)

    # # ============= Slack URL Verification ============ #
    # # In order to verify the url of our endpoint, Slack will send a challenge
    # # token in a request and check for this token in the response our endpoint
    # # sends back.
    # #       For more info: https://api.slack.com/events/url_verification
    # if "challenge" in slack_event:
    #     return make_response(slack_event["challenge"], 200, {"content_type":
    #                                                         "application/json"
    #                                                         })
    global slackEvent
    slackEvent = request.get_json().get('event')

    type_of_event = slackEvent.get('type')
    text = slackEvent.get('text')
    # print(text)
    userID = slackEvent.get('user')

    # Describe commands
    if(tokens.get("focusBot") in text):

        if type_of_event == "message" and "describe commands" in text.lower() and userID != None:
            response = 'Command 1: List tasks\nParameters: None\nDescription: Returns all the issues that have status To Do or In Progress for the given user if it exists' + \
                       '\n\nCommand 2: Start task\nParameters: <task-name> <session-duration> <short-break-duration> <long-break-duration> <number-of-sessions>\nDescription: Starts the session corresponding to the given task if it exists. ' + \
                       'After the <session-duration>, bot recommends taking a short break for <short-break-duration>. After <number-of-sessions> sessions the bot recommends a long break for <long-break-duration>' +  \
                        '\n\nCommand 3: Create task\nParameters: <project-key> <issue-type> <issue-name> <issue-description> <number-of-points>\nDescription: Creates an issue on Jira using the given parameters if valid' + \
                       '\n\nCommand 4: Show progress \nParameters: None \nDescription: Returns the project report graph as a PNG for for the current sprint if active'
            slack_client.api_call("chat.postMessage", channel=slackEvent.get('channel'), text=response)
        # use case 1
        #happy path - list In progress and To Do tasks
        #sad path - No active sprint for the user

        if type_of_event == "message" and "list tasks" in text.lower() and userID != None:
            # response = getIssues(get_user(userID))
            in_progress_issues = jira.search_issues(
                "assignee=%s and status='In Progress'" % get_user(userID))
            response = []
            to_do_issues = jira.search_issues(
                "assignee=%s and status='To Do'" % get_user(userID))
            issues = in_progress_issues + to_do_issues
            print("ISSUES: "+str(len(issues)))
            if len(issues)!=0:
                for issue in issues:
                    response.append('Project: %s Issue : %s IssueID: %s Points: %s Status: %s \n' % (issue.fields.project.key, issue.fields.summary, issue.key, issue.fields.customfield_10027, issue.fields.status.name))

                response = "".join(response)
            else:
                response = "No Active Tasks exist!"
            slack_client.api_call("chat.postMessage", channel=slackEvent.get('channel'), text=response)

        # use case 2
        #happy path - create a task and send standard "Task created" response
        #sad path - Invalid Parameters
        #Eg: create task {project-key} {summary} {description} {task points}
        #Command : Create task <project-key> <issue-type> <issue-name> <issue-description> <number-of-points>
        elif type_of_event == "message" and "create task" in text.lower() and userID != None:
            params = text.split(" ")
            if len(params) < 8 :
                response = 'Insufficient number of parameters are given \n Error in creating an issue!'
            elif len(params) > 8:
                response = 'Too many parameters are given \n Error in creating an issue!'
            else:
                issue_dict = {
                    "project": {"key": str(params[3])},
                    "issuetype": {"name": (str(params[4])).title()},
                    "summary": str(params[5]),
                    "description": str(params[6]),
                    "customfield_10016": str(params[7]),
                    "customfield_10020": 1,
                    "customfield_10027": str(params[7]),
                    "assignee": {"name": get_user(userID)}
                }
                #issuetype={'name': 'Task'}
                #assignee={'name':'jcheruk'}
                #customfield_10016 = 4
                #customfield_10020=1
                # if IsValid_NewIssue(issue_dict):
                #     new_issue = jira.create_issue(fields = issue_dict) 
                #     response = 'Issue created'
                # else: 
                #     response = 'Error in creating an issue! Please check your parameters'
                response = validateNewIssue(issue_dict,get_user(userID))
                if not response:
                    issue_dict['customfield_10016'] = int(params[7])
                    issue_dict['customfield_10027'] = int(params[7])
                    new_issue = jira.create_issue(fields = issue_dict)
                    response.append('Issue created successfully!')
                else:
                    response.append('Error in creating an issue!')
                response = "".join(response)
            slack_client.api_call("chat.postMessage", channel=slackEvent.get('channel'), text=response)
            #new_issue_to_create = {
               # "summary": str(params[4]),
               # "description": str(params[5]),
               # "points": int(params[6]),
               # "project-key": str(params[3])
            #}
            #new_issue = createTask(new_issue_to_create)
            #slack_client.api_call("chat.postMessage", channel=slackEvent.get('channel'), text=new_issue)

        #use case 3
        #happy path - Start task and send updates every n seconds. Take break etc
        #sad path - Invalid Parameters
        # eg: Start Task {TaskId} {Session Time} {Short Break Time} {Long Break Time}
        elif type_of_event == "message" and "start task" in text.lower() and userID != None:
            cmd = text.split()[3:]
            user = get_user(userID)
            activetask = getFromUserMetadata(user, "activetask")
            if activetask != "-1":
                slack_client.api_call("chat.postMessage", channel=slackEvent.get('channel'), text="You already have an active pomodoro task")
            else:
                req = {}
                req["user_name"] = user
                req["channel_id"] = slackEvent.get('channel')
                req["params"] = cmd
                #putToUserMetadata(user, "activetask", cmd[0])

                t = threading.Thread(target=pomodoro_task, args=(req,))
                t.start()
                # print(cmd)
                # print(request.get_json())

        # elif type_of_event == "message" and "start task" in text.lower() and userID != None:
        #     t = threading.Thread(target=startTask,args=(text , ))
        #     t.start()
            

        #use case 4 - Show Progress
        #happy path - Show a picture
        #sad path - No active sprint/ no tasks

        elif type_of_event == "message" and "show progress" in text.lower() and userID != None:
            #t = threading.Thread(target=getProgress, args=(get_user(userID) , ))
            t = threading.Thread(target=GetDataFromDb, args=(get_user(userID) , ))
            t.start()
            
        
    r = Response(response=request.get_json().get('challenge'), status=200, mimetype="text/plain")
    r.headers["Content-Type"] = "text/plain"
    return r


#Lets make this function dynamic - to fetch active task and start epoch
def getFromUserMetadata(user, column):
    #usermetadata
    print("column: " + column)
    query = 'SELECT '+column+' FROM usermetadata WHERE userid = %s'
    print("query")
    print(query)
    result = db.query(query, (user,))
    return result.fetchone()[0]

def putToUserMetadata(user, column, columnValue):
    print(user+" :"+ str(column)+" :"+ str(columnValue))
    result = db.query("Update usermetadata set "+column+" = %s where userid = %s", (columnValue, user))
    db.conn.commit()
    return True

#convered in updateStatus
def get_task_points_from_jira(task):
    return 2

def put_session_percentage_to_db(user, week, session, val):
    print(session)
    col = "Session"+str(session)
    
        
    cur = db.query("SELECT "+col+" FROM focussession WHERE userid = %s and weekid = %s", (user, week))
    out = cur.fetchone()
    val = val/100
    if out is  None:
  
        output= cur.execute("INSERT INTO focussession VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
            (user, week, 0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00))
        
        db.conn.commit()
    else:
        print(out)
        val=val+float(out[0])

    output = db.query("Update focussession set "+col+" = %s where userid = %s and weekid = %s ",(round(val,2), user, week))
    db.conn.commit()
            #print output output.fetchone()

    return True

#covered all these cases in updateStatus - check onve.
def put_task_percentage_to_jira(task, val, table):
    #Also close the task if 100%
    #closeIssue(task)
    pass

def submit_button_task(data):
    # print(data)
    if data["actions"][0]["type"] == "button":  # stop task
        putToUserMetadata(data["user"]["username"], "activeTask", "-1")
        slack_client.api_call("chat.postMessage", channel=data["container"]["channel_id"], text="Stopping the Task!")
        #return "True"
    else:
        print("AFTER BUTTON")
        user = data["user"]["username"]
        task, epoch, duration = (data["actions"][0]["placeholder"]["text"]).split()
        # points = get_task_points_from_jira(task) ##get total points for that session
        percent = int(data["actions"][0]["selected_option"]["text"]["text"])
        points = updateTaskStatus(percent, task)
        if points == -1:
            slack_client.api_call("chat.postMessage", channel=data["container"]["channel_id"],
                                  text="Error! Invalid Input! Please enter a proper value!")
            #return "True"

        if percent == 100:
            print("100")
            putToUserMetadata(data["user"]["username"], "activeTask", "-1")
            #return "True"

        print("POINTS COMPLETED " + str(points))
        curr_datetime = time.localtime(int(epoch))

        # get epoch from DB
        day = curr_datetime.tm_wday-1  # 0 to 6
        if day > 4:
            return
        # print("day:" + str(day) + " epoch: " + str(epoch))
        col = '"'
        col += getCurrentDay() + '"'
        start = getFromUserMetadata(user, col)
        # print("start :" + str(start))
        # print("VAL: "+str(int(epoch) - start ))

        if start == 0 or ((int(epoch) - start) > (3600 * 24)):
            print("CHANGE START TIME")
            start = int(epoch)
            putToUserMetadata(user, col, int(epoch))

        sess = math.floor((int(epoch) - start) / 3600) + 1  # check for more than 8 sessions


        if sess > 8: #Float cases ?
            return

        epoch = int(epoch)
        duration = float(duration)
        total_duration = duration
        rem = min([(sess + 1) * 3600 + start - epoch, duration])

        while duration != 0 and sess <= 8:
            session_percent = ((rem / total_duration) * points) * 200
            session = int(day * 8 + sess)
            print("UPDATING FOCUS SESSION : ")
            put_session_percentage_to_db(user, getCurrentWeek(), session, session_percent)

            epoch += rem
            sess += 1
            duration -= rem
            rem = min([(sess + 1) * 3600 + start - epoch, duration])


@app.route('/submit_button', methods=['POST', 'GET'])
def submit_button():
    #pdb.set_trace()
    data = json.loads(request.form["payload"])
    t = threading.Thread(target=submit_button_task, args=(data,))
    t.start()

    r = Response(status=200, mimetype="text/plain")
    r.headers["Content-Type"] = "text/plain"
    return r

def validateStartTask(params, user):
    response = ''
    flag = True
    if len(params) != 5:
        response += 'Exactly 5 parameters required. Provided %d parameters. ' % len(params)
        flag = False
    else:
        try:
            issue = jira.issue(params[0])
            if str(user) != str(issue.fields.assignee):
                response += 'The entered task is not assigned to you. '
                flag = False
            if str(issue.fields.status) == 'Done':
                response += 'The entered task is already Done. '
                flag = False

            session_time = None
            short_break = None
            long_break = None
            num_sessions = None

            try:
                session_time = float(params[1])
                if session_time < 0:
                    flag = False
                    response += 'Session time cannot be a negative number. '
            except:
                flag = False
                response += 'Session time should be valid number - float is allowed. '

            try:
                short_break = float(params[2])
                if short_break < 0:
                    flag = False
                    response += 'Short break cannot be a negative number. '
            except:
                flag = False
                response += 'Short break should be a valid positive number - float is allowed. '
            try:
                long_break = float(params[3])
                if long_break < 0:
                    flag = False
                    response += 'Long break cannot be a negative number. '
            except:
                flag = False
                response += 'Long break should be a valid positive number - float is allowed. '
            try:
                num_sessions = int(params[4])
                if num_sessions < 0:
                    flag = False
                    response += 'Number of sessions cannot be a negative number. '
            except:
                flag = False
                response += 'Number of sessions should be a valid positive number - Only integer allowed. '

            if short_break != None and long_break != None and short_break > long_break:
                response += 'The short break time should be lesser than long break time. '
                flag = False
            if short_break != None and session_time != None and short_break > session_time:
                response += 'The short break time should be lesser than session time. '
                flag = False
            if num_sessions != None and session_time != None and session_time * num_sessions > (issue.fields.customfield_10016 * 2 * 60 + 30):
                response += 'You are asking for more time than permitted. Available only %d minutes for this task. ' % math.floor(issue.fields.customfield_10016 * 2 * 60 + 30)
                flag = False
        except:
            response += 'Invalid task ID. '
            flag = False

        # for p in params[1:]:
        #     if not p.isdigit():
        #         response += 'All parameters following task ID are expected to be numbers. '
        #         flag = False
        #         break
    if not flag:
        response = 'Invalid Input! ' + response

    return flag, response



def pomodoro_task(cmd):
    params = cmd["params"]
    # print(params)
    user = cmd['user_name']
    flag, response = validateStartTask(params, user)
    if not flag:
        slack_client.api_call("chat.postMessage", channel=cmd['channel_id'], text=response)
        return 
    changeTaskStatus(params[0])
    putToUserMetadata(user, "activetask", params[0])
    op = []
    for percent in range(1, 101):
        text_d = dict()
        text_d["type"] = "plain_text"
        text_d["text"] = str(percent)
        op.append({"text": text_d, "value": "value-" + str(percent)})

    for session in range(int(params[-1])):
        #Get the percentage completed from JIRA for the given issue
        #If it's 100% return
        activetask = getFromUserMetadata(user, "activetask")
        print(activetask)
        if activetask == "-1":
            return
        slack_client.api_call("chat.postMessage", channel=cmd["channel_id"], text="Start your task, session " + str(session+1))
        start = time.time()

        #Task in progress
        # print(params[1])
        # print(type(params[1]))
        # print('Session time is : ' + params[1] + str(type(params[1])))
        time.sleep(float(params[1])*60)
        slack_client.api_call("chat.postMessage", channel=cmd["channel_id"], text="Session over")
        response = 'Enter the percentage completed'
        json_blocks = [
            {
                "type": "section",
                "block_id": "section678",
                "text": {
                    "type": "mrkdwn",
                    "text": "Enter percentage completed"
                },
                "accessory": {
                    "action_id": "text1234",
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": params[0] + " " + str(int(start)) + " " + str(float(params[1])*60)
                    },
                    "options": op
                }
            }
        ]
        slack_client.api_call("chat.postMessage", channel=cmd['channel_id'], text=response, blocks=json_blocks)
        json_blocks = [ {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Stop Task",
                            "emoji": False
                        }
                    }
                ]
            }]

        slack_client.api_call("chat.postMessage", channel=cmd['channel_id'], text=response, blocks=json_blocks)
        time.sleep(20)
        activetask = getFromUserMetadata(user, "activetask")
        #print(activetask)
        if activetask == "-1" or session == (int(params[-1])-1):
            break
        slack_client.api_call("chat.postMessage", channel=cmd["channel_id"], text="Time to take a short break")
        time.sleep(float(params[2])*60)
        slack_client.api_call("chat.postMessage", channel=cmd["channel_id"], text="Short break over")

    putToUserMetadata(user, "activeTask", "-1")
    slack_client.api_call("chat.postMessage", channel=cmd["channel_id"], text="Time to take a long break")
    time.sleep(float(params[-2])*60)
    slack_client.api_call("chat.postMessage", channel=cmd["channel_id"], text="Long break over")




# @app.route('/start_task', methods=['POST', 'GET'])
# def pomodoro_start():
#     print('here')
#     t = threading.Thread(target=pomodoro_task, args=(request.form,))
#     t.start()
#     r = Response(status=200, mimetype="text/plain")
#     r.headers["Content-Type"] = "text/plain"
#     return r



@app.route('/', methods=['POST','GET'])
def hello():
    return "hello"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
