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
            "label_pin": Tk.Label(root, text='    PIN :    ',font=('TkTextFont',10), padx=5, pady=5),
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

        def clearWindowList(element_list):
            for i in range(len(element_list)):
                element_list[i].destroy()

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
                cred_container_frame.grid(row=0, column=0)
                # cred_container_frame.pack(padx=2, pady=2)

                cred_fields = []            #[ [index_label1, e_entry1, p_entry1, view_button1, clipboard_button1, edit_button1, delete_button1], ..... ]
                # Last element in cred_fields will always be the row with only the index and + button


                def toggleShowPw(row_num, char):
                    cred_fields[row_num][2].configure(show=char)

                def copyToClipboard(row_num):
                    root.clipboard_clear()
                    root.clipboard_append(cred_fields[row_num][2].get())

                def disintegrateRow(row_num):
                    e_man.popRow(row_num)
                    p_man.popRow(row_num)
                    clearWindowList(cred_fields[row_num])
                    regenRows()

                    # Add the last row with the + button which is used to add a new row
                    row_num2 = len(cred_fields)

                    index_label = Tk.Label(cred_container_frame, text=e_man.data_lines+1 , font=('TkTextFont',10), padx=5, pady=5, width=5, bg='#FF5D5C')
                    newrow_button = Tk.Button(cred_container_frame, text='➕ New Entry', width=12, bg='#9CCCFF', command=addDummyRow)
                    index_label.grid(row=row_num2, column=0)
                    newrow_button.grid(row=row_num2, column=1)

                    cred_fields.append([index_label, newrow_button])

                def toggleEdit(row_num, firstSave=False):
                    fields = cred_fields[row_num]
                    em = fields[1]      # e_entry
                    pw = fields[2]      # p_entry
                    ed = fields[5]      # edit_button

                    mode = ed.config('text')[-1]

                    if(mode == 'Edit'):
                        toggleShowPw(row_num, '')
                        pw.configure(state='normal')
                        em.configure(state='normal')
                        ed.configure(text='Save', bg='#11CC11')
                    elif(mode == 'Save'):
                        toggleShowPw(row_num, '*')
                        pw.configure(state='readonly')
                        em.configure(state='readonly')
                        ed.configure(text='Saving', state='disabled')
                        if(firstSave):
                            ed.configure(command=lambda: toggleEdit(row_num))
                            fields[6].grid(row=row_num, column=6)

                        new_em_text = em.get()
                        new_pw_text = pw.get()
                        e_man.storeData(new_em_text, row_num)
                        p_man.storeData(new_pw_text, row_num)

                        ed.configure(text='Edit', bg='#9CCCFF', state='normal')

                def addRow(email, password):
                    # Function to add a row to the windows

                    row_num = len(cred_fields)

                    e_text, p_text = Tk.StringVar(), Tk.StringVar()

                    index_label = Tk.Label(cred_container_frame, text=row_num+1 , font=('TkTextFont',10), padx=5, pady=5, width=5, bg='#FF5D5C')
                    e_entry = Tk.Entry(cred_container_frame, textvariable=e_text , font=('TkTextFont',10), width=25, bg='#DCF2E3', highlightbackground='black', highlightthickness=2, state='readonly')
                    p_entry = Tk.Entry(cred_container_frame, textvariable=p_text, font=('TkTextFont',10), width=25, bg='#DCF2E3', highlightbackground='black', highlightthickness=2, state='readonly', show='*')
                    view_button = Tk.Button(cred_container_frame, text='👁 View', width=7, bg='#9CCCFF')
                    clipboard_button = Tk.Button(cred_container_frame, text='📋 Copy', width=7, bg='#9CCCFF', command=lambda: copyToClipboard(row_num))
                    edit_button = Tk.Button(cred_container_frame, text='Edit', width=7, bg='#9CCCFF', command=lambda: toggleEdit(row_num))
                    delete_button = Tk.Button(cred_container_frame, text='🗑️ Delete', width=10, bg='#CC1111', command=lambda: disintegrateRow(row_num))

                    view_button.bind("<ButtonPress>", lambda e: toggleShowPw(row_num, ''))
                    view_button.bind("<ButtonRelease>", lambda e: toggleShowPw(row_num, '*'))

                    e_text.set(email)
                    p_text.set(password)

                    index_label.grid(row=row_num, column=0)
                    e_entry.grid(row=row_num, column=1)
                    p_entry.grid(row=row_num, column=2)
                    view_button.grid(row=row_num, column=3)
                    clipboard_button.grid(row=row_num, column=4)
                    edit_button.grid(row=row_num, column=5)
                    delete_button.grid(row=row_num, column=6)

                    # TODO: Add an edit button on each row ✅
                    # TODO: Add a copy to clipboard button for e_entry and p_entry ✅
                    # TODO: Make the 👁 button actually work ✅

                    cred_fields.append([index_label, e_entry, p_entry, view_button, clipboard_button, edit_button, delete_button])

                def addDummyRow():
                    # Remove new row button
                    cred_fields[-1][0].destroy()
                    cred_fields[-1][1].destroy()
                    del cred_fields[-1]

                    # Add dummy row
                    row_num1 = len(cred_fields)

                    e_text, p_text = Tk.StringVar(), Tk.StringVar()

                    index_label = Tk.Label(cred_container_frame, text=row_num1+1 , font=('TkTextFont',10), padx=5, pady=5, width=5, bg='#FF5D5C')
                    e_entry = Tk.Entry(cred_container_frame, textvariable=e_text , font=('TkTextFont',10), width=25, bg='#DCF2E3', highlightbackground='black', highlightthickness=2, state='normal')
                    p_entry = Tk.Entry(cred_container_frame, textvariable=p_text, font=('TkTextFont',10), width=25, bg='#DCF2E3', highlightbackground='black', highlightthickness=2, state='normal', show='')
                    view_button = Tk.Button(cred_container_frame, text='👁 View', width=7, bg='#9CCCFF')
                    clipboard_button = Tk.Button(cred_container_frame, text='📋 Copy', width=7, bg='#9CCCFF', command=lambda: copyToClipboard(row_num1))
                    edit_button = Tk.Button(cred_container_frame, text='Save', width=7, bg='#11CC11', command=lambda: toggleEdit(row_num1, firstSave=True))
                    delete_button = Tk.Button(cred_container_frame, text='🗑️ Delete', width=10, bg='#CC1111', command=lambda: disintegrateRow(row_num1))

                    view_button.bind("<ButtonPress>", lambda e: toggleShowPw(row_num1, ''))
                    view_button.bind("<ButtonRelease>", lambda e: toggleShowPw(row_num1, '*'))

                    e_text.set('')
                    p_text.set('')

                    index_label.grid(row=row_num1, column=0)
                    e_entry.grid(row=row_num1, column=1)
                    p_entry.grid(row=row_num1, column=2)
                    view_button.grid(row=row_num1, column=3)
                    clipboard_button.grid(row=row_num1, column=4)
                    edit_button.grid(row=row_num1, column=5)
                    # delete_button.grid(row=row_num, column=6)

                    cred_fields.append([index_label, e_entry, p_entry, view_button, clipboard_button, edit_button, delete_button])

                    # Re-add the row with + button at the end
                    row_num2 = len(cred_fields)
                    index_label = Tk.Label(cred_container_frame, text=row_num2+1 , font=('TkTextFont',10), padx=5, pady=5, width=5, bg='#FF5D5C')
                    newrow_button = Tk.Button(cred_container_frame, text='➕ New Entry', width=12, bg='#9CCCFF', command=addDummyRow)

                    index_label.grid(row=row_num2, column=0)
                    newrow_button.grid(row=row_num2, column=1)

                    cred_fields.append([index_label, newrow_button])


                # Display main GUI

                # Display data read from storage
                def regenRows():
                    for i in range(len(cred_fields)):
                        clearWindowList(cred_fields[i])

                    cred_fields.clear()

                    for i in range(e_man.data_lines):
                        addRow(e_man.decrypted_data[i], p_man.decrypted_data[i])

                regenRows()

                # Add the last row with the + button which is used to add a new row
                row_num = len(cred_fields)

                index_label = Tk.Label(cred_container_frame, text=e_man.data_lines+1 , font=('TkTextFont',10), padx=5, pady=5, width=5, bg='#FF5D5C')
                newrow_button = Tk.Button(cred_container_frame, text='➕ New Entry', width=12, bg='#9CCCFF', command=addDummyRow)
                index_label.grid(row=row_num, column=0)
                newrow_button.grid(row=row_num, column=1)

                cred_fields.append([index_label, newrow_button])
                
                #Display other utility buttons
                
                


        # Mainloop
        root.mainloop()

main()