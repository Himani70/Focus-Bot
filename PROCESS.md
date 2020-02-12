## Process

Initially, we started with task for the 4 use cases. We assigned 20 points for each of us for the entire milestone. 10 for each iteration. We also had assigned 4 buffer points for the time spent on helping others, meetings, extra time spent on the task incase of difficulties faced during implementation etc.  We made use of the Kanban board and assigned all the task at the beginning of the first iteration. 

We designed the tasks using the SMART approach. Every use case was assigned as task(s) depending on the complexity and achievability. We planned in such a way that the dependent tasks are completed first. So, the priority was given for the tasks which will be useful for other tasks. Meanwhile, independent tasks were assigned to an user. 

In our case, Use case 1 ( List tasks ) , Use case 2 ( Create task ) were dependent on JIRA and was assigned independently. The Use case 3 ( Start task ) and Use case 4 (  show progress ) are dependent on the database. So, the database setup task was completed in the first iteration. The schema design of the database was discussed with the team and got approval of everyone so that it can accommodate all the use cases and also scalable. The Use cases 3 and 4 were completed in the second iteration. Since the Use cases 3 and 4 involved multiple aspects, they were subdivided into separate tasks which were worked on independently. By following the SMART approach, we were able to achieve the desired results and complete the tasks on time. It helped us mitigate the dependency task issues. 
Below is a series of images representing the progress of the tasks.

#### SPRINT  1 ( Oct 23-- Fri Nov 1)

This was the initial phase, just after the tasks were discussed, created and assigned.
![stage1](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/Milestone-2/kanban%20board/1.png)

This was after completing two use cases and other tasks were in progress.
![stage2](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/Milestone-2/kanban%20board/2.png)

This was after completing setting up the Database task.
![stage3](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/Milestone-2/kanban%20board/3.png)

This was at the end of Sprint 1. We had completed 3 tasks and were actively working on the other tasks. We had also added Unit Test cases task for the next milestone.
![stage4](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/Milestone-2/kanban%20board/4.png)

#### SPRINT 2 ( Nov 2--Fri Nov 8th)

After completing the Show Progress task
![stage5](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/Milestone-2/kanban%20board/5.png)

After making progress on the Use case 3 Task
![stage6](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/Milestone-2/kanban%20board/6.png)

The two images below depict the progress of Sprint 2. We have assigned a new task for Process.md. It is for fine tuning the documentation and everyone is involved in the task.
![stage7](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/Milestone-2/kanban%20board/7.png)

Final board 
![stage8](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/Milestone-2/kanban%20board/8.png)


## Practices

###### Scrumban

We used the scrumban methodology throughout this iteration. As the name suggests the scrumban methodology incorporates both Scrum and Kanban practices. In this section we would summarize how we used this Scrumban technique

###### Scrum Practices

