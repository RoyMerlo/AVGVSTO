
![defavg](https://github.com/user-attachments/assets/3a4af588-56fb-48e3-82c1-c32dfd0e5a56)














![AVGVSTOEN2](https://github.com/user-attachments/assets/b9956f46-da28-4ca3-a994-4ba953b68294)






🛡️ AVGVSTO - Advanced Security Suite with USB Binding 

AVGVSTO  is a Python-based encryption tool that binds sensitive data to a physical USB drive , ensuring decryption is only possible when the authorized device is connected. It combines AES-256 encryption with robust USB hardware authentication and brute-force protection for enhanced security. 
🔍 Key Features 

    Hardware-Bound Encryption 
    Files can only be decrypted when the original USB drive (used during encryption) is connected. The USB's unique identifier (st_dev) is embedded in the encrypted file.
    AES-256 with PBKDF2 
    Secure key derivation using SHA-256 with 1 million iterations  for password-to-key conversion.
    Brute-Force Protection 
    After 3 failed decryption attempts , encrypted files/folders are automatically deleted.
    Recursive Folder Encryption 
    Encrypt entire directories and nested files with a single operation.
    Modern GUI 
    Intuitive interface with drag-and-drop support, real-time feedback, and responsive design.
     

🧰 System Requirements 

    Python 3.9+   
    Dependencies :  
    bash
     
    pip install pycryptodome psutil
    OS Support :
    Windows, Linux, macOS (USB detection optimized for Windows and Unix-like systems).
    GUI :
    Built with tkinter (included in Python).
     

📦 Project Structure 
 
AVGVSTO/
├── AVGVSTO.py              # Main application (GUI + logic)
├── usb_secure.key          # Stores the authorized USB drive's unique ID
├── attempts.txt            # Tracks failed decryption attempts
├── requirements.txt        # Dependency list
└── README.md               # Documentation
 
 
🚀 Installation & Setup 

    Clone the Repository    
    bash
     
git clone https://github.com/your-username/AVGVSTO.git
cd AVGVSTO
 
 

Install Dependencies    
bash
 
pip install -r requirements.txt
 
Run the Application    
bash
 

     
    
    python AVGVSTO.py
     
     
     

📋 Usage Guide 
1. Configure a Secure USB Drive 

    Connect a USB drive.
    In the app, select it from the dropdown menu.
    Click "🔧 Set Secure USB Drive" .
    ➤ This saves the USB's unique ID to usb_secure.key.
     

2. Encrypt Files/Folders 

    Click "🔐 Encrypt File or Folder" .
    Enter a strong password (not stored; used to derive the encryption key).
    Select a file or folder.
    ➤ The original file/folder will be deleted after encryption.
     

3. Decrypt Files/Folders 

    Ensure the authorized USB drive is connected.
    Click "🔓 Decrypt File or Folder" .
    Enter the password used during encryption.
    ➤ After 3 incorrect attempts, files are permanently deleted.
     

🔐 Security Architecture 
USB Binding Mechanism 

The USB drive's unique identifier (st_dev) is hashed with SHA-256 and stored in usb_secure.key. During decryption, the app verifies the connected USB matches this ID. If the USB is lost, data becomes unrecoverable. 
Password Management 

    Passwords are never stored.  
    A SHA-256 hash of the password is embedded in the encrypted file.  
    PBKDF2 with 1 million iterations slows brute-force attacks.
     

Brute-Force Protection 

Failed decryption attempts are tracked in attempts.txt. After 3 failures: 

    Encrypted files/folders are deleted.
    The attempt counter resets.
     

🧠 Technical Details 
Encryption Process 

    Generate a random salt (16 bytes)  and IV (16 bytes) .
    Derive a 32-byte AES key from the password and USB ID using PBKDF2.
    Encrypt data with AES-256 in CBC mode.
    Append metadata to the encrypted file:
    [salt][iv][usb_id][password_hash][encrypted_data]
     

Decryption Process 

    Extract salt, IV, USB ID, and password hash from the file.
    Verify the connected USB matches the stored ID.
    Validate the entered password against the stored hash.
    Decrypt data using the derived key and IV.
     

⚠️ Security Considerations 

    USB Key File (usb_secure.key) :
    This file is critical. If exposed, an attacker could bypass USB binding. Protect it with strict file permissions.
    Physical Security :
    Losing the USB drive means losing access to encrypted data. Store it securely.
    Password Strength :
    Use long, complex passwords to resist dictionary attacks.
     

🤝 Contributing 

Contributions are welcome! To contribute: 

    Fork the repository.
    Create a feature branch:  
    bash
     

 
1
git checkout -b feature/new-feature
 
 
Commit changes:  
bash
 
 
1
git commit -m "Add new feature"
 
 
Push to the branch:  
bash
 

     
    1
    git push origin feature/new-feature
     
     
    Open a Pull Request.
     


❤️ Authors 

    Roy Merlo (RM) : GitHub @RoyMerlo 
    RPX : GitHub @RPX 
     

📬 Contact 

For questions or suggestions, open an issue on GitHub or reach out to the authors directly. 

AVGVSTO  is a powerful tool for securing sensitive data with hardware-based encryption. Ideal for:   

    Secure backups of confidential documents  
    Sharing encrypted files with strict access control  
    Protecting against unauthorized data recovery
     

🔒 Always verify your USB drive is disconnected when not in use. 
  

