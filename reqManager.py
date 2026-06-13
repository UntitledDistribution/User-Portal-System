from tkinter import messagebox
import saveManager

def trip(eml="", usr="", key=""):


    """ REGISTRATION ACCOUNT REQUIREMENTS """


    trip = False # Defines the trip variable 

    if len(key) < 8: #Checks if password shorter than 8 chars.
        #print("[INFO] Requirement Trip: Length")
        trip = True

    if ',' in eml or ',' in usr or ',' in key: #Sanitises input from commas to prevent breakage
        #print("[INFO] Requirement Trip: Commas")
        trip = True

    if not '@' in eml or not '.' in eml: #Checks if email is valid. Looks for @ Symbol.
        #print("[INFO] Requirement Trip: Not Email")
        trip = True
    
    if not any(c.isupper() for c in key) and not any(c.islower() for c in key) and not any(c.isdigit() for c in key):
        #print("[INFO] Requirement Trip: Complexity")
        trip = True
    
    #if saveManager.read.check.publicInfo(eml, usr) == True:
    #    trip = None


        """ END ACCOUNT REQUIREMENT CHECKS """

    #VIOLATED PASSWORD REQUIREMENTS
    if trip == True:
        ans = messagebox.askquestion("Requirements", "Invalid credentials. Would you like to see the requirements?")
        if ans == 'yes':
            req = [
                " - Password must be at least 8 characters long\n",
                " - Password must not contain any commas (,)\n",
                " - Email field must contain an email\n",
                " - Password must contain at least a capital and lowercase letter\n"
                " - Password must contain a number"
                ]
            messagebox.showinfo("Requirements", "Credential Requirements: \n" + "".join(req))
        return True #Returns 'True' because the requirements have been violated.
    
    #PASS REQUIREMENTS
    elif trip == False:
        return False

    #EXISTING ACCOUNT
    elif trip == None:
        print("[DEBUG] Account already exists...")
        messagebox.showerror("Registration", "Your account already exists... Please Sign in")
        return None
    



    