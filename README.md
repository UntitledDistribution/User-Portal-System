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

## Initial Release: v1.0
This is the very first version of my authentication system and i'm aware this version is extremely inefficient and may not be as cross-platform friendly as I had hoped.
for this version, you need to install the following via Python's package manager
 - tkinter
 - pillow
 - customtkinter


# Details
This section will cover the files / scripts in my program and why they are needed.

## saveManager.py
This script is essentially the middle-man that is utilised in main.py as a library.
If the data.list file doesn't exist, it gets created with nothing inside to prevent errors.
This allows for the main.py document to be more efficient when handling read and writes between the main.py and data.list file


## data.list
The user records are stored here in a CSV / PlainText format where User Information is formatted as:
```shell
Email, Username, Password, Description, Image/pfp (base64 format)
```
and if you was to execute the program or review the code you'd notice there would be some default values such as the Description and Image.
This is to prevent the program from causing errors when spliting the commas and assigning the variables. The default values for the description and image is:
```shell
..., ..., ..., This is a Description!, img
```
If the image variable is set as 'img' it will default to the default profile image located in bin\defaultpfp.jpg
