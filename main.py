import socket 
import getpass
import sys

class GameClient:

        
    server_ip_address=str(input(" Enter IP Address  e.g  :"))
    port_number =int(input("Enter Port Number e.g :"))
    user_name=str(input("Enter Your Username e.g :"))
    password=getpass.getpass("Enter Your password e.g :")
    

    def __init__(self,server_ip_address,port_number,user_name,password):
        self.server_ip_address =server_ip_address
        self.port_number=port_number
        self.user_name =user_name
        self.password =password

    def connect_server(self):
        
           self.socket= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
           try:
                self.socket.connect((self.server_ip_address,self.port_number))
                print("Server connected successfully!.")

           except ConnectionRefusedError:
                print(" Server failed to connect!.")
                sys.exit()

           except TimeoutError:
                print("Server Time out error!.")
                sys.exit()

           except Exception:
                print("Unexpected error has occurred!.")     
                sys.exit()

    def Login(self):
         
         



    


    