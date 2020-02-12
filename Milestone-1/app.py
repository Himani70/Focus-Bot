from flask import Flask, url_for, request
from flask import Response, make_response
from slackclient import SlackClient
import json
import requests
import threading
import os
import time
from mock import patch, MagicMock
from jira import JIRA


app = Flask(__name__)

tokens = {}
with open('configs.json') as json_data:
    tokens = json.load(json_data)

slackEvent = None
slack_client = SlackClient(tokens.get("slack_bot_token"))
jira = JIRA(basic_auth=(tokens.get("userId"), tokens.get("userToken")),
                    options={'server': tokens.get("serverEndPoint")})

def readJson(filename):
    with open(filename) as file:
       return(json.load(file))

def mock_responses(responses, default_response=None):
  return lambda input: responses[input] if input in responses else default_response


def get_user(user_id):
    payload = {'token': tokens.get("slack_bot_token"), 'user': user_id}
    r = requests.get('https://slack.com/api/users.info', params=payload)
    res = json.loads(r.text)
    return res['user']['name']

def mock_startTask(responses, isValid, slackEvent):
    if isValid==True:
        slack_client.api_call("chat.postMessage", channel=slackEvent.get('channel'), text="Start working on your task.")
        time.sleep(10)
        slack_client.api_call("chat.postMessage", channel=slackEvent.get('channel'), text="Great Work! Time for a short break.")
        time.sleep(5)
        slack_client.api_call("chat.postMessage", channel=slackEvent.get('channel'), text="Resume working on the task. You got this")
        
    elif isValid==False:
        slack_client.api_call("chat.postMessage", channel=slackEvent.get('channel'), text="Invalid Parameters! Please check your command.")

    return True


def startTask(command):
    isValid = True
    mockStartTask = MagicMock(side_effect = mock_startTask)
    params = command.split(" ")
    print("params :", len(params))
    if len(params)!=8:
        isValid = False
    else:
        sessionTime = params[4]
        shortBreakTime = params[5]
        longBreakTime = params[6]
        numberofSessions = params[7]
        if((str(sessionTime).isdigit() and str(shortBreakTime).isdigit() and str(longBreakTime).isdigit() and str(numberofSessions).isdigit())==False):
            isValid = False
        
    return mockStartTask(readJson("mock/issues.json"), isValid, slackEvent)

def getIssues(assignee):
    my_mock = MagicMock()
    mock_json = readJson('mock/issues.json')

    d = {}
    for user in mock_json['users']:
        if not mock_json['users'][user].get('issues'):
            continue
        result = ''
        for issue in mock_json['users'][user]['issues']:
            if mock_json['users'][user]['issues'][issue]['status'] == 'Done':
                continue
            result += issue + '\n'
            for field, value in mock_json['users'][user]['issues'][issue].items():
                result += field + ' : ' + str(value) + '\n'
            result += '\n'

        if result != '':
            d[user] = result
    my_mock.foo.side_effect = mock_responses(d, default_response='No active issues exist')
    return my_mock.foo(assignee)

def checkCreateTask(new_issue_to_create):
    if (isinstance(new_issue_to_create['summary'],str) and isinstance(new_issue_to_create['description'],str) ):
        if ( isinstance(new_issue_to_create['points'],int) and new_issue_to_create['points'] in range(1,11)):
            if (new_issue_to_create['project-key'] in readJson('mock/projects.json')['projects']):
                print("project")
                return True
    return False

def createTask(new_issue_to_create):
    my_mock = MagicMock()
    valid = checkCreateTask(new_issue_to_create)
    my_mock.foo.side_effect = mock_responses({True: 'Issue Created'},default_response='Error in creating an issue! Please check your parameters.')
    return my_mock.foo(valid)

