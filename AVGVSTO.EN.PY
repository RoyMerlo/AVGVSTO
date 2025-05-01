import os
import sys
import platform
import psutil
import hashlib
import hmac
from tkinter import *
from tkinter import ttk, filedialog, messagebox, simpledialog
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

# --- Configuration files ---
KEY_FILE = "usb_secure.key"
ATTEMPTS_FILE = "attempts.txt"

# --- Encryption functions ---
def derive_key(password, salt):
    """Derive a secure key using PBKDF2"""
    return PBKDF2(password, salt, dkLen=32, count=1000000)

def pad(data):
    """PKCS7 padding"""
    pad_len = AES.block_size - len(data) % AES.block_size
    return data + bytes([pad_len]) * pad_len

def unpad(data):
    """Remove PKCS7 padding"""
    return data[:-data[-1]]

def get_usb_identifier(path):
    """Get unique USB drive identifier"""
    try:
        stat = os.stat(path)
        return hashlib.sha256(str(stat.st_dev).encode()).hexdigest()
    except:
        return None

def save_usb_key_id(usb_path):
    """Save USB drive ID to configuration file"""
    usb_id = get_usb_identifier(usb_path)
    if usb_id:
        with open(KEY_FILE, 'w') as f:
            f.write(usb_id)
        return usb_id
    return None

def load_usb_key_id():
    """Load saved USB drive ID"""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'r') as f:
            return f.read().strip()
    return None

def scan_usb_and_match_id(saved_id):
    """Verify connected USB drives against saved ID"""
    for path in list_usb_drives():
        if get_usb_identifier(path) == saved_id:
            return path
    return None

def list_usb_drives():
    """List all connected USB storage devices"""
    drives = []
    for p in psutil.disk_partitions():
        if platform.system() == 'Windows' and 'removable' in p.opts:
            drives.append(p.device)
        elif '/media' in p.mountpoint or '/run/media' in p.mountpoint:
            drives.append(p.mountpoint)
    return drives

def encrypt_file(file_path, key, usb_id):
    """Encrypt a single file"""
    with open(file_path, 'rb') as f:
        data = f.read()
    salt = get_random_bytes(16)
    iv = get_random_bytes(16)
    password_hash = hashlib.sha256(key).digest()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data))
    with open(file_path + '.enc', 'wb') as f:
        f.write(salt + iv + usb_id.encode() + password_hash + encrypted_data)
    os.remove(file_path)

def decrypt_file(file_path, key, current_usb_id):
    """Decrypt a single file"""
    with open(file_path, 'rb') as f:
        raw = f.read()
    salt = raw[:16]
    iv = raw[16:32]
    stored_usb_id = raw[32:96].decode(errors='ignore')
    stored_password_hash = raw[96:128]
    
    if stored_usb_id != current_usb_id:
        raise ValueError("Unauthorized USB drive")
    if not hmac.compare_digest(stored_password_hash, hashlib.sha256(key).digest()):
        raise ValueError("Incorrect password")
    
    data = raw[128:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(data))
    new_path = file_path.replace('.enc', '')
    
    with open(new_path, 'wb') as f:
        f.write(decrypted_data)
    os.remove(file_path)

def process_folder(folder_path, key, usb_id, encrypt=True):
    """Process all files in a folder recursively"""
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            if encrypt and not file.endswith(".enc"):
                encrypt_file(full_path, key, usb_id)
            elif not encrypt and file.endswith(".enc"):
                decrypt_file(full_path, key, usb_id)

def load_attempts():
    """Load decryption attempt counter"""
    if os.path.exists(ATTEMPTS_FILE):
        with open(ATTEMPTS_FILE, 'r') as f:
            return int(f.read().strip())
    return 0

def save_attempts(attempts):
    """Save current attempt counter"""
    with open(ATTEMPTS_FILE, 'w') as f:
        f.write(str(attempts))

