Installation 
1.  Sign up for a google cloud account at console.developrs.google.com
2.  Follow the instructions and download the json with the keys in it.
3.  Head to https://developers.google.com/identity/sign-in/web/sign-in and follow the   
    directions to get a google oauth client id.
4.  Once you have an oauth id change the clientid in GoogleButton.jsx in the scripts folder.
5.  Create a .env file and set GOOGLE_APPLICATION_CREDENTIALS equal to the path of the json key from step 2.
6.  Creaate a variable named PROJECT_ID in the same .env file and set it equal to the project_id in the json
7.  Sign up for a pixabay account at https://pixabay.com/accounts/register/?source=main_nav
8.  Create a .env file and set the variable IMAGE_ID to the accounts API key.
9.  Install postgresql by following the directions at https://www.postgresql.org/download/
10. Initialize psql by running `sudo service postgresql initdb`
11. Do `sudo service postgresql start` to start psql.
12. Create a new superuser by running `sudo -u postgres createuser --superuser $USER`  
13. Run `sudo -u postgres createdb $USER` to make a new database
14. To make a new user follow these commands 
    a) If you quit out of psql enter `psql` again. 
    b) Enter the following command   
    (replace some_username_here and new_password_here with your username and password)  
    `create user some_username_here superuser password 'new_password_here';`  
    c) `\q` to quit out of sql  

15. Create a .env file to hold your databases user password and url. These  
    should be called SQL_USER, SQL_PASSWORD, and DATABASE_URL respectively.
16. Clone this repository if you have not already by performing `git clone https://github.com/NJIT-CS490/project2-m2-sb989.git`
17. Change the path names for the .env files in the proj2.py file to their appropriate locations. 
18. Perform the following command in the terminal  
    sudo pip install -r requirements.txt
19. To start the program run python prog2.py
20. Open a browser and head to 127.0.0.1:8080 to see the site.

Problems
1.  One problem I encountered was when I deployed my app to heroku. The google oauth would not work on some devices but would work on others.  
    After searching the internet for answers to this problem I finally asked the slack chat for any solutions.  
    Someone recommeneded adding the heroku link with both https and http to the google oauth page. This solved this issue.
2.  When breaking the chatbox into different react components the check to see if the message was from the user stopped working.  
    As a result all messages appeared as if they were from others. After a few hours of looking through the code I finally realised  
    that I had mispelled the variable that I passed to the react component.

Improvements
1.  I would implement multiple ways to login as well as the traditional login function using email and passsword. Other websites like facebook
    have a react component like google making implementing their login easy. For the traditional login function I would send the email and password to the server  
    which would check the database to see if the password entered is correct and send a respone to the client. The password on the databse would be hashed.

2.  Implementing multiple chat rooms would another improvment I would implement if I had time. The user would see the chatrooms they are a part of on the left in a   
    list they could scroll through. They could look for a chatroom through a search bar. This would send to the server the name of the chatroom and it would return  
    a list of chatrooms with similar names through a json file. This file would also include wether or not the room is password protected. If it is, it would require  
    the user to enter the password which would be sent to the server and checked against the password stored on the database.  
    Sending messages to a chatroom would take advantage of socket.io's room ability. This allows it to send messages to only a certain group of people. The rooms name,  
    password, and socketio's room id would be kept on the database. 
