
#                             ____     __     _____  ___   _______  ________
#   ___  ___  ___ ___ _    __|_  /____/ /__  /  _/ |/ / | / / __/ |/ /_  __/
#  / _ \/ _ \/ -_) _ \ |/|/ //_ </ __/  '_/ _/ //    /| |/ / _//    / / /   
#  \___/ .__/\__/_//_/__,__/____/_/ /_/\_\ /___/_/|_/ |___/___/_/|_/ /_/    
#     /_/     (c) openw3rk / (c) openw3rk INVENT                        

import subprocess
import sys
                                       
def install_packages():

    try:
        import pip
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'ensurepip'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    
    required_packages = ['tk', 'ftplib']
    for package in required_packages:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
    from ftplib import FTP, error_perm
except ImportError:
    install_packages()
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
    from ftplib import FTP, error_perm
class openw3rkFFTC:
    def __init__(self, master):
        self.master = master
        self.master.title("openw3rk-FFTC")
        
        self.ftp = None
        self.ftp_details = {
            'host': tk.StringVar(),
            'username': tk.StringVar(),
            'password': tk.StringVar()
        }
        
        self.history = []
        self.current_path = ""
        self.forward_history = []
        
        self.create_widgets()
        

        print(r"""  
                                ____       _       _____ _   ___      ________ _   _ _______ 
                               |___ \     | |     |_   _| \ | \ \    / /  ____| \ | |__   __|
   ___  _ __   ___ _ ____      ____) |_ __| | __    | | |  \| |\ \  / /| |__  |  \| |  | |   
  / _ \| '_ \ / _ \ '_ \ \ /\ / /__ <| '__| |/ /    | | | . ` | \ \/ / |  __| | . ` |  | |   
 | (_) | |_) |  __/ | | \ V  V /___) | |  |   <    _| |_| |\  |  \  /  | |____| |\  |  | |   
  \___/| .__/ \___|_| |_|\_/\_/|____/|_|  |_|\_\  |_____|_| \_|   \/   |______|_| \_|  |_|   
       | |                                                                                  
       |_|  develop@openw3rk.de                                                       
""") 

        print("\nWelcome to openw3rk-FFTC [*openw3rk FTP FILE TRANSFER CLIENT*]\n\n(c) openw3rk / (c) openw3rk INVENT\n");

    def create_widgets(self):
        login_frame = tk.Frame(self.master)
        login_frame.pack(pady=10)
        
        tk.Label(login_frame, text="Host:").grid(row=0, column=0)
        tk.Entry(login_frame, textvariable=self.ftp_details['host']).grid(row=0, column=1)
        
        tk.Label(login_frame, text="Username:").grid(row=1, column=0)
        tk.Entry(login_frame, textvariable=self.ftp_details['username']).grid(row=1, column=1)
        
        tk.Label(login_frame, text="Password:").grid(row=2, column=0)
        tk.Entry(login_frame, textvariable=self.ftp_details['password'], show='*').grid(row=2, column=1)
        
        tk.Button(login_frame, text="Login", command=self.connect).grid(row=3, columnspan=2, pady=5)
        nav_frame = tk.Frame(self.master)
        nav_frame.pack(pady=5)
        
        self.back_button = tk.Button(nav_frame, text="<--", command=self.go_back, state=tk.DISABLED)
        self.back_button.pack(side=tk.LEFT, padx=5)
        
        self.forward_button = tk.Button(nav_frame, text="-->", command=self.go_forward, state=tk.DISABLED)
        self.forward_button.pack(side=tk.LEFT, padx=5)
        self.tree = ttk.Treeview(self.master)
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)
        
        self.tree["columns"] = ("size", "modified")
        self.tree.heading("#0", text="Name")
        self.tree.heading("size", text="Size")
        self.tree.heading("modified", text="Modified")
        
        self.tree.bind("<Double-1>", self.change_directory)
        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Upload", command=self.upload_file).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Download", command=self.download_file).pack(side=tk.LEFT, padx=5)
        copyright_label = tk.Label(self.master, text="(c) openw3rk / (c) openw3rk INVENT", anchor="e")
        copyright_label.pack(side=tk.BOTTOM, fill=tk.X, pady=5, padx=5)
    
    def connect(self):
        try:
            self.ftp = FTP(self.ftp_details['host'].get())
            self.ftp.login(self.ftp_details['username'].get(), self.ftp_details['password'].get())
            self.history = [self.ftp.pwd()]
            self.current_path = self.ftp.pwd()
            self.forward_history = []
            self.load_directory()
            messagebox.showinfo("Info", "Connected successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def load_directory(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        file_list = []
        self.ftp.retrlines('LIST', file_list.append)
        
        for file_info in file_list:
            parts = file_info.split()
            filename = parts[-1]
            size = parts[4]
            modified = " ".join(parts[5:8])
            self.tree.insert("", "end", text=filename, values=(size, modified))
        
        self.update_nav_buttons()
    
    def change_directory(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            directory = self.tree.item(selected_item[0], 'text')
            try:
                self.ftp.cwd(directory)
                self.history.append(self.ftp.pwd())
                self.current_path = self.ftp.pwd()
                self.forward_history = []
                self.load_directory()
            except error_perm:
                pass  
    
    def go_back(self):
        if len(self.history) > 1:
            self.forward_history.append(self.history.pop())
            self.ftp.cwd(self.history[-1])
            self.current_path = self.history[-1]
            self.load_directory()
    
    def go_forward(self):
        if self.forward_history:
            next_dir = self.forward_history.pop()
            self.history.append(next_dir)
            self.ftp.cwd(next_dir)
            self.current_path = next_dir
            self.load_directory()
    
    def update_nav_buttons(self):
        if len(self.history) > 1:
            self.back_button.config(state=tk.NORMAL)
        else:
            self.back_button.config(state=tk.DISABLED)
        
        if self.forward_history:
            self.forward_button.config(state=tk.NORMAL)
        else:
            self.forward_button.config(state=tk.DISABLED)
    
    def upload_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            with open(filename, 'rb') as file:
                self.ftp.storbinary(f'STOR {os.path.basename(filename)}', file)
            self.load_directory()
            messagebox.showinfo("Info", "File uploaded successfully")
    
    def download_file(self):
        selected_item = self.tree.selection()
        if selected_item:
            filename = self.tree.item(selected_item[0], 'text')
            save_path = filedialog.asksaveasfilename(initialfile=filename)
            if save_path:
                with open(save_path, 'wb') as file:
                    self.ftp.retrbinary(f'RETR {filename}', file.write)
                messagebox.showinfo("Info", "File downloaded successfully")

if __name__ == "__main__":
    try:
        import tkinter as tk
        from tkinter import ttk, filedialog, messagebox
        from ftplib import FTP, error_perm
    except ImportError:
        install_packages()
    
    root = tk.Tk()
    app = openw3rkFFTC(root)
    root.mainloop()
