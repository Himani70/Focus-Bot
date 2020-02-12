## Table of contents
* [Bot Platform Implementation](#bot-platform-implementation)
* [Use Cases Refinement](#use-cases-refinement)
* [Mocking Infrastructure](#mocking-infrastructure)
* [Puppeteer Testing of each use case](#puppeteer-testing-of-each-use-case)
* [Screencast](#screencast)

# Bot Platform Implementation

Our bot known as FocusBot is integrated with Slack. 

Users can add the bot and view the available commands by "@FocusBot Show commands".

All the commands given to the bot should be made by calling @FocusBot <Command>

# Use Cases Refinement

## Refinement:
  
  1. Showing progress graphs instead of burndown charts to represent focus sessions.
  2. Removed Notification Use case as we have switched from burndown charts to progress graph. 
  
## Updated Use Cases:

## Use Case 1: List open tasks assigned to specific user
```
1. Preconditions
User must have Jira and bot API tokens in the system
2. Main Flow
   User will request list of open tasks assigned to him/her [S1]. Bot will return the list of tasks along with it's details [S2]. 
3. Subflows
  [S1] User will request list of open tasks assigned to him/her
  [S2] Bot will return the list of tasks along with it's details
4. Alternative Flows
  [E1] No open tasks/active sprints available for the specific user
```

## Use Case 2:  Create custom tasks
```
1. Preconditions
User must have Jira and bot API tokens in the system
2. Main Flow
   User will request to create custom task using the command create task [S1]. Bot will create a new open task with the given details [S2].
3. Subflows
  [S1] User will request to create custom task using the command create task {Summary} {Description} {Points} {Project-key}
  [S2] Bot will create a new open task with the given details
4. Alternative Flows
  [E1] User enters task details in an invalid format or values (eg:negative values for points)
```

## Use Case 3: Set Pomodoros for the user’s tasks
```
1. Preconditions
User must have Jira and bot API tokens in the system
2. Main Flow
   User will request to start a task using the command Start Task [S1]. Bot will ask the user to update the status of the task and take a break after every session [S4]. Bot will change the status to Closed after 100% completion of the task [S5]. 
3. Subflows
  [S1] User will request to start a task using the command Start Task {TaskId} {Session Time} {Short Break Time} {Long Break Time}
  [S4] Bot will ask the user to update the status of the task and take a break after every session.
  [S5] Bot will change the status to Closed after 100% completion of the task.
4. Alternative Flows
  [E1] No open tasks available for the specific user or the user enters an invalid command
```

## Use Case 4: Check the progress
```
1. Preconditions
User must have Jira and bot API tokens in the system
2. Main Flow
   User requests the bot to show progress [S1]. Bot displays the user's progress in the form of heatmap [S2].
3. Subflows
  [S1] User requests the bot to show progress using the command Show Progress
  [S2] Bot displays the user's progress in the form of heatmap 
4. Alternative Flows
  [E1] No open tasks/active sprints available for the specific user 
```

# Mocking Infrastructure

Mock data used can be found [here](https://github.ncsu.edu/csc510-fall2019/CSC510-3/tree/master/Milestone-1/mock). 
Our bot mocks all the API calls to Jira and Database thus retrieving the necessary data from the mock files.

## Explanation

For Use case 1, we have a mock data for two users. The user Jagan (jcheruk) has two issues and an active sprint. The user Priyankha (pbhalas) does not have an active sprint.

For Use case 2, we are showing one session - short break - resuming task (next session) for the happy path to keep the screencaset brief. This is just a gist of how the functionality will be implemented. 

Usually, it will be

```
Session
Loop (No. of Sessions-1)
   Short Break
   Session
Long Break
Session
```
and continues like this

For Use case 3, we are mocking the creation of a new task and the related database calls. This returns Issue created if the parameters are valid.

For Use case 4, we are returning a sample progress graph representing the weekly focus sessions for a valid user with active sprint and tasks.

# Puppeteer Testing of each use case

Puppeteer testing files can be found [here](https://github.ncsu.edu/csc510-fall2019/CSC510-3/tree/master/integration-testing)

For Use cases 1 and 4, we are showing sad paths from a different user account since our use cases are attached to the user. 

 ## Use Case 1
 1. Happy Path: Lists To Do and In Progress tasks and their details
 2. Sad Path: No active sprint exists for the user
 
 ## Use Case 2
 1. Happy Path: Creates task and sends the response "Issue Created"
 2. Sad Path: Invalid parameters are given and the bot responds as "Error in creating an issue! Please check the parameters."
 
 ## Use Case 3
 1. Happy Path: Starts task and sends update every n seconds to take short/long break depending on the user's configuration while starting the task.
 2. Sad Path: Invalid parameters are given and bot responds as "Invalid Parameters! Please check your command."
 
 ## Use Case 4
 1. Happy Path: Shows progress graphs
 2. Sad Path: No active sprint/tasks exists for the user

# Screencast

Find the link to our screencast [here](https://drive.google.com/file/d/1c0HmPwjlGJhutx8Q9MUbTzvd1fP14kcD/view?usp=sharing)
 
# Task Tracking

We have made use of Trello for tracking individual tasks. Everyone is involved in all the tasks for individual use cases.

[Trello cards](https://trello.com/focusbot) 
   

# Table Structure

https://docs.google.com/document/d/1g2WQe-VcyMzfuMOmGrj-xd1hQrLlaGVSXJAgdG48srg/edit?ts=5db3c755

