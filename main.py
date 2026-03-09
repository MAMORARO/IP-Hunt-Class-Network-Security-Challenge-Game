import mysql.connector 
from datetime import datetime
import hashlib
import getpass
import sys


class GameClient:

    def __init__(self): # constructor
        self.user_name = None
        self.password = None
        self.connection = None
        self.cursor = None

    def get_user_input(self):
        self.user_name = input("Enter your username :")
        self.password = getpass.getpass("Enter your password :")

    def connect_database(self):
        try:
            self.connection = mysql.connector.connect(
                host = "localhost",
                port = 3306,
                user = self.user_name,
                password = self.password,
                database = "ip_hunt_class"
            )
            self.cursor = self.connection.cursor()
            print ("connected successfully")

        except mysql.connector.Error:
            print ("connection failed")
            sys.exit()
     
    def check_progress(self):
        
        try:
            
            self.select_query =self.cursor.execute("select current_level from hunt_progress where username=%s",(self.user_name,))

            results = self.cursor.fetchone()

            if results is None:
                self.cursor.execute("insert into hunt_progress(username,current_level,completed) values(%s, 1, 0)",(self.user_name,))
                self.connection.commit()
                self.current_level =1
                print("New player! starting at level 1.")
            else:
                self.current_level = results[0]
                print(f"Welcome back! continuing from level {self.current_level}.")   

        except mysql.connector.Error:
              print("error checking progress has occurred.")
              sys.exit() 

    def get_challenge(self):
        
        try:
            
            self.cursor.execute("select suspicious_ip and hint from challenges where username=%s and level=%s",(self.user_name, self.current_level))
            results =self.cursor.fetchone()

            if results is None:
               print("No challenge found for this level.")
               sys.exit()
            else:
                print("="*40)
                print(f"Level {self.current_level}")
                print("="*40)
                print(f" Hint: {self.hint}")
                print("="* 40)

        except  mysql.connector.Error:
            print("Error retrieving challenge.")
            sys.exit()              

    def  verify_answer(self):
        
        try:
            
            while True:
                user_answer = input("Enter your flag answer:")

                combined = user_answer + self.user_name
                hash_input =hashlib.sha256(combined.encode()).hexdigest()


                self.cursor.execute("select flag_hash from challenges where username =%s and level =%s", (self.user_name,self.current_level))

                results = self.cursor.fetchone()
                flag_hash = results[0]

                if hash_input == flag_hash:
                    print("correct! well done.")
                    self.log_attempt(True)
                    self.update_progress()
                    break
                else:
                    print("wrong answer, try again.")
                    self.log_attempt(False)
        except  mysql.connector.Error:
               
               print("Error verifying answer.")
               sys.exit()  


    def   log_attempt(self, success): # update the players log attempt, try to  track 
        try: 
            self.cursor.execute("insert into attempt_log(username , level , attempt_time, success) values (%s, %s, %s, %s)",(self.user_name,self.current_level, datetime.now(),success)) 

            self.connection.commit()  

        except mysql.connector.Error:
            print("Error logging attempt.")
            sys.exit()

    def update_process(self):

        try:
            self.current_level +=1

            self.cursor.execute(" update hunt_progress set current_level =%s where username =%s",(self.current_level,self.user_name)) 
            self.connection.commit()
            print(f"Advancing to the next level {self.user_name}.")
        except mysql.connector.Error:
            print("Error updating progress.")
            sys.exit()

    def TCP_Game(self):

        try:

            completion_time =datetime.mow()

            self.cursor.execute("select username from leaderboard where username =%s",(self.user_name,))
            results = self.cursor.fetchone()

            if results is None:
                self.cursor.execute("insert into leaderboard(username, completion_time) value(%s, %s)", (self.user_name, completion_time))
                self.conncetion.commit()

                print("congratulations!, You completed the IP hunt!.")
                print(f"Completion time: {completion_time}")

        except  mysql.connector.Error:
            print("Error completing Game.")  
            sys.exit()

    def close_connection(self):
        try:

            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            print("Connection has closed.")

        except mysql.connector.Error:
            print("Error closing connection.")

    def play_game(self):

        self.get_user_input()
        self.connect_database()
        self.check_progress()

        while self.current_level <=3:
            self.get_challenge()
            self.verify_answer()

        if  self.current_level >3:
            self.TCP_Game()

        self.close_connection()          
                                          

if __name__ =="__main__":
    game=GameClient()
    game.play_game()






























                             
            

    


    