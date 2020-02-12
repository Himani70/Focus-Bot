# Milestone: DEPLOYMENT

The goal of this milestone is to demonstrate a fully deployed version of Focus bot present in slack team https://se510-3.slack.com.

Details on how to connect and test are given as part of [Acceptance Testing](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/ACCEPTANCE_TESTING.md)

### Deployment

We have used configuring management tools to fully provision and configuring a remote environment for the bot. We choose EC2 to deploy our server. We made use of the AWS Educate credits and have also used Elastic IP for the EC2 instances to expose the app to the Slack. 

Ansible playbook can be found at [Deployment Script](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/playbook.yaml).

The inventory script is as follows:
![Inventory](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/images/Screenshot%202019-12-01%20at%205.37.05%20PM.png)

    [group]

    {IPAddress} ansible_user=xxxx ansible_become=true ansible_ssh_private_key_file=path/to/pem/file
 
Steps to run the script:

Run command 
```sh
sudo ansible-playbook -i hosts playbook.yaml -vvv
```

Here, the hosts is the inventory file. If required, the default inventory file (/etc/ansible/hosts or similar) can be used. The playbook also requires a config.yaml file. The required github token to access this repository since it is private and the database user name and password has to be specified. The format of the config.yaml can be found at [Config File](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/config.yaml). The config.yaml should be in the same folder as the playbook.yaml file. 

The steps to run the ansible script are as follows:

1) Update/create your inventory file with the required host information.
2) Update/create your config.yaml file with the required configuration details.
3) Make sure the first two steps are done.
4) Run the ansible-script.

[Deployment Demo](https://drive.google.com/open?id=16JholtXMWFopgrUsa-tCki8UMD8OPatq)

This demo might seem longer than desired. We had to clearly show all the steps involved and the things to update if a new server has to be used. It was also not aided by the bandwidth at home. Apologies for any inconvinience.

### Acceptance Testing

[Acceptance Testing](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/ACCEPTANCE_TESTING.md) has been created separately for a clear picture.

### Continuous Integration (CI) Server

Deployed a jenkins server in the local and also created a job to build the repository after every commit.

CI setup and the related focusbot job:

![CI](https://github.ncsu.edu/csc510-fall2019/CSC510-3/blob/master/images/CI.png)

Features:
----------
1) The jenkins job starts after every commit to the focus bot repository and checks the correctness of the commit by running unit, integration, functional tests etc. 
2) Also added a post build task to show that the functionality of jenkins can be enhanced. The post build task can range my executing a script or sending mails to members involved in the project about the build status.
3) The jenkins setup can be migrated to VM with just few extra steps.
4) The current jenkins setup will try to run the test cases and execute a post build task if the previous build step was success. The post build task can be configured to execute for success/ failure i.e. dynamic use cases. For example, we might want to notify the memebers only when the build was failure and continue the next step in deployment if the build step was success.

[CI Demo](https://drive.google.com/open?id=1cjL4PBK8IbxjjiQu_C6f1ka0oiEHI-Pg) 

This demo might seem longer than desired. We had to clearly show all the steps involved and the things to update if a new server has to be used. It was also not aided by the bandwidth at home. Apologies for any inconvinience.


### Kanban Board

Scrumban method was followed for this sprint as well and the cards are displayed on the [project board](https://github.ncsu.edu/csc510-fall2019/CSC510-3/projects/2?fullscreen=true) under Sprint-3 column.

### Final code

Final code has been updated in [Milestone-2](https://github.ncsu.edu/csc510-fall2019/CSC510-3/tree/master/Milestone-2) folder.

### Screencasts

[Acceptance Testing](https://drive.google.com/file/d/1WgpGRXn51jYZYmVMj0iqgKlG9BNunkIW/view?usp=sharing)

[Deployment Demo](https://drive.google.com/open?id=16JholtXMWFopgrUsa-tCki8UMD8OPatq)

[CI Demo](https://drive.google.com/open?id=1cjL4PBK8IbxjjiQu_C6f1ka0oiEHI-Pg) 

