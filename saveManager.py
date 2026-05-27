import os

# ~ # VARIABLES
ud = "data.list"

# ~ # FILE DEPENDENCY
if not os.path.isfile(ud):
    with open(ud, "w") as file: #New text document, Write access
        pass #Create file

# ~ # WRITE DATA TO SAVE - Utilised in Registration Page

def create(eml, usr, key, desc="Enter a Description", image="img"): #Creating a function and declaring variables in that order of input. This function allows creation of account

    with open(ud, "a") as file: # *********************
        file.write(f"\n{eml}, {usr}, {key}, {desc}, {image}")
""" SOMETHING TO IMPROVE ON - Store password in Hash, Compare Hashed saved password with new hash to validate password """


# ~ # MODIFY USER DATA - Utilised in Profile Page to update description and image
def modify(eml, desc="", image=""):
    """
    Updates the desc / img for the user with the given email.
    Only the fields provided will be updated. The Login info does not get updated.
    """
    # Read all lines from the file
    with open(ud, "r") as file:
        lines = file.readlines()
    
    # Prepare the new lines
    new_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            new_lines.append(line)
            continue
        try:
            emlRecall, usrRecall, keyRecall, descRecall, imgRecall = line.split(', ')
            if emlRecall == eml:
                # Use new values if provided, otherwise keep the old ones
                new_desc = desc if desc != "" else descRecall
                new_image = image if image != "" else imgRecall
                # Create the updated line
                new_line = f"{emlRecall}, {usrRecall}, {keyRecall}, {new_desc}, {new_image}"
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        except ValueError:
            new_lines.append(line)
    
    # Write all lines back to the file
    with open(ud, "w") as file:
        for line in new_lines:
            file.write(f"{line}\n")


# ~ # Securely checks if the user's password is correct by returning true / false - Utilised in Login Page
def checkKey(eml, key):
    with open(ud, "r") as file:
        lines = file.readlines()
        for line in lines:
            try:
                emlRecall, usrRecall, keyRecall, descRecall, imgRecall = line.strip().split(', ')
                #Have to keep usrRecall in as thats how its formatted in the text document. Without it, it would be reading the username as the password.
                if emlRecall == eml and keyRecall == key: #Compare against input information and save
                    return True
            except:
                continue
    return False

#Checks if an email is already registered
def checkEml(eml):
    with open(ud, "r") as file:
        lines = file.readlines()
        for line in lines:
            try:
                emlRecall, _, _, _, _ = line.strip().split(', ')
                if emlRecall == eml:
                    return True
            except ValueError:
                # Skip malformed lines
                continue
    return False   


def recall(eml):
    with open(ud, "r") as file:
        for line in file:
            line = line.strip()
            if line != "":  #Checks if the line was actually visible
                try:
                    email, username, password, description, image = line.split(", ")
                    if email == eml:
                        return f"{email}, {username}, {description}, {image}"
                except:
                    continue
    return None   