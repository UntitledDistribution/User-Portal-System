import customtkinter as ctk #In place for standard tkinter as it has more customisation options.
import os # Handling file directories cross-platform. 
import io
import base64 as b64
import saveManager # Utilise my own Library - Middleman of Saved data.
from tkinter import messagebox
from PIL import Image, ImageTk #Image handling


""" GLOBAL GUI Properties """


root = ctk.CTk() #Creating the main window.

global ww, wh

FontHead = ctk.CTkFont(family="Arial", size=24, weight="bold") #Heading font.
FontBold = ctk.CTkFont(family="Arial", size=18, weight="bold") #Bold font.
FontNorm = ctk.CTkFont(family="Arial", size=18) #Normal font.

root.option_add("*Font", FontNorm) #Default font

ctk.set_default_color_theme(os.path.join("bin", "theme.json")) #Setting the default theme to a modified custom version of the built-in 'green' theme. (CustomTkinter)

# Shared Window functions #

class window():

    def size(ww, wh, center=0):
        

        sw = root.winfo_screenwidth() #Screen width
        sh = root.winfo_screenheight() #Screen height

        x = (sw // 2) - (ww // 2) # MidPoint of X axis
        y = (sh // 2) - (wh // 2) # MidPoint of Y axis

        if center == 1:
            root.geometry(f"{ww}x{wh}+{x}+{y}") #Size window + Center window.
        else:
            root.geometry(f"{ww}x{wh}") #Only size window.
        
    def center(frame):
        banH = 15 #Height of banner - space to avoid to prevent overlapping.

        #frame.place(relx=0.5, rely=0.5, anchor="center") #LEGACY - Center positions frame to the window, ignoring the banner.
        

        # relx/rely center it, 'y' shifts it down by pixel count in banH
        frame.place(relx=0.5, rely=0.5, anchor="center", y=banH)
        

    def hide():
        RFrame.place_forget() #]
        LFrame.place_forget() #] - Hides each individual page. Notice how I miss the banner frame. thats because I want the banner to indefinitely be drawn to the Window.
        PFrame.place_forget() #]
        return #Go back to where this was called from.



""" CTK WINDOW PAGES """


BFrame = ctk.CTkFrame(root) #Banner Frame
RFrame = ctk.CTkFrame(root) #Registration Frame
LFrame = ctk.CTkFrame(root) #Login Frame
PFrame = ctk.CTkFrame(root) #Profile Frame

# Display class holds all of the UI elements and things that need to be done on each page before displaying to user.

class display():
    def banner():
        banner_path = os.path.join("bin", "banner.png")
        file = Image.open(banner_path) # Open the banner image.
        w, h = 139.5, 35.37 # displays width and height of the banner image in pixels.

        image = ctk.CTkImage(
            light_image=file,   #] - Specify the image for both light and dark mode
            dark_image=file,    #]
            size=(w, h), # Resize the banner image.
        )

        # Uses a label as a panel to display the banner image.
        panel = ctk.CTkLabel(
            BFrame, # Parent the label to the banner frame.
            image=image, 
            fg_color="#1E1E1E", #Banner background color
            width=w, 
            height=h+15, #Image height + additional 15 pixels to give banner padding on y-axis whilst still looking good.
            text="" #Prevents any default text from being displayed here.
            )
        panel.pack(fill="x") # Tells the banner to be displayed from edge-to-edge of the window.

        BFrame.pack(fill="x") # Shows the banner frame to the user and gives it space from next elements on y-axis by 10px.
    


    def login():
        window.hide() #Hides all other windows before displaying this page.
        root.title("Login") #Titles the open window to Login.

        global LemlEntry, LkeyEntry

        Llabel = ctk.CTkLabel(LFrame, text="Login", font=FontHead) #Header "Login" label
        Llabel.grid(row=0, column=0, pady=10) #Puts components in table order to ensure layout the same to mitigate layout issues.

        LemlEntry = ctk.CTkEntry(LFrame, placeholder_text="Email") #Email entry field
        LemlEntry.grid(row=1, column=0)

        LkeyEntry = ctk.CTkEntry(LFrame, placeholder_text="Password", show="•") #Password entry field - I searched for the symbol.
        LkeyEntry.grid(row=2, column=0)

        LlogEntry = ctk.CTkButton(LFrame, text="Login", command=logic.login) #Its a button that executes the 'command' argument when clicked.
        LlogEntry.grid(row=3, column=0, padx=2.5, pady=5) #Padx and Pady is spacing between the buttons on X and Y axis.

        LlogReg = ctk.CTkButton(LFrame, text="Don't have an account?", command=display.register) #Button to switch to registration page.
        LlogReg.grid(row=4, column=0, padx=2.5, pady=2.5)

        window.size(ww=300, wh=350, center=1) #Sizes the window to 300x350 and centers the window.
        LFrame.pack() #Shows the login frame to the user.
        window.center(LFrame) #Centers the login frame to the window.



    def register():
        window.hide()
        root.title("Register") #Renames the window title to 'Register'.

        global RemlEntry, RusrEntry, RkeyEntry

        Rlabel = ctk.CTkLabel(RFrame, text="Registration", font=FontHead) #Header "Register" label
        Rlabel.grid(row=0, column=0, pady=10)

        RemlEntry = ctk.CTkEntry(RFrame, placeholder_text="Email") #Email entry field
        RemlEntry.grid(row=1, column=0, padx=15, pady=0.5)

        RusrEntry = ctk.CTkEntry(RFrame, placeholder_text="Username") #Username entry field
        RusrEntry.grid(row=2, column=0, padx=15, pady=0.5)

        RkeyEntry = ctk.CTkEntry(RFrame, placeholder_text="Password", show="•") #Password entry field
        RkeyEntry.grid(row=3, column=0, padx=15, pady=3.5)

        RregButton = ctk.CTkButton(RFrame, text="Register", command=logic.register) #Registration button
        RregButton.grid(row=4, column=0, padx=15, pady=3.5)

        RexistButton = ctk.CTkButton(RFrame, text="Have an account?", command=display.login) #Registration button
        RexistButton.grid(row=5, column=0, padx=15, pady=3.5)

        window.size(ww=300, wh=350, center=0) #resizes window size to 300x350 but doesn't center.
        RFrame.pack(padx=0, pady=0) #Display the page.
        window.center(RFrame) #Centers the registration frame to the window.



    def profile(eml):
        window.hide()
        root.title("Profile") #Renames the window title to 'Profile'.

        global Peml, Pdesc

        fetch = saveManager.read.fetch(eml)
        if fetch != "":
            eml, usr, desc, img = fetch.split(", ")

        Plabel = ctk.CTkLabel(PFrame, text="Profile", font=FontHead) #Header "Profile" label
        Plabel.grid(row=0, column=0, pady=10)

        
        if img != "img":
            PimgData = b64.b64decode(img)
            Ppfp = Image.open(io.BytesIO(PimgData))
        else:
            Ppfp = Image.open("bin/defaultpfp.jpg")

        Ppfp = Ppfp.resize((100, 100))
        Ppfp = ImageTk.PhotoImage(Ppfp)
        PButton = ctk.CTkButton(PFrame, image=Ppfp, text="", fg_color="transparent", bg_color="transparent", hover_color="grey", command=logic.profile.updatePfp)
        PButton.grid(row=1, column=0, pady=5)



        Peml = ctk.CTkEntry(PFrame) #Email entry field

        Peml.configure(state="normal")
        Peml.delete(0, "end")
        Peml.insert(0, eml)
        Peml.configure(state="readonly")

        Peml.grid(row=2, column=0, padx=15, pady=0.5)


        Pusr = ctk.CTkEntry(PFrame) #Username entry field

        Pusr.configure(state="normal")      #]
        Pusr.delete(0, "end")               #]
        Pusr.insert(0, usr)                 #] - Adds information to Entry boxes and then sets them to readOnly, ensuring the user can't change the contents after registration
        Pusr.configure(state="readonly")    #]

        Pusr.grid(row=3, column=0, padx=15, pady=0.5)


        Pdesc = ctk.CTkTextbox(PFrame, width=250, height=275) #Description text box field (width & height in pixels)

        desc = desc.replace("\\n", "\n")
        Pdesc.insert("1.0", desc)

        Pdesc.grid(row=4, column=0, padx=15, pady=3.5)
        

        Psave = ctk.CTkButton(PFrame, text="Save", command=logic.profile.updateDesc) #Save button
        Psave.grid(row=5, column=0, padx=15, pady=3.5)


        Plogout = ctk.CTkButton(PFrame, text="Logout", command=logic.profile.logout) #Logout button
        Plogout.grid(row=6, column=0, padx=15, pady=3.5)


        window.size(ww=300, wh=650, center=1)
        PFrame.pack(padx=0, pady=0) #Display the page.

        window.center(PFrame) #Centers the profile frame to the window.



""" LOGIC FUNCTIONS """


class logic():

    def login():
        eml = LemlEntry.get()
        key = LkeyEntry.get()

        if eml == "":
            messagebox.showerror("Account Portal", "Invalid Credentials...\nPlease Try Again.")
            LkeyEntry.delete(0, ctk.END)
            return
        
        if saveManager.read.check.key(eml, key) == True:
            display.profile(eml)



    def register():
        eml = RemlEntry.get() #]
        usr = RusrEntry.get() #] - Fetches user inputted credentials from Entry boxes.
        key = RkeyEntry.get() #]

        """ REGISTRATION ACCOUNT REQUIREMENTS """

        trip = False # Defines the trip variable 

        if len(key) < 8: #Checks if password shorter than 8 chars.
            print("[INFO] Requirement Trip: Length")
            trip = True

        if ',' in eml or ',' in usr or ',' in key: #Sanitises input from commas to prevent breakage
            print("[INFO] Requirement Trip: Commas")
            trip = True

        if not '@' in eml or not '.' in eml: #Checks if email is valid. Looks for @ Symbol.
            print("[INFO] Requirement Trip: Not Email")
            trip = True
    
        if not any(c.isupper() for c in key) and not any(c.islower() for c in key) and not any(c.isdigit() for c in key):
            print("[INFO] Requirement Trip: Complexity")
            trip = True
    
        if saveManager.read.check.email(eml) == True:
            trip = None

        """ END ACCOUNT REQUIREMENT CHECKS """

        """ CHECK """

        if trip == False:
            saveManager.write.create(eml, usr, key)
            messagebox.showinfo("Registration", "You have successfully signed up!")

            RemlEntry.delete(0, ctk.END) # ]
            RusrEntry.delete(0, ctk.END) # ] - Clears all of the text fields in Registration page.
            RkeyEntry.delete(0, ctk.END) # ]

            display.login()

        elif trip == True:
            ans = messagebox.askquestion("Registration", "Invalid credentials. Would you like to see the requirements?")
            if ans == 'yes':
                req = [
                    " - Password must be at least 8 characters long\n",
                    " - Password must not contain any commas (,)\n",
                    " - Email field must contain an email\n",
                    " - Password must contain at least a capital and lowercase letter"
                    " - Password must contain a number"
                    ]
                messagebox.showinfo("Requirements", "Credential Requirements: \n" + "".join(req))
                return; return
        elif trip == None:
            print("[DEBUG] Account already exists...")
            messagebox.showerror("Registration", "Your account already exists... Please Sign in")
    
    #Profile Page Logic

    class profile():
        
        def updateDesc():
            eml = Peml.get()
            desc = Pdesc.get("1.0", "end-1c")

            if ',' in desc:
                messagebox.showerror("Profile Update", "Description cannot contain commas (,)\n Your changes might not have been saved.")
            
            desc = desc.replace('\n', "\\n")
            desc = desc.replace(',', '')
            saveManager.write.modify(eml, desc)



        def updatePfp():
            eml = Peml.get()
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
                    P64img = b64.b64encode(PfpData).decode("utf-8")

                    saveManager.write.modify(eml, img=P64img)

                    logic.profile.updateDesc()

                    logic.profile.logout(1)


        


        def logout(relog=0):

            eml = LemlEntry.get()

            if relog == 0:
                print("[INFO] Logging out...")
                window.hide()
                display.login()

            elif relog == 1:
                print("[INFO] Reloading...")
                window.hide()
                display.profile(eml)



display.banner() #Displays the banner to the screen before displaying any other menu to ensure it sticks at the top.
display.login()

root.mainloop()