# This is a secondary application which handles the changing of the main
# login credentials for the application

# IMPORTS
#######################################################################
import tkinter as Tk
from cryptography.fernet import InvalidToken
from modules.manager import Manager
#######################################################################


# INITIALIZATION
#######################################################################
e_man = Manager("./store/storage1.dat", "./store/secret.key")

palette = ['#113859', '#1C588C', '#174873', '#6D8BA6', '#6D8BA6', '#9CCCFF']
#######################################################################


# TKINTER GUI
#######################################################################
def main():
    global logo_img

    # Create window
    root = Tk.Tk()
    root.resizable(0,0)
    root.configure(bg=palette[0])
    root.title('Change logincredentials')

    def changePwdHandler(oldPwd, oldPin, newPwd, newPin):
        if e_man.keyFileExists():
            if(newPwd == "" or newPin == ""):
                win_elements['alert_label'].configure(fg='red', text='New credentials cannot be empty')
                return
            # Verify old password
            e_man.setInstancePassword(oldPwd)
            e_man.setInstanceSalt(oldPin)
            try:
                e_man.readKey()
            except InvalidToken:
                win_elements['alert_label'].configure(fg='red', text='Current credentials are incorrect!')
            else:
                e_man.changePassword(newPwd, newPin)
                win_elements['alert_label'].configure(fg='green', text='Successfully changed login credentials!')
        else:
            win_elements['alert_label'].configure(fg='red', text='Please generate your credentials first\nby launching the main application')


    # Initialize window elements
    win_elements = {
        "label_pwd_old": Tk.Label(root, text='Current Password :', font=('TkTextFont',10), padx=5, pady=5, bg=palette[0], fg='white'),
        "label_pin_old": Tk.Label(root, text='Current PIN :', font=('TkTextFont',10), padx=5, pady=5, bg=palette[0], fg='white'),
        "label_pwd_new": Tk.Label(root, text='New Password :', font=('TkTextFont',10), padx=5, pady=5, bg=palette[0], fg='white'),
        "label_pin_new": Tk.Label(root, text='New PIN :', font=('TkTextFont',10), padx=5, pady=5, bg=palette[0], fg='white'),
        "entry_box_pwd_old": Tk.Entry(root, show='\u2022', width=40),
        "entry_box_pwd_new": Tk.Entry(root, show='\u2022', width=40),
        "entry_box_pin_old": Tk.Entry(root, show='\u2022', width=40),
        "entry_box_pin_new": Tk.Entry(root, show='\u2022', width=40),
        "changepwd_button": Tk.Button(
            root, text='Change Credentials', font=('TkTextFont', 10), bg=palette[4], fg='white', width=15,
            command=lambda: changePwdHandler(
                win_elements["entry_box_pwd_old"].get(), win_elements["entry_box_pwd_new"].get(),
                win_elements["entry_box_pin_old"].get(), win_elements["entry_box_pin_new"].get()
                )
            ),
        "alert_label": Tk.Label(root, text='', font=('TkTextFont',10), width=30, bg=palette[0], fg='red')
    }

    # Position window elements
    win_elements["label_pwd_old"].grid(row=0, column=0)
    win_elements["label_pin_old"].grid(row=1, column=0)
    win_elements["label_pwd_new"].grid(row=2, column=0)
    win_elements['label_pin_new'].grid(row=3, column=0)
    win_elements["entry_box_pwd_old"].grid(row=0, column=1)
    win_elements['entry_box_pwd_new'].grid(row=1, column=1)
    win_elements["entry_box_pin_old"].grid(row=2, column=1)
    win_elements['entry_box_pin_new'].grid(row=3, column=1)
    win_elements["changepwd_button"].grid(row=5, column=1)
    win_elements["alert_label"].grid(row=6, column=1)

    root.mainloop()

main()