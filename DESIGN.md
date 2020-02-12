## Table of contents
* [Problem Statement](#problem-statement)
* [Bot Description](#bot-description)
* [Use Cases](#use-cases)
* [Design Sketches](#design-sketches)
* [Architecture Design](#architecture-design)
* [Design Patterns](#design-patterns)

# Problem Statement
Tasks and To-Dos are like bread and butter for any software engineer. Often times a lot of tasks pile up at once, especially when there is some production issue or a build failure. And the engineer is suddenly overwhelmed with a bunch of fresh tasks competing for some space in his/her already long to-do list. There is also a high chance the deadlines overlap or the individuals lose track of the deadlines of their tasks. The best way to handle these kind of situations is to approach the tasks systematically, decide on a schedule to complete all the tasks on time and keep track of the progress. In this project we propose to build a bot that assists software engineers to efficiently expend time and effort and in turn maximize the productivity.
<br />
<br />
As most of us are interested in the actual numbers, the bot would generate burndown charts to graphically represent work left to do in a project. Using these visual tools, the engineer can observe his/her progress over time and can plan his day accordingly. 


# Bot Description
The FocusBot that we are building helps users to track and manage the tasks he/she is responsible for and improve productivity. All the users can create customized tasks. They use pomodoro technique to perform the task. When the user starts a task, the pomodoro timer will automatically start and will notify the user when the session time completes to take a short break. If the user completes four continuous pomodoro sessions, then the bot notifies the user to take a long-break. The user can customize the pomodoro session time, long-break and short-break times before he/she starts a task. He can also switch to Do Not Disturb mode on request. After each pomodoro session, the user has to update the status of the task. When the user completes the task, he/she can end the task. The bot daily notifies the personal progress of the user in the form of burndown charts and if the user wants to check his/her personal progress, he/she can do so by requesting the bot and the bot will display the burndown charts.<br /><br />
For team tasks, team members will be assigned tasks and each team member uses pomodoro technique to be more productive while performing their individual tasks and can update the status of the task. The team members can see the team progress as well as their personal progress by checking the burndown charts. As the task deadline approaches, bot notifies the whole team about the team members lagging behind the completion of the task. 

### Why your bot is good solution for the problem ?

- It helps in managing distractions and maintaining better awareness of the time.
- The pomodoro technique helps in improving the task planning and also eliminates burnouts.
- It can also help the user to be more accountable by showing his personal and team progress everyday.
- Burndown charts give a better visualisation of how focussed the team/ team member is rather than just messages and also helps us to know how much time is being spent productively.
- It can work like a virtual scrum at task level.

### Tagline:
Work while you work, play while you play

# Use Cases
## Use Case 1: List open tasks assigned to specific user
```
1. Preconditions
User must have Jira and bot API tokens in the system
Jira must be integrated with the bot
2. Main Flow
   User will request list of open tasks assigned to him/her [S1]. Bot will return the list of tasks along with it's details [S2]. 
3. Subflows
  [S1] User will request list of open tasks assigned to him/her
  [S2] Bot will return the list of tasks along with it's details
4. Alternative Flows
  [E1] No open tasks available for the specific user
```
## Use Case 2: Set Pomodoros for the user’s tasks
```
1. Preconditions
User must have Jira and bot API tokens in the system
Jira must be integrated with the bot
2. Main Flow
   User will request to start a task [S1]. Bot will ask the user if he wants to use the default pomodoro settings or customize it [S2]. Bot will send the format required to customize the pomodoro settings [S3]. Bot will ask the user to update the status of the task and take a break after every session [S4]. Bot will change the status to Closed after 100% completion of the task [S5]. 
3. Subflows
  [S1] User will request to start a task.
  [S2] Bot will ask the user if he wants to use the default pomodoro settings or customize it.
  [S3] Bot will send the format required to customize the pomodoro settings.
  [S4] Bot will ask the user to update the status of the task and take a break after every session.
  [S5] Bot will change the status to Closed after 100% completion of the task.
4. Alternative Flows
  [E1] No open tasks available for the specific user
```
## Use Case 3:  Create custom tasks
```
1. Preconditions
User must have Jira and bot API tokens in the system
Jira must be integrated with the bot
2. Main Flow
   User will request to create custom task  [S1]. Bot will ask for details in the format Name-Description-Points [S2]. Bot will create a new open task with the given details [S3].
3. Subflows
  [S1] User will request to create custom task
  [S2] Bot will ask for details in the format Name-Description-Points
  [S3]  Bot will create a new open task with the given details
4. Alternative Flows
  [E1] User enters task details in an invalid format or values (eg negative values for points)
```
## Use Case 4: Check the progress
```
1. Preconditions
User must have Jira and bot API tokens in the system
Jira must be integrated with the bot
2. Main Flow
     User requests the bot to View progress [S1]. Bot returns with options of Team progress  or Personal progress [S2]. User selects the specific progress which he wants to view [S3]. Bot displays the specific progress in the form of burndown chart [S4].
3. Subflows
  [S1] User provides the command to View progress
  [S2] Bot returns with the two options Team progress and Personal progress
  [S3] User will select one of the options
  [S4] Bot displays the selected progress in the form of burndown chart 
4. Alternative Flows
  [E1] No open tasks available for the specific user
```
## Use Case 5: Send Notifications
```
1. Preconditions
User must have Jira and bot API tokens in the system
Jira must be integrated with the bot
2. Main Flow
    Bot automatically sends the user’s progress at a certain time everyday as a notification to the user [S1].  As the task deadline approaches, bot sends notifications to all the team members if any team member is lagging behind the expected percentage of task completion [S2] 
3. Subflows
  [S1] Bot automatically sends the user’s progress in the form of burn down charts at a certain time as a notification daily to the user. 
  [S2]  As the task deadline approaches, bot sends notifications to all the team members specifying the percentage of task that a team member has to complete if that team member is lagging behind the expected percentage of task completion. 
4. Alternative Flows
[E1] No open tasks available for the specific user
```
# Design Sketches:

## Storyboard

#### 1. List open tasks assigned to specific user
![listTasks](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/images/storyboard-1-listTasks.png)

#### 2.Set Pomodoros for the user’s tasks

###### 2.1 Start Task
![startTask](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/images/storyboard-2-startTask.png)

###### 2.2 Customise Pomodoro
![customisePomodoro](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/images/storyboard-2-customisePomodoro.png)

###### 2.3 Update the status of the task and take a break after every session
![taskStatus](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/images/storyboard-2-taskStatus.png)

#### 3. Create custom tasks
![createTask](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/images/storyboard-3-createTask.png)

#### 4. Check the progress
![checkProgress](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/images/storyboard-4-showProgress.png)

#### 5. Send notifications

###### 5.1 Scheduled Personal notifications
![notifications1](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/images/storyboard-5-scheduledPersonal.png)

###### 5.2  Scheduled Team Deadline
![notifications2](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/images/storyboard-5-teamDeadline.png)

## Wireframes

#### 1. List Tasks
![listTasks](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/images/ListTasks.png)

#### 2.Set Pomodoros for the user’s tasks

###### 2.1 Customised Promodoro
![customizedPomodoro](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/images/CustomizedPomodoro.png)

###### 2.2 Default Pomodoro
![defaultPomodoro](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/images/DefaultPomodoro.png)

###### 2.3 Update the status of the task and take a break after every session
![taskStatus](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/images/SessionBreak.png)


###### 2.4 Finish Task
![finishTask](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/images/FinishTask.png)

#### 3. Create custom tasks
![createTask](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/images/CreateTask.png)

#### 4. Check the progress
![checkProgress](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/images/ShowMyProgress.png)

#### 5. Send notifications

###### 5.1 Scheduled Personal notifications
![notifications1](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/images/DailyProgressNotification.png)

###### 5.2  Scheduled Team Deadline
![notifications2](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/images/DeadlineWarning.png)

# Architecture Design
## Architecture Diagram and component details:
![Image of architecture design](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/images/FocusBotArchitecture.jpg)

<br /> Note: All HTTP requests and response exchange JSON <br />
## Components
### Slackbot
Slack is used as an interface for the user to interact with the bot. User can view the available commands by @ the bot.
### Server
The application will be connected to the slack workspace using the Slack RTM API. The Server communicates with the slack to receive input, handles the database communication and also talks to JIRA via REST calls.
### Database
The information regarding the slack users and the corresponding JIRA users, task related information will be stored in the database. It can be very useful when the functionalities of the bot are extended.
### JIRA
The server makes calls via JIRA Agile REST API to get task related information. The API sends response to server which is subsequently used to send response back to the user's query
## Architecture constraints and guidelines:
The following are the constraints of the bot:- 
1. It is assumed that the token required for accessing JIRA and Slack are generated and persisted in the Database/ hardcoded in the code.
2. The bot only handles the use cases mentioned in the Design and might not fail gracefully for other cases.
3. The bot expects the conversation to be either the commands that it supports or the ones that the bot asks the user to choose.
4. JIRA: There should be a team with an active Sprint cycle.
# Design patterns
1. **Factory Pattern:** Used to create objects for tasks,users etc.
2. **Scheduled Task pattern:** Used to implement pomodoros as we set a timer to complete task and the system delays asking the user to take a break until the timer ends.
3. **Mediator Pattern:** Our bot encapsulates how the user and Jira task objects interact. As and when the user requests to create, view, update tasks the bot handles it for the user. 
4. **Facade Pattern:** The bot acts as a facade to mask the complex task management done on Jira.
5. **Interpreter Pattern:** Used to interpret the user's query and perform the relevant action.
## Additional Pattern
We will be using the Pipe and Filter Architecture pattern for our TaskFocus bot. Since, our data flows from Slack to Jira through different components in between and simulates stream processing of data, we believe Pipe and Filter architecture will be the most suitable pattern for our bot.