- We had 2 sprints to ensure we plan and execute work in regular intervals.
- The work was executed on a priority basis. Some tasks like DB setup and connection establishment were prerequisites for some use-cases like pomodoro logic. So the prerequisite tasks were given extra priority and completed early in the sprint.
- We had targeted goals and a dedicated number of points to be completed for each sprint. This was divided equally amongst the team members. Everyone executed their tasks on time and the code was further reviewed by the peers. Feedbacks were gathered and changes were updated on a timely basis.
- We had regular scrum meetings across the two sprints, where we discussed agenda, daily plan, refined/added use cases. You can access our meeting minutes [here](https://github.ncsu.edu/csc510-fall2019/CSC510-3/tree/master/Milestone-2/MeetingNotes)

###### Kanban Practices

- We had a dedicated project board on Github with columns like ToDo, In Progress and Done. You would find additional columns Sprint 1 progress and Sprint 2 progress, to clearly demarcate the targeted tasks that were completed in Sprint 1 and Sprint 2. You can take a look at our Kanban board [here](https://github.ncsu.edu/csc510-fall2019/CSC510-3/projects/2)
- The Kanban board acted as a visual workflow management that highlights tasks/stories as cards. Each card has a task title, optional description, number of story points and assignees. We iteratively kept updating the number of pending points left to complete as we progressed.
- We ensured that we do not have too many tasks in progress at the same time as strongly recommended as a part of Kanban practices.
- The visual segregation helped us identify our weaknesses and issues to improve. For example, the stories that have been on ToDo for quite some time were addressed and acted upon.

###### Agile practices

- We followed Agile process throughout our development this time. 
- We had an iterative approach where we chose a set of features/tasks and implemented them to completion in every iteration. 
- At the end of every iteration, we reviewed the code and refined them in the next iteration. 
- This allowed us to be very flexible with the scope of our use cases because Agile is the best model for changing requirements. 

###### Peer Reviews

An essential part of the software development cycle is peer reviews. This helps the developer to refine his/her code at an early stage. Hence, we closely followed this process in our development cycle. Every time a team member commits a completed use case, a peer reviewer was assigned whose responsibility was to verify if the code captures the essence of the planned use case design and its resilience towards edge cases. The reviewer not only checks the correctness of the code, but also suggests any potentially optimized approach to solving the same use case. If the reviewer found difficulty in understanding any code segment the two developers scheduled a one-one where the developer walks through the code and discusses his/her approach before the reviewer scrutinizes it.

###### Pair Programming

Another common Agile practice we incorporated in our development cycle is pair programming. Here, two developers work on a single laptop; the programmer who types the code is called the driver and the one who oversees the direction of the code logic is called the navigator. The developer swap roles every few minutes based on their preferred portion. Specifically in our project, Himani and Prashanthi worked on the Use Case 4: Progress graph generation while Jagan and Priyankha worked on Use Case 3: Pomodoro. 

## Consistency 

###### Divided tasks equally amongst everyone

We assigned 20 points for each of us for the entire milestone. 10 for each iteration. The exact split up and how we weighed are described in the above section.

###### Commit frequency for the two sprints

Commit graph for the week of Oct 28 - Nov 2 (Iteration-1) is as follows :
![week1](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/Milestone-2/images/iteration1.png)

Commit graph for the week of Oct 28 - Nov 2 (Iteration - 2) is as follows :
![week2](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/Milestone-2/images/iteration2.png)

As it can be seen from the above graph, the commits are spread across the number of points we allocated each iteration.
Iteration-2 had lot of integrations to do on each of our tasks over the first iteration which shows the peak in the number of commits in the second iteration over first iteration.

###### Consistency in Agile 

To be on the same page, everyday standups are held and meeting notes are uploaded. The meeting notes also include the work finished for the previous day and the work in progress for the current day. 
This helped us in knowing what each of us are doing and how much work is left to continue.

## Documentation of iteration end 

###### First iteration 

Use case-1: List Tasks was done completely<br />
Use case-2: Create Task was done completely<br />
Database set up: The database was set up and necessary tables were created and mock data was inserted for temporary use<br />
Use case-3: Start Task, for this the pomodoro implementation logic was discussed and implementation was done partially<br />
Progress graph generation for use case-4 : Progress graph requirements and display format were discussed and implementation was done partially 

###### Second iteration

Use case-3: Start Task was done completely<br />
Progress graph generation for use case-4: Progress graph generation was done completely<br />
Use case-4: Show progress was done completely.

###### Status of completed tasks:

1. Use Case-1: List tasks
2. Use Case-2: Create task
3. Use Case-3: Start task
4. Use Case-4: Show progress<br />

The above tasks were completed and giving the required output

###### Status of incomplete tasks:

1. Some edge cases have to be captured in the use cases
2. Unit test cases should be implemented for all the use cases

###### Process Reflection:

We also faced some blockers while implementing the tasks. We made use of the buffer points which had been assigned to dive deep and solve the issues.

###### Blockers:

For the Use Case 3, we faced issues with the front end integration of the interactive buttons. We were unable to let go off the warnings and had to research on the issue. After digging deep, we found the issue was a result of async process and had to solve it accordingly. 

For the Use Case 4, we wanted to show the same colour palette for all percentage above 100. So, we spent time in coming up with an efficient way to design it.


