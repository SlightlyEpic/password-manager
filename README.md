# Password Manager Application

### Overview
This is a GUI-based password manager application built using Python and Tkinter. It securely stores and manages passwords and related credentials using encryption provided by the cryptography library. Users can:
- Securely store credentials.
- Add, view, edit, and delete credentials.
- Use password and PIN-based authentication to protect access.

### Features
- First-time Setup: Generate a new encryption key and secure the application with a master password and PIN.
- Login System: Password and PIN are required for authentication.
- Encrypted Storage: All credentials are encrypted using a secure key.
- Credential Management:
    - Add new entries.
    - Edit existing credentials.
    - Copy credentials to the clipboard.
    - Delete entries securely.
- User-Friendly Interface: Easy-to-use GUI with intuitive controls.

### Security Details
- Encryption: Uses the Fernet symmetric encryption from the cryptography library.
- Key Storage: The encryption key is stored in secret.key. Protect this file.
- Password and PIN Validation: Password and PIN are used to derive keys for decryption and validation.

### Running the Application
With python insalled, double click `Launch App.pyw` to launch the application. Alternatively run `python "Launch App.pyw"` from a terminal to start it.

PS: This was a school project which was written waaaaay back so the code could be a little sloppy 😅