def reset_attempts():
    """Reset attempt counter"""
    if os.path.exists(ATTEMPTS_FILE):
        os.remove(ATTEMPTS_FILE)

# --- Graphical User Interface ---
class AVGVSTO(Tk):
    def __init__(self):
        super().__init__()
        self.title("AVGVSTO - Security Suite")
        self.geometry("520x560")
        self.configure(bg="#1e1e1e")
        
        # Main title (White, large)
        title_label = Label(
            self,
            text="AVGVSTO",
            fg="white",
            bg="#1e1e1e",
            font=("Segoe UI", 72, "bold")
        )
        title_label.pack(pady=20)
        
        # Version subtitle
        subtitle_label = Label(
            self,
            text="Version 1.0",
            fg="#888888",
            bg="#1e1e1e",
            font=("Segoe UI", 14)
        )
        subtitle_label.pack()
        
        # Developer logos
        logo_frame = Frame(self, bg="#1e1e1e")
        logo_frame.pack(pady=10)
        
        # RM Logo
        self.rm_logo = Label(
            logo_frame,
            text="RM",
            fg="#00ff00",
            bg="#1e1e1e",
            font=("Segoe UI", 18, "bold"),
            cursor="hand2"
        )
        self.rm_logo.pack(side=LEFT, padx=10)
        self.rm_logo.bind("<Enter>", lambda e: self.rm_logo.config(fg="#00ffff"))
        self.rm_logo.bind("<Leave>", lambda e: self.rm_logo.config(fg="#00ff00"))
        Label(logo_frame, text=" - Powered By Roy Merlo", fg="#888888", bg="#1e1e1e", font=("Segoe UI", 10)).pack(side=LEFT)
        
        # RPX Logo
        self.rpx_logo = Label(
            logo_frame,
            text="RPX",
            fg="#ff0000",
            bg="#1e1e1e",
            font=("Segoe UI", 18, "bold"),
            cursor="hand2"
        )
        self.rpx_logo.pack(side=LEFT, padx=10)
        self.rpx_logo.bind("<Enter>", lambda e: self.rpx_logo.config(fg="#ff00ff"))
        self.rpx_logo.bind("<Leave>", lambda e: self.rpx_logo.config(fg="#ff0000"))
        Label(logo_frame, text=" - Powered By RPX", fg="#888888", bg="#1e1e1e", font=("Segoe UI", 10)).pack(side=LEFT)
        
        # USB drive selector
        self.usb_var = StringVar()
        self.usb_combo = ttk.Combobox(self, textvariable=self.usb_var, width=50)
        self.usb_combo.pack(pady=10)
        self.refresh_usb_list()
        
        # Action buttons
        button_frame = Frame(self, bg="#1e1e1e")
        button_frame.pack(pady=15)
        
        buttons = [
            ("🔧 Set Secure USB Drive", self.set_usb),
            ("🔐 Encrypt File or Folder", self.encrypt_data),
            ("🔓 Decrypt File or Folder", self.decrypt_data),
            ("🔄 Refresh USB List", self.refresh_usb_list)
        ]
        
        for text, command in buttons:
            btn = Button(
                button_frame, text=text, command=command,
                bg="#2d2d2d", fg="#00ffcc", font=("Segoe UI", 12),
                relief=FLAT, bd=0, padx=10, pady=8, width=25
            )
            btn.pack(fill=X, pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#00ffcc", fg="#1e1e1e"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#2d2d2d", fg="#00ffcc"))
        
        # Status bar
        self.status = Label(
            self, text="", bg="#1e1e1e", fg="#00ffcc", font=("Segoe UI", 12)
        )
        self.status.pack(pady=10)
        
        # Initial USB detection
        self.refresh_usb_list()

    def refresh_usb_list(self):
        """Update USB drive list in combobox"""
        self.usb_combo["values"] = list_usb_drives()
        self.usb_combo.set("Select USB drive...")

    def set_usb(self):
        """Configure selected USB as secure device"""
        selected = self.usb_var.get()
        if selected:
            if save_usb_key_id(selected):
                self.status.config(text="✅ Secure USB drive configured")
            else:
                self.status.config(text="❌ Failed to save USB ID")
        else:
            messagebox.showwarning("Warning", "Please select a valid USB drive")

    def encrypt_data(self):
        """Handle file/folder encryption"""
        usb_id = load_usb_key_id()
        if not usb_id:
            messagebox.showerror("Error", "Set up a secure USB drive first")
            return
        
        current_usb_path = scan_usb_and_match_id(usb_id)
        if not current_usb_path:
            messagebox.showerror("Error", "Secure USB drive not detected")
            return
        
        password = simpledialog.askstring("Password", "Enter encryption password:", show="*")
        if not password:
            messagebox.showwarning("Warning", "Password is required")
            return
        
        key = derive_key(password, usb_id.encode())
        path = filedialog.askopenfilename(title="Select File") or filedialog.askdirectory(title="Select Folder")
        
        if not path or not os.path.exists(path):
            messagebox.showwarning("Warning", "Invalid file/folder selection")
            return
        
        try:
            if os.path.isfile(path) and path.endswith(".enc"):
                messagebox.showwarning("Warning", "File already encrypted")
                return
            
            if os.path.isdir(path):
                for root, _, files in os.walk(path):
                    for file in files:
                        if file.endswith(".enc"):
                            messagebox.showwarning("Warning", "Folder contains already encrypted files")
                            return
            
            if os.path.isfile(path):
                encrypt_file(path, key, usb_id)
            else:
                process_folder(path, key, usb_id, encrypt=True)
            
            messagebox.showinfo("Success", "File/folder encrypted successfully")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decrypt_data(self):
        """Handle file/folder decryption"""
        usb_id = load_usb_key_id()
        if not usb_id:
            messagebox.showerror("Error", "Set up a secure USB drive first")
            return
        
        current_usb_path = scan_usb_and_match_id(usb_id)
        if not current_usb_path:
            messagebox.showerror("Error", "Unauthorized USB drive detected!")
            return
        
        attempts = load_attempts()
        max_attempts = 3
        
        while attempts < max_attempts:
            password = simpledialog.askstring("Password", "Enter decryption password:", show="*")
            if not password:
                messagebox.showwarning("Warning", "Password required")
                return
            
            key = derive_key(password, usb_id.encode())
            path = filedialog.askopenfilename(title="Select Encrypted File") or filedialog.askdirectory(title="Select Encrypted Folder")
            
            if not path or not os.path.exists(path):
                messagebox.showwarning("Warning", "Invalid selection")
                return
            
            try:
                if os.path.isfile(path):
                    decrypt_file(path, key, usb_id)
                else:
                    process_folder(path, key, usb_id, encrypt=False)
                
                messagebox.showinfo("Success", "File/folder decrypted successfully")
                reset_attempts()
                break
            
            except ValueError as ve:
                attempts += 1
                save_attempts(attempts)
                
                if attempts < max_attempts:
                    messagebox.showerror(
                        "Error",
                        f"Attempt {attempts} failed: {str(ve)}\n"
                        f"{max_attempts - attempts} attempts remaining"
                    )
                else:
                    try:
                        if os.path.isfile(path):
                            os.remove(path)
                            messagebox.showerror("Error", "Too many failed attempts. File deleted")
                        else:
                            import shutil
                            shutil.rmtree(path)
                            messagebox.showerror("Error", "Too many failed attempts. Folder deleted")
                        
                        reset_attempts()
                    except Exception as del_err:
                        messagebox.showerror("Error", f"Failed to delete: {str(del_err)}")
                    break
            
            except Exception as e:
                messagebox.showerror("Error", f"Operation failed: {str(e)}")
                break

# --- Application entry point ---
if __name__ == "__main__":
    try:
        app = AVGVSTO()
        app.mainloop()
    except Exception as e:
        print(f"[FATAL ERROR] {str(e)}")