def getProgress(assignee):
  dictionary = readJson('mock/issues.json')
  result= {}

  for user in dictionary['users']: 
    if dictionary['users'][user].get('active_sprint'):
      result[user] = True
        
  my_mock = MagicMock()
  my_mock.foo.side_effect = mock_responses(result, default_response = 'Active sprint does not exist!')
  
  return sendProgressGraph(my_mock.foo(assignee))

def sendProgressGraph(status):
    channelId = slackEvent.get('channel')
    if status!=True:
        slack_client.api_call("chat.postMessage", channel=channelId, text=status)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        rel_path = "/mock/heat-map.png"
        abs_file_path = script_dir+rel_path  
        with open(abs_file_path) as file_content:
            response = slack_client.api_call(
                "files.upload",
                channels=[channelId],
                file=file_content,
                title="Weeekly Progress Graph"
        )
    return True


@app.route('/sample-event', methods=['POST', 'GET'])
def test_sample_event():

    global slackEvent
    slackEvent = request.get_json().get('event')

    type_of_event = slackEvent.get('type')
    text = slackEvent.get('text')

    userID = slackEvent.get('user')

    # Describe commands
    if(tokens.get("focusBot") in text):
        if type_of_event == "message" and "describe commands" in text.lower() and userID != None:
            response = 'Command 1: List tasks\nParameters: None\nDescription: Returns all the issues that have status To Do or In Progress for the given user if it exists' + \
                       '\n\nCommand 2: Start task\nParameters: <task-name> <session-duration> <short-break-duration> <long-break-duration> <number-of-sessions>\nDescription: Starts the session corresponding to the given task if it exists. ' + \
                       'After the <session-duration>, bot recommends taking a short break for <short-break-duration>. After <number-of-sessions> sessions the bot recommends a long break for <long-break-duration>' +  \
                        '\n\nCommand 3: Create task\nParameters: <project-key> <issue-name> <issue-description> <number-of-points>\nDescription: Creates an issue on Jira using the given parameters if valid' + \
                       '\n\nCommand 4: Show progress \nParameters: None \nDescription: Returns the project report graph as a PNG for for the current sprint if active'
            slack_client.api_call("chat.postMessage", channel=slackEvent.get('channel'), text=response)
        # use case 1
        #happy path - list In progress and To Do tasks
        #sad path - No active sprint for the user
        if type_of_event == "message" and "list tasks" in text.lower() and userID != None:
            response = getIssues(get_user(userID))
            slack_client.api_call("chat.postMessage", channel=slackEvent.get('channel'), text=response)

        # use case 2
        #happy path - create a task and send standard "Task created" response
        #sad path - Invalid Parameters
        #Eg: create task {project-key} {summary} {description} {task points}
        elif type_of_event == "message" and "create task" in text.lower() and userID != None:
            params = text.split(" ")
            new_issue_to_create = {
                "summary": str(params[4]),
                "description": str(params[5]),
                "points": int(params[6]),
                "project-key": str(params[3])
            }
            new_issue = createTask(new_issue_to_create)
            slack_client.api_call("chat.postMessage", channel=slackEvent.get('channel'), text=new_issue)

        #use case 3
        #happy path - Start task and send updates every n seconds. Take break etc
        #sad path - Invalid Parameters
        # eg: Start Task {TaskId} {Session Time} {Short Break Time} {Long Break Time}
        elif type_of_event == "message" and "start task" in text.lower() and userID != None:
            t = threading.Thread(target=startTask,args=(text , ))
            t.start()
            

        #use case 4 - Show Progress
        #happy path - Show a picture
        #sad path - No active sprint/ no tasks
        elif type_of_event == "message" and "show progress" in text.lower() and userID != None:
            t = threading.Thread(target=getProgress, args=(get_user(userID) , ))
            t.start()
        
    r = Response(response=request.get_json().get('challenge'), status=200, mimetype="text/plain")
    r.headers["Content-Type"] = "text/plain"
    return r



@app.route('/', methods=['POST'])
def hello():
    return "hello"

if __name__ == '__main__':
    app.run()