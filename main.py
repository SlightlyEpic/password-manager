# IMPORTS
#######################################################################
import tkinter as Tk
import tkinter.constants as TkC
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
def main():
    if not e_man.keyFileExists():
        # Show page to generate key
        #
        #
        #
        #

        # Close window
        # main()
        pass
    else:
        # Create window
        root = Tk.Tk()
        root.geometry('360x90')
        root.title('Login')
        root.resizable(0,0)
        root.configure(bg='#002766')

        # Initialize window elements
        win_elements = {
            "label_pwd": Tk.Label(root, text='Password :',font=('TkTextFont',10), padx=5, pady=5),
            "label_pin": Tk.Label(root, text='PIN :',font=('TkTextFont',10), padx=5, pady=5),
            "entry_box_pwd": Tk.Entry(root, show='\u2022', width=40),
            "entry_box_pin": Tk.Entry(root, show='\u2022', width=40),
            "ok_button": Tk.Button(root, text='OK', font=('TkTextFont', 10), fg='blue', width=5, command=lambda: login(win_elements["entry_box_pwd"].get(), win_elements["entry_box_pin"].get()))
        }

        # Position window elements
        win_elements["label_pwd"].grid(row=1,column=1)
        win_elements["label_pin"].grid(row=2,column=1)
        win_elements["entry_box_pwd"].grid(row=1,column=2)
        win_elements["entry_box_pin"].grid(row=2,column=2)
        win_elements["ok_button"].grid(row=3,column=2)

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

        def clearWindow(win_elements):
            # NOTE: for key in win_elements.keys() does not work because it results in this error -> RuntimeError: dictionary changed size during iteration
            for key in list(win_elements):
                win_elements[key].destroy()     # Make tkinter destroy the element
                del win_elements[key]           # Remove it from the dictionary

        def login(password, pin):

            if not checkCredentials(password, pin):
                # Login failed due to invalid credentials

                # Show login failed text
                print("login failed")
                #
                #
                #

                pass
            else:
                # Successful login

                e_man.decryptData()         # Decrypt emails through key
                p_man.decryptData()         # Decrypt passwords through key


                root.geometry("900x720")
                clearWindow(win_elements)

                cred_container_frame = Tk.Frame(root, height=620, width=880, bg='#FF5D5C')
                # cred_container_frame.grid(row=0, column=0)
                cred_container_frame.pack(padx=2, pady=2)
                cred_fields = []            # no not this pls ignore -> [ [Email1_label, Password1_label], [Email2_label, Password2_label], ..... ]

                def addRow(email, password):
                    # Function to add a row to the windows

                    row_num = len(cred_fields)

                    e_text, p_text = Tk.StringVar(), Tk.StringVar()

                    index_label = Tk.Label(cred_container_frame, text=row_num+1 , font=('TkTextFont',10), padx=5, pady=5, width=5, bg='#FF5D5C')
                    e_entry = Tk.Entry(cred_container_frame, textvariable=e_text , font=('TkTextFont',10), width=25, bg='#9CCCFF', highlightbackground='black', highlightthickness=2, state='readonly')
                    p_entry = Tk.Entry(cred_container_frame, textvariable=p_text, font=('TkTextFont',10), width=25, bg='#DCF2E3', highlightbackground='black', highlightthickness=2, state='readonly', show='\u2022')
                    view_button = Tk.Button(cred_container_frame, text='👁', width=2, bg='#9CCCFF')

                    e_text.set(email)
                    p_text.set(password)

                    index_label.grid(row=row_num, column=0)
                    e_entry.grid(row=row_num, column=1)
                    p_entry.grid(row=row_num, column=2)
                    view_button.grid(row=row_num, column=3)

                    # TODO: Add an edit button on each row
                    # TODO: Add a copy to clipboard button for e_entry and p_entry
                    # TODO: Make the 👁 button actually work, probably replace it with a radiobutton instead

                    cred_fields.append([index_label, e_entry, p_entry, view_button])

                # Display main GUI
                # Display data read from storage
                for i in range(e_man.data_lines):
                    addRow(e_man.decrypted_data[i], p_man.decrypted_data[i])
                
                #Display other utility buttons
                

        login('hello', '1234')
        # Mainloop
        root.mainloop()

main()