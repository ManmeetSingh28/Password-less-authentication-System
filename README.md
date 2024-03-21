# Face-Recognition-Login-System

It's a Password-less-authentication-System which is developed using Python Tkinter, MySQL database and Twilio.

To successfully launch the project in your system, first, you must create the following database, and tables and declare some default data there. I'm assuming the MySQL server is installed in your system and you know the basics.

1. Create a database with this name, "employee_management"

create database employee_management;

2. Now create a table ("employee_register") under that database.

CREATE TABLE employee_register (
f_name VARCHAR(40) NOT NULL,
l_name VARCHAR(40) NOT NULL,
uid INT NOT NULL AUTO_INCREMENT,
email VARCHAR(100) NOT NULL,
contact BIGINT NOT NULL,
PRIMARY KEY (uid)
);

3. Run this command
   Since we have set the user id as Integer type and Auto Increment (see the previous section), here we will set a base value for it so that the counting starts from that range.

==== ALTER TABLE employee_register AUTO_INCREMENT=1000; ==== #Important

4. Create an another table ("admin") there

CREATE TABLE admin (
username VARCHAR(255) NOT NULL,
password VARCHAR(255) NOT NULL,
PRIMARY KEY (username)
);

5. Insert default value into the "admin" table
   In this case, we are setting a user id and password for the admin of the system. You need to choose this credential as per your choice here.

INSERT INTO admin (username,password) VALUES ('your_username','your_password');

6. Please ensure that the necessary content is added to the credentials.py file.

7. After completing the preceding steps, please proceed by installing the required dependencies using the provided requirements file (requirements.txt). Once installed, you can execute the main.py file to run the application.

8. Please ensure that images are placed in the 'Images' folder with filenames corresponding to the UID.
