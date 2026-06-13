# Python User Portal System
This is a basic Python authentication system where a plaintext file in form of "data.list" is utilised by the saveManager.py file to store user credentials. 
This authentication system is only used to demonstrate my skills in Python and utilising Tkinter, CustomTkinter and TTKBootstrap.

## What is this used for?


## Usecase
Purely to demonstrate skills with a Basic User Account System.
You are more than welcome to copy my work for your own usecase but please give credit where necessary to this GitHub Repository.

# Python Dependancies
Some Libraries need to be installed, this can vary depending on the version you are intending to install.

## How to install libraries in Python...
You have two options, you can run the install.bat file provided in the releases and will be specific to that version, or you can manually install the Python dependancies.

You can manually install the dependancies in python using the built-in package manager.
Steps may vary depending on your Operating System, but for this guide, I will be giving Microsoft Windows specific instructions.
 1. Open your preferred CLI application
 2. Navigate to your Python Environment path, in Windows it can be typically found in your 'Program Files' or 'AppData' folder.
 3. After finding the Python executable, run the following:
```shell
./python.exe -m pip install [PACKAGE_NAME]
```
Where PACKAGE_NAME is an item of the list provided below to get the script to work.

## Solution Dependancies
Dark mode - Introduced automatically thanks to full migration to CustomTkinter
Reduced amount of code - Clear and Concise
Cross-platform - Thanks to using the IO library to navigate directories.
More Comments - The portal system is now easier to be understood by other programmers.

The dependent libraries for this script are as followed:
 - Tkinter (Deliver messages to the user)
 - CustomTkinter (UI Customisation)
 - Pillow (Image rendering)


# Details
This section will cover the files / scripts in my program and why they are needed.


## main.py
This script runs the logic and interface of the program utilising CustomTkinter to display content to the user. It is used to scoop user inputted information to communicate with saveManager to save and recall user infromation.

Here are the three pages that are included in my program:

| Login Page | Profile Page | Registration Page |
| ---------- | ------------ | ----------------- |
|<img width="210" height="266" alt="LPreview" src="https://github.com/user-attachments/assets/c84ea39e-083b-4e27-896a-ddda205b0426" /> | <img width="209" height="471" alt="PPage" src="https://github.com/user-attachments/assets/601e0c33-9068-4d45-843b-a98bb1ab23d1" /> | <img width="209" height="264" alt="RPreview" src="https://github.com/user-attachments/assets/7b649d58-0dcc-4b76-b8aa-2cbfa9b9c73d" /> |

The main.py script also has requirements during registration and ensures the program remains stable without breakage (hopefully! - Bug fixes are released to mitigate this.)


## saveManager.py
This script is essentially the middle-man that is utilised in main.py as a library.
If the data.list file doesn't exist, it gets created with nothing inside to prevent errors.
This allows for the main.py document to be more efficient when handling read and writes between the main.py and data.list file

## reqManager.py
This script is treated like a library / dependancy in my program. It is needed to check inputted user credentials against the account requirements to ensure it meets a set of rules such as a password needing to be longer than 8 characters long, Whilst it would be possible to merge this file into the ```main.py``` file, I have chosen it to be an external file so it is easier for others to understand and modify the file without even needing an advanced understanding of Python, you can modify the requirements with simplicity.

## data.list
The user records are stored here in a CSV / PlainText format where User Information is formatted as:
```shell
Email, Username, Password (SHA-256), Description, Image/pfp (base64 format)
```
and if you was to execute the program or review the code you'd notice there would be some default values such as the Description and Image.
This is to prevent the program from causing errors when spliting the commas and assigning the variables. The default values for the description and image is:
```shell
..., ..., ..., This is a Description!, img
```
If the image variable is set as 'img' it will default to the default profile image located in bin\defaultpfp.jpg otherwise, the program will assume its a Base64 string and will try to render the string as an image.
