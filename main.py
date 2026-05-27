import base64
import io
import tkinter as tk; from tkinter import messagebox; from tkinter import font#; from tkinter import ttk #Tkinter imports of Doom!
import saveManager
import ttkbootstrap as ttk # UI Customisation (CUSTOM LIBRARY - To be removed since switching to customtkinter)
import customtkinter as ctk
from PIL import Image, ImageTk
import os
import base64 as b64

#INTRODUCTION
root = tk.Tk()
PEmlInfo = None
PUsrInfo = None

#GLOBAL CONFIG VARIABLES
GFontHeading = font.Font(family="Helvetica", size=18, weight="bold")
GFontBold = font.Font(family="Helvetica", size=14, weight="bold")
GFontRegular = font.Font(family="Helvetica", size=14, weight="normal")

#GLOBAL CONFIG CODE
root.option_add("*Font", GFontRegular) #Default font
ctk.set_appearance_mode("light")

try:
    ctk.set_default_color_theme("bin\\theme.json") #Execution on Windows
except:
    ctk.set_default_color_theme("bin/theme.json") #Execution on UNIX-based Systems

style = ttk.Style() #LEGACY, NOT NEEDED SOON!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# ~ #
DFrame = tk.Frame(root) #Debug Menu frame
BFrame = tk.Frame(root) #Banner Frame (persistant across all pages)
RFrame = tk.Frame(root) #Registration Frame
LFrame = tk.Frame(root) #Login Frame
PFrame = tk.Frame(root) #Profile Frame

