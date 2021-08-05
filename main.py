# IMPORTS
#######################################################################
import tkinter as Tk
from cryptography.fernet import InvalidToken
from modules.manager import Manager
#######################################################################




# INITIALIZATION
#######################################################################
e_man = Manager("./storage1.dat", "./secret.key")
p_man = Manager("./storage2.dat", "./secret.key")
#######################################################################




# TKINTER GUI
#######################################################################
if not e_man.keyFileExists():
    # Show page to generate key
    #
    #
    #
    #

    pass
else:
    # Show login page elements
    #
    #
    #
    #

    def checkCredentials(password, pin):
        e_man.setInstancePassword(password)
        e_man.setInstanceSalt(pin)
        p_man.setInstancePassword(password)
        p_man.setInstanceSalt(pin)

        try:
            e_man.readKey()
            p_man.readKey()
        except InvalidToken:
            # Invalid credentials
            return False
        else:
            # Valid credentials
            return True
    
    def login():
        password = "????"       # Get value of password
        pin = "????"            # Get value of pin

        if not checkCredentials(password, pin):
            # Login failed due to invalid credentials

            # Show login failed text
            #
            #
            #
            #

            pass
        else:
            # Successful login

            e_man.decryptData()         # Decrypt emails through key
            p_man.decryptData()         # Decrypt passwords through key
            
            def addRow(email, password):
                # Function to add a row to the window
                pass

            # Display main GUI
            #
            #
            #
            #
            #

            pass