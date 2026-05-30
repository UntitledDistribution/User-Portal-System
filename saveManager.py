import hashlib as hl
import os

""" VARIABLES """

ud = os.path.join("bin", "data.list") # "ud" stands for "user data". This variable is the file location of the 'data.list' file.

""" CHECK FILE EXIST """

if not os.path.exists(ud): #Checks if the 'data.list' file exists.
    with open(ud, "w") as f: # If it doesn't exist, create it. The "w" means "write", as we are adding the file.
        f.write("") # Write an empty file - Could also use 'pass' here as alternative.

""" LOGIC """

def hash(key):

    binary = key.encode() # Encode the password to bytes
    hash = hl.sha256(binary) # Hash the password using SHA-256 algorithm
    hashHex = hash.hexdigest() # Convert the hash to hexadecimal format
    return hashHex


""" WRITE DATA """


class write():

    #Create account function - Used in Registration.
    def create(eml, usr, key, desc="Enter a Description", img="img"):
        
        # Hash the 'key' variable for enhanced security. I used hashlib.
        key = hash(key) # Use the hash function to convert key to hash before saving.

        with open(ud, "a") as f: 
            f.write(f"{eml}, {usr}, {key}, {desc}, {img}\n") #Writes the email, username, hashed password, description and image name to the 'data.list' file. Each piece of data is separated by a comma and space for easy retrieval later. The "a" means "append", as we are adding to the file.
    
    
    def modify(eml, desc="", img=""):
        """
        Description and image variable contain a DEFAULT variable of nothing.
         This ensures no errors are caused for if the user only decides to only modify just the description or image.
        """

        with open(ud, "r") as f:
            lines = f.readlines()
    
        newLines = []

        for line in lines:
            line = line.strip()
        
            # Skip empty lines entirely
            if line == "":
                continue

            try:
                # Attempt to parse the line
                parts = line.split(", ")
                if len(parts) != 5:
                    # If line is malformed, keep it as is
                    newLines.append(line)
                    continue

                emlFetch, usrFetch, keyFetch, descFetch, imgFetch = parts

                if emlFetch == eml:
                    # Apply modifications
                    newDesc = desc if desc != "" else descFetch
                    newImg = img if img != "" else imgFetch
                
                    newLine = f"{emlFetch}, {usrFetch}, {keyFetch}, {newDesc}, {newImg}\n"
                    newLines.append(newLine)
                else:
                    # Keep other users' data unchanged
                    newLines.append(line)
                
            except ValueError:
                # Handle any unexpected parsing errors
                newLines.append(line)
    
        with open(ud, "w") as f:
            for line in newLines:
                f.write(line)
        

""" READ DATA"""


class read():

    # CHECK ACCOUNT INFORMATION
    class check():
        
        def email(eml):

            with open(ud, "r") as f:
                lines = f.readlines()

                for line in lines:
                    try:
                        emlFetch, _, _, _, _ = line.split(", ") # We only need the email, skip the rest using underscore (_).

                        if emlFetch == eml:
                            return True # If the email exists in the file, return True.
                        
                    except ValueError: # If the line has an abnormal amount of variables (!=5), skip it.
                        continue
                return False # If the email doesn't match, return False.


        def key(eml, key):

            key = hash(key) # Hash the key so if it was right, it would be identical to the key inside the saved file.

            with open(ud, "r") as f:

                lines = f.readlines()
                for line in lines:

                    try:
                        emlFetch, _, keyFetch, _, _ = line.split(", ") # We only need the email and key, skip the rest using underscore (_).

                        if emlFetch == eml: # If the email matches the one in the file, check the password.
                            if keyFetch == key: # If the hashed key matches the hashed key in the file, return True.
                                return True
                            else:
                                return False # If the hashed key doesn't match the hashed key in the file, return False.
                    except:
                        continue
        
    def fetch(fetchEml):
        with open(ud, "r") as f:
            for line in f:
                line = line.strip()

                if line != "": #Checks if the line actually contained anything...
                    try:
                        eml, usr, _, desc, img = line.split(", ")
                        if fetchEml == eml:
                            return f"{eml}, {usr}, {desc}, {img}"
                    except:
                        continue
        return None