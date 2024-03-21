from tkinter import simpledialog
import cv2
import time
import pymysql
import numpy as np
from tkinter import *
import settings as st
import credentials as cr
import face_recognition as f
import videoStream as vs
import multiprocessing as mp
from datetime import datetime
from tkinter import messagebox
from tkinter import messagebox
from twilio.rest import Client
from credentials import *

# The LoginSystem class
class LoginSystem:
    def __init__(self, root):
        # Window settings
        self.window = root
        self.window.title("Login System")
        self.window.geometry("780x480")
        self.window.config(bg=st.color1)
        self.window.resizable(width = False, height = False)

        # Declaring a variable with a default value
        self.status = False

         # Left Frame
        self.frame1 = Frame(self.window, bg=st.color1)
        self.frame1.place(x=0, y=0, width=540, relheight = 1)

        label_in_frame1 = Label(self.frame1, text="Password Less Authentication System", font=("Arial", 18), bg=st.color1, fg="black")
        label_in_frame1.place(x=80, y=180)

        name1 = Label(self.frame1, text="-Manmeet Singh", font=("Arial", 16), bg=st.color1, fg="black")
        name1.place(x=80, y=230)
        name2 = Label(self.frame1, text="-Ipsit Maurya", font=("Arial", 16), bg=st.color1, fg="black")
        name2.place(x=80, y=260)
        name3 = Label(self.frame1, text="-Subhratha Sinha", font=("Arial", 16), bg=st.color1, fg="black")
        name3.place(x=80, y=290)

        # Right Frame
        self.frame2 = Frame(self.window, bg = st.color2)
        self.frame2.place(x=540,y=0,relwidth=1, relheight=1)

        # Calling the function called buttons()
        self.buttons()

    # A Function to display buttons in the right frame
    def buttons(self):
        loginButton = Button(self.frame2, text="Login", font=(st.font3, 12), bd=2, cursor="hand2", width=7, command=self.loginEmployee)
        loginButton.place(x=74, y=40)

        registerButton = Button(self.frame2, text="Register", font=(st.font3, 12), bd=2, cursor="hand2", width=7, command=self.adminPanel)
        registerButton.place(x=74, y=100)

        clearButton = Button(self.frame2, text="Clear", font=(st.font3, 12), bd=2, cursor="hand2", width=7, command=self.clearScreen)
        clearButton.place(x=74, y=160)

        exitButton = Button(self.frame2, text="Exit", font=(st.font3, 12), bd=2, cursor="hand2", width=7, command=self.exit)
        exitButton.place(x=74, y=220)

    # A Function to login into the system through face recognition method
    def loginEmployee(self):
        # Clear the screen first
        self.clearScreen()
    
        # Inheriting the class called VideoStream and its
        # methods here from the videoStream module to capture the video stream
        faces = vs.encode_faces()
        encoded_faces = list(faces.values())
        faces_name = list(faces.keys())
        video_frame = True
    
        # stream = 0 refers to the default camera of a system
        video_stream = vs.VideoStream(stream=0)
        video_stream.start()
    
        while True:
            if video_stream.stopped is True:
                break
            else:
                frame = video_stream.read()
    
                if video_frame:
                    face_locations = f.face_locations(frame)
                    unknown_face_encodings = f.face_encodings(frame, face_locations)
    
                    face_names = []
                    for face_encoding in unknown_face_encodings:
                        # Comparing the faces
                        matches = f.compare_faces(encoded_faces, face_encoding)
                        name = "Unknown"
    
                        face_distances = f.face_distance(encoded_faces, face_encoding)
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = faces_name[best_match_index]
    
                        face_names.append(name)
    
                video_frame = not video_frame
    
                for (top, right, bottom, left), faceID in zip(face_locations, face_names):
                    # Draw a rectangular box around the face
                    cv2.rectangle(frame, (left - 20, top - 20), (right + 20, bottom + 20), (0, 255, 0), 2)
                    # Draw a Label for showing the name of the person
                    cv2.rectangle(frame, (left - 20, bottom - 15), (right + 20, bottom + 20), (0, 255, 0),
                                  cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    # Showing the face_id of the detected person through
                    # the WebCam
                    cv2.putText(frame, "Face Detected", (left - 20, bottom + 15), font, 0.85, (255, 255, 255), 2)
    
                    # Call the function for attendance
                    self.status = self.isPresent(faceID)

                # delay for processing a frame
                delay = 0.04
                time.sleep(delay)
    
                cv2.imshow('frame', frame)
                key = cv2.waitKey(1)
                # If self.status is True(which means the face is identified)
                # the look will be break,
                # and all cv2 window will be closed.
                if self.status == True:
                    # Set the logged_in_user attribute
                    self.setLoggedInUser(faceID)
                    break
        video_stream.stop()
    
        # closing all windows
        cv2.destroyAllWindows()
        # Calling a function to show the status after entering an employee
        self.employeeEntered()
    
    # Function to set the logged_in_user attribute
    def setLoggedInUser(self, UID):
        try:
            connection = pymysql.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
            curs = connection.cursor()
            curs.execute("SELECT * FROM employee_register WHERE uid=%s", UID)
            row = curs.fetchone()

            if row:
                self.logged_in_user = row
                print("Logged in user:", self.logged_in_user)  # Ensure user details are retrieved
            connection.close()
        except Exception as e:
            messagebox.showerror("Error!", f"Error setting logged-in user: {str(e)}", parent=self.window)

    # A Function to check if the user id of the detected face is matching 
    # with the database or not. If yes, the function returns the value True.
    def isPresent(self, UID):
        try:
            connection = pymysql.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
            curs = connection.cursor()
            curs.execute("select * from employee_register where uid=%s", UID)
            row = curs.fetchone()
            if row == None:
                pass
            else:
                connection.close()
                return True
        except Exception as e:
                messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)

    def generate_otp(self):
        import random
        return str(random.randint(100000, 999999))
    # A Function to display the entering time of the employee after his/her
    # face is identified.
    def employeeEntered(self):
        # Clear the screen first
        self.clearScreen()
        # Reset the value of self.status varible 
        self.status = False

        heading = Label(self.frame1, text="Face Verified", font=(st.font4, 30, "bold"), bg=st.color1, fg=st.color3)
        heading.place(x=140, y=30)
        
        # Getting the current time
        current_datetime = datetime.now()
        now = current_datetime.strftime("%d-%m-%Y %I:%M:%S %p")  # Example format: YYYY-MM-DD HH:MM:SS

        label1 = Label(self.frame1, text="Time: ", font=(st.font1, 18, "bold"), bg=st.color1, fg=st.color3)
        label1.place(x=40, y=120)

        # Display the current time on the Tkinter window
        timeLabel = Label(self.frame1, text=now, font=(st.font1, 16), bg=st.color1, fg=st.color3)
        timeLabel.place(x=160, y=123)

         # Display the name of the logged-in employee
         # Display user details
        if self.logged_in_user:
            # Extract user details
            user_name = f"{self.logged_in_user[0]} {self.logged_in_user[1]}"
            user_uid = self.logged_in_user[2]
            user_contact = self.logged_in_user[4]

            # Create and place labels for user details
            name_label = Label(self.frame1, text="Name:", font=(st.font1, 16), bg=st.color1, fg=st.color3)
            name_label.place(x=40, y=160)
            name_value = Label(self.frame1, text=user_name, font=(st.font1, 16), bg=st.color1, fg=st.color3)
            name_value.place(x=160, y=160)

            email_label = Label(self.frame1, text="Phone:", font=(st.font1, 16), bg=st.color1, fg=st.color3)
            email_label.place(x=40, y=190)
            email_value = Label(self.frame1, text=user_contact, font=(st.font1, 16), bg=st.color1, fg=st.color3)
            email_value.place(x=160, y=190)

            uid_label = Label(self.frame1, text="UID:", font=(st.font1, 16), bg=st.color1, fg=st.color3)
            uid_label.place(x=40, y=220)
            uid_value = Label(self.frame1, text=user_uid, font=(st.font1, 16), bg=st.color1, fg=st.color3)
            uid_value.place(x=160, y=220)

            otp = self.generate_otp()
            # Initialize Twilio client
            client = Client(Account_SID, Auth_Token)

            # Send OTP using your valid Twilio phone number
            message = client.messages.create(
                body=f"Your OTP is: {otp}",
                from_= Twilio_Number,
                to=user_contact
            )
            print(message.sid)

            # Create Entry widget for OTP input
            otp_label = Label(self.frame1, text="Enter OTP:", font=(st.font1, 16), bg=st.color1, fg=st.color3)
            otp_label.place(x=40, y=250)
            self.otp_entry = Entry(self.frame1, font=(st.font1, 16), bg=st.color4, fg=st.color3)
            self.otp_entry.place(x=160, y=250)

            # Create a button to verify OTP
            verify_button = Button(self.frame1, text="Verify OTP", font=(st.font3, 12), bd=2, cursor="hand2", width=10, command=lambda: self.verifyOTP(otp))
            verify_button.place(x=350, y=250)

    def verifyOTP(self, generated_otp):
        try:
            entered_otp = self.otp_entry.get().strip()
            if entered_otp == "":
                messagebox.showerror("Error", "Please enter the OTP.")
                return

            # Perform OTP verification here
            # Compare entered OTP with the expected OTP
            if self.otp_entry.get() == generated_otp:
            # For now, let's assume the OTP verification is successful
                messagebox.showinfo("Success", "OTP verification successful!")
            # Proceed to the next step or page
                login_successful_label = Label(self.frame1, text="Login Successful", font=(st.font1, 16), bg=st.color1, fg=st.color3)
                login_successful_label.place(x=40, y=300)
            else:
            # OTP verification failed
                messagebox.showerror("Error", "Incorrect OTP entered. Please try again.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    # A Function to display widgets for Admin Login
    def adminPanel(self):
        # Clear the screen first
        self.clearScreen()

        heading = Label(self.frame1, text="Admin Panel", font=(st.font4, 30, "bold"), bg=st.color1, fg=st.color3)
        heading.place(x=140, y=30)

        usernameLabel = Label(self.frame1, text="User Name", font=(st.font1, 18), bg=st.color1, fg=st.color3)
        usernameLabel.place(x=40, y=120)

        self.userName = Entry(self.frame1, font=(st.font2, 15), width=20, bg=st.color4, fg=st.color1)
        self.userName.place(x=160, y=123)

        passwordLabel = Label(self.frame1, text="Password", font=(st.font1, 18), bg=st.color1, fg=st.color3)
        passwordLabel.place(x=40, y=180)

        # Password Entry Box
        self.password = Entry(self.frame1, show="*", font=(st.font2, 15), width=20, bg=st.color4, fg=st.color1)
        self.password.place(x=160, y=183)

        loginButton = Button(self.frame1, text="Login", font=(st.font3, 12), bd=2, cursor="hand2", width=7, bg=st.color5, fg=st.color1, command=self.loginAdmin)
        loginButton.place(x=220, y=240)

    # A Function for login into the system for the Admin
    def loginAdmin(self):
        if self.userName.get() == "" or self.password.get() == "":
            messagebox.showerror("Field Missing", "Please fill all the field")
        else:
            try:
                connection = pymysql.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
                curs = connection.cursor()
                curs.execute("select * from admin where username=%s and password=%s", (self.userName.get(), self.password.get()))
                row=curs.fetchone()
                
                if row == None:
                    messagebox.showerror("Error!","Please enter the correct information", parent=self.window)
                else:
                    self.registerPage()
                    connection.close()
            except Exception as e:
                messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)

    # If the Admin logged in successfully, this function will display widgets
    # to regiter a new employee
    def registerPage(self):
        self.clearScreen()

        name = Label(self.frame1, text="First Name", font=(st.font2, 15, "bold"), bg=st.color1).place(x=40,y=30)
        self.nameEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.nameEntry.place(x=40,y=60, width=200)

        surname = Label(self.frame1, text="Last Name", font=(st.font2, 15, "bold"), bg=st.color1).place(x=300,y=30)
        self.surnameEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.surnameEntry.place(x=300,y=60, width=200)

        # Calling the function getUID() to get the user id of the last employee
        row = self.getUID()
        
        uid = Label(self.frame1, text="User ID*", font=(st.font2, 15, "bold"), bg=st.color1).place(x=40,y=100)
        # Displaying the current available user id for the new employee
        self.uidLabel = Label(self.frame1, text=f"{row[0] + 1}", bg=st.color1, fg=st.color3, font=(st.font2, 15))
        self.uidLabel.place(x=40,y=130)

        eamil = Label(self.frame1, text="Email ID", font=(st.font2, 15, "bold"), bg=st.color1).place(x=300,y=100)
        self.emailEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.emailEntry.place(x=300,y=130, width=200)

        contact = Label(self.frame1, text="Contact", font=(st.font2, 15, "bold"), bg=st.color1).place(x=300,y=170)
        self.contactEntry = Entry(self.frame1, bg=st.color4, fg=st.color1, font=(st.font2, 15))
        self.contactEntry.place(x=300,y=200, width=200)

        submitButton = Button(self.frame1, text='Submit', font=(st.font3, 12), bd=2, command=self.submitData, cursor="hand2", bg=st.color5,fg=st.color1).place(x=200,y=389,width=100)

    # This function returns the last or max user id from the employee_register table
    def getUID(self):
        try:
            connection = pymysql.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
            curs = connection.cursor()
            curs.execute("select MAX(uid) from employee_register")
            row = curs.fetchone()
            # Close the connection
            connection.close()
            # Return row
            return row

        except Exception as e:
            messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)
    
    # This function enters the data of the new employee into the employee_register
    # table.
    def submitData(self):
        if self.nameEntry.get() == "" or self.surnameEntry.get() == "" or self.emailEntry.get() == "" or self.contactEntry.get() == "" :
            messagebox.showwarning("Empty Field", "All fields are required", parent = self.window)
        else:
            try:
                connection = pymysql.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
                curs = connection.cursor()

                curs.execute("insert into employee_register (f_name,l_name,email,contact) values(%s,%s,%s,%s)",
                                        (
                                            self.nameEntry.get(),
                                            self.surnameEntry.get(),
                                            self.emailEntry.get(),
                                            self.contactEntry.get(),
                                        ))
                connection.commit()
                connection.close()
                messagebox.showinfo('Done!', "The data has been submitted")
                self.resetFields()
            
            except Exception as e:
                messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)
    
    # This function resets all the fields for register an employee
    def resetFields(self):
        self.nameEntry.delete(0, END)
        self.surnameEntry.delete(0, END)
        # Updating the user id label with the next available uid from the table
        row = self.getUID()
        self.uidLabel.config(text=f"{row[0] + 1}")
        self.emailEntry.delete(0, END)
        self.contactEntry.delete(0, END)

    # Function to clear all the widgets from the frame1
    def clearScreen(self):
        for widget in self.frame1.winfo_children():
            widget.destroy()

    # A function to destroy the tkinter window
    def exit(self):
        self.window.destroy()

# The main function
if __name__ == "__main__":
    root = Tk()
    obj = LoginSystem(root)
    root.mainloop()