#WINDOW CONFIGURATION
def WinCfg(window_width, window_height):

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width // 2) - (window_width // 2) #Finds half of screen res for X
    y = (screen_height // 2) - (window_height // 2) #Finds half of screen res for Y

    root.geometry(f"{window_width}x{window_height}+{x}+{y}") #Apply the changes... Window size + Center Screen


# FORM FUNCTIONS

def HideForms():
    print("[INFO] Hiding all other Graphical Forms")
    DFrame.forget()
    RFrame.forget()
    LFrame.forget()
    PFrame.forget()
    return # This returns back to the line of where the function was originally called from.

def Show_Debug():
    HideForms()
    root.title("Debug Menu") #Changes the Tkinter Window title.
    WinCfg(300, 300)
    DFrame.pack(padx=0, pady=0) #Pady = Vertical spacing, Padx = Horizontal spacing

def Show_Ban():
    Bfile = "bin/banner.png"
    banner = Image.open(Bfile)
    w, h = 139.5, 35.37

    # Use CTkImage instead of ImageTk.PhotoImage
    Bimg = ctk.CTkImage(light_image=banner, size=(w, h))

    banlabel = ctk.CTkLabel(root, image=Bimg, text="", bg_color="#1E1E1E", width=w, height=h+15)
    banlabel.pack(fill="x", pady=0)

    BFrame.pack(padx=0, pady=10)

def Show_Reg():
    HideForms()
    root.title("Registration") #Changes the Tkinter Window title.
    WinCfg(300, 300)
    RFrame.pack(padx=0, pady=0)

def Show_Log():
    HideForms()
    root.title("Login") #Changes the Tkinter Window title.
    WinCfg(300, 300)
    LFrame.pack(padx=0, pady=0)

def Show_Pro(root, eml):
    HideForms()
    root.title("Your Profile") #Changes the Tkinter Window title.
    WinCfg(300, 700)

    recall = saveManager.recall(eml)
    if recall != "":
        eml, usr, desc, img = recall.split(", ")
    
    if img != "img":
        PimgData = b64.b64decode(img)
        Ppfp = Image.open(io.BytesIO(PimgData))
    else:
        Ppfp = Image.open("bin/defaultpfp.jpg")

    Ppfp = Ppfp.resize((200, 200)) #16:9 ratio
    Ppfp = ImageTk.PhotoImage(Ppfp)
    PButton = ctk.CTkButton(root, image=Ppfp, text="", fg_color="transparent", bg_color="transparent", hover_color="grey", command=Pro.pfp.newPfp)
    PButton.pack(pady=20)

    PEml.configure(state="normal")
    PEml.delete(0, "end")
    PEml.insert(0, eml)
    PEml.configure(state="readonly")

    PUsr.configure(state="normal")
    PUsr.delete(0, "end")
    PUsr.insert(0, usr)
    PUsr.configure(state="readonly")


    desc = desc.replace("\\n", "\n")
    PDesc.insert("1.0", desc)

    PFrame.pack(padx=0, pady=0)

# PROGRAM LOGIC FUNCTIONS

def Reg():
    print("[INFO] Executing Registration event")
        
    eml = RemlEntry.get() #]
    usr = RusrEntry.get() #] - Fetches user inputted credentials from Entry boxes.
    key = RkeyEntry.get() #]

    #~ Account Requirements ~#

    trip = False

    if len(key) < 8: #Checks if password shorter than 8 chars.
        trip = True

    if ',' in eml or ',' in usr or ',' in key: #Sanitises input from commas to prevent breakage
        trip = True

    if not '@' in eml or not '.' in eml: #Checks if email is valid. Looks for @ Symbol.
        trip = True
    
    if not any(c.isupper() for c in key) and any(c.islower() for c in key) and any(c.isdigit() for c in key): #Checks if there is a capital, lowercase letter and numbers included in the password. - Source: ONLINE FORM
        trip = True
    
    if saveManager.checkEml(eml) == True:
        trip = None
    
    #~ End Account Requirements ~#
    #~ Check if any account requirements have tripped ~#

    if trip == False:
        saveManager.create(eml, usr, key)
        messagebox.showinfo("Registration", "You have successfully signed up!")

        RemlEntry.delete(0, tk.END) # ]
        RusrEntry.delete(0, tk.END) # ] - Clears all of the text fields in Registration page.
        RkeyEntry.delete(0, tk.END) # ]

        Show_Log()

    elif trip == True:
        ans = messagebox.askquestion("Registration", "Invalid credentials. Would you like to see the requirements?")
        if ans == 'yes':
            req = [
                " - Password must be at least 8 characters long\n",
                " - Password must not contain any commas (,)\n",
                " - Email field must contain an email\n",
                " - Password must contain at least a captial and lowercase letter"
                " - Password must contain a number"
                ]
            messagebox.showinfo("Requirements", "Credential Requirements: \n" + "".join(req))
            return; return
    elif trip == None:
        print("[DEBUG] Account already exists...")
        messagebox.showerror("Registration", "Your account already exists... Please Sign in")

#LOGIN LOGIC

def Log():
    print("[INFO] Executing Login event")
    eml = LemlEntry.get()
    key = LkeyEntry.get()

    if not eml or len(key) < 6: #Checks if there is anything in the username box and if the password is at least 6 characters long
        messagebox.showerror("ERROR: Login Portal", "Invalid email or password")
        LkeyEntry.delete(0, tk.END)
        return
    
    if not saveManager.checkKey(eml, key):
        messagebox.showinfo("ERROR: Login Portal", "Credential Mismatch") # Warns user that credentials were wrong
        return
    #messagebox.showinfo("Success", "Login successful!") # Legacy asset
    Show_Pro(root, eml)

class Pro():
    
    def save():
        print("Saving profile changes...")
        eml = PEml.get()
        desc = PDesc.get("1.0", "end-1c")

        if ',' in desc:
            messagebox.showerror("Profile Update", "Description cannot contain commas (,)\n Your changes might not have been saved.")
        desc = desc.replace('\n', "\\n")
        desc = desc.replace(',', '')
        saveManager.modify(eml, desc)

    class pfp():
        def newPfp():
            eml = PEml.get()
            file = ctk.filedialog.askopenfilename(
                title="Select a Profile Picture",
                filetypes=[
                    ("Image files (jpg, jpeg, png)", "*.jpg;*.jpeg;*.png"),
                    ("JPEG files (jpg, jpeg)", "*.jpg;*.jpeg"),
                    ("PNG files (png)", "*.png")
                ]
            )

            if file != "":
                # Open the image file in binary mode
                with open(file, "rb") as img:
                    # Read the binary data
                    PfpData = img.read()
            
                     # Convert the binary data to a Base64 string
                    P64img = base64.b64encode(PfpData).decode("utf-8")
                    saveManager.modify(eml, image=P64img)

                    messagebox.showinfo("Profile Picture Update", "Profile picture updated successfully!\nPlease log out and log back in again to see the changes.")
                    exit()
                    





    def logout():
        print("Logging out...")
        PEml.delete(0, tk.END)
        PUsr.delete(0, tk.END)
        PDesc.delete("1.0", tk.END)
        Show_Debug()

    #NOT COMPLETE!! REFER TO PROFILE REFERENCE SHEET!




# GRAPHICS



""" Debugging Menu UI """



Dlabel = tk.Label(DFrame, text="Debug Menu"); Dlabel.pack()
regBtn = ctk.CTkButton(DFrame, text="Register", command=Show_Reg); regBtn.pack()
logBtn = ctk.CTkButton(DFrame, text="Login", command=Show_Log); logBtn.pack()
proBtn = ctk.CTkButton(DFrame, text="Profile", command=Show_Pro); proBtn.pack()



""" Login """



Llabel = tk.Label(LFrame, text="Login")
Llabel.grid(row=0, column=0)

LemlEntry = ctk.CTkEntry(LFrame, placeholder_text="Email")
LemlEntry.grid(row=1, column=0)

LkeyEntry = ctk.CTkEntry(LFrame, show="•", placeholder_text="Password")
LkeyEntry.grid(row=2, column=0)

logEntry = ctk.CTkButton(LFrame, text="Login", corner_radius=5, command=Log)
logEntry.grid(row=4, column=0, padx=2.5, pady=2.5)

logForgot = ctk.CTkButton(LFrame, text="I don't have an Account", corner_radius=5, command=Show_Reg)
logForgot.grid(row=5, column=0, padx=2.5, pady=2.5)



""" Register UI """



Rlabel = tk.Label(RFrame, text="Registration")
Rlabel.grid(row=0, column=0, padx=2.5, pady=2.5)

RemlEntry = ctk.CTkEntry(RFrame, placeholder_text="Email")
RemlEntry.grid(row=1, column=0, padx=0.5, pady=0.5)

RusrEntry = ctk.CTkEntry(RFrame, placeholder_text="Username")
RusrEntry.grid(row=2, column=0, padx=0.5, pady=0.5)

RkeyEntry = ctk.CTkEntry(RFrame, show="•",placeholder_text="Password")
RkeyEntry.grid(row=3, column=0, padx=0.5, pady=0.5)

regEntry = ctk.CTkButton(RFrame, text="Register", command=Reg)
regEntry.grid(row=4, column=0, padx=2.5, pady=2.5)

regExist = ctk.CTkButton(RFrame, text="I have an account", command=Show_Log)
regExist.grid(row=5, column=0, padx=2.5, pady=2.5)



""" Profile """



PLabel = tk.Label(PFrame, text="Profile")
PLabel.configure(font=GFontBold)
PLabel.grid(row=0, column=0, padx=2.5, pady=2.5)


#********


PEml = ctk.CTkEntry(PFrame, placeholder_text="Email not found.")

PEml.configure(state="readonly")
PEml.grid(row=2, column=0, padx=0.5, pady=0.5)

PUsr = ctk.CTkEntry(PFrame, placeholder_text="Username not found.")

PUsr.configure(state="readonly")
PUsr.grid(row=3, column=0, padx=0.5, pady=0.5)

PDesc = ctk.CTkTextbox(PFrame, width=250, height=275)
PDesc.grid(row=4, column=0, padx=0.5, pady=0.5)

Psave = ctk.CTkButton(PFrame, text="Save Changes", command=Pro.save)
Psave.grid(row=5, column=0, padx=2.5, pady=2.5)

PLogout = ctk.CTkButton(PFrame, text="Logout", command=Pro.logout)
PLogout.grid(row=6, column=0, padx=2.5, pady=2.5)

Show_Ban()
Show_Debug() # Starts the Debugging Menu, Utilised during program creation for convenience.

root.mainloop()