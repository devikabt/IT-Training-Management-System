# Web application for "IT-Training-Management-System"

Everything that happens in the training center will be automated by the IT-Training Management System. It is intended to assist and simplify the work of all individuals who receive training at the center, teach programs to students, and operate the training center. The database contains training details provided by the training center, tests and results of students who attend tuition at the center, contact information and personal information for each individual who attends training at the center.

## Participants of "IT-Training Management System"
* STUDENTS
* TRAINERS
* RECEPTIONIST
* ADMIN

## Participant Functionality
 * Admin - Admin/Owner of the training center may add a receptionist, delete a receptionist, add a trainer, delete a trainer, see details of everyone like Receptionist, Trainers, and  members. Add new students to the training center, delete a student when one is departing, add course details, remove course details, add and remove batches depending on course details, and trainers.

 * Students - Students can use the system to access their batch information, course information, exam information, and progress information. Users can change their contact information, personal information, and so forth. Students can also see their trainers' contact information. Kids can keep track of their development.

 * Trainers - Trainers may develop and update test plans, examine all the details, progress of all those who train under them,  modify their own contact data and personal information, and view all the batch details they are handling in the training center.

 * Receptionist - Receptionist can view contact details of everyone, batch details, course details, add a member, delete a member.

 ## TECHNOLOGIES USED

* Frontend Technologies :
    1. HTML5
    2. CSS3
    3. BOOTSTRAP
    4. Javascript
    5. Jquery

* Backend Technologies :
   - Python
		- flask
		- flask session
        - flask_mysqldb 
* Database 
   - MYSQL

* Local Server
   - WAMPSERVER


## LIBRARIES USED 
Below python libraries are used in this app. 

- flask 
- flask_mysqldb 
- wtforms 
- wtforms.fields
- passlib.hash 
- flask_script
- functools 
- datetime 

Below is the command to install a python library 

pip install [library_name]

## Requirements for running application:

my SQL database: we need to have mysql database. the database name is TrainingManagement, if not then please create datebase with this given name.

This system needs one bootstrap admin user to be present. To add the admin user, use below command

INSERT INTO info(username, password, street, city, phone, name, prof)
 VALUES('Admin', '$5$rounds=535000$ieyp6HcB3HxFQBrM$DOIzUkDfDQ8Q4PMYXopPKum392DuG.gRNZDpw5c0r4B', 
 	'Castle house', 'Dublin 1', '123456789', 'Devika', 1);

To run the app, navigate to root directory and enter below command. 

flask --app app run 

Once app opens (usually open run on 127.0.0.1:5000 given that user does not change port), user will land on login page. 

Enter below credentials to login as admin user. 

- username - Admin
- password - Admin@123

Having logged in, you must first enter course data before adding a trainer. Because teachers will be chosen based on the courses that the training facility provides. Next, we must add trainers since Admin will build batches depending on them. We construct batches after adding trainers. Students can be added after batches have been added. Nevertheless, we cannot generate students until we first create batches.

After creating Courses, Trainers, Batches, and Students. Trainers can update the test dates for each batch and evaluate each student in their batch. Students may access their progress data in the dashboard once Trainers have updated their progress.

This system provides a dashboard for receptionists with functions such as adding members, deleting members, and seeing the details of current members.








