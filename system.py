import sqlite3
import re
import hashlib
from user import User
import os

class Menu:
  ## Constructor
  ## Hold Menu Items Internally
    def __init__(self):
      self.opening = ""
      self.selections = {}
      
    #destructor
    def __del__(self):
      print('Menu Deconstructed')
    def clear(self):
        if os.name == 'nt':
            _ = os.system('cls')
        else:
            _ = os.system('clear')
    ## Set Each Menu Item for the  
    def setSelection(self,hotKey,selection):
      self.selections[hotKey] = selection
    def setOpening(self,opening):
      self.opening = opening
    ## Displays Each Set Menu Item; System Class performs the action
    ## Display List
    def displaySelections(self):
      print(self.opening)
      for hotKey,selection in self.selections.items():
        print("["+hotKey+"] "+ selection['label'])
      print("[0] Exit")
    ## Display List  
    def start(self):
    ## Main Menu Loop
      while True:
        self.displaySelections()
        selection = input()
        if(selection == '0'):
          print("Exiting")
          self.clear()
          break
        if selection in self.selections:
          self.clear()
          thisSelection = self.selections[selection]
          menuItem = thisSelection['action']
          menuItem()
        else:
          print("Invalid Input. Please Try Again")
 
class System:
  def __init__(self): #create and connect to db
    self.conn = sqlite3.connect("accounts.db") #establishes connection to SQLite database called accounts
    self.cursor = self.conn.cursor() #creates cursor object which is later used to execute SQL queries
    self.cursor.execute("CREATE TABLE IF NOT EXISTS accounts (username varchar2(25) PRIMARY KEY, password varchar2(12), fName varchar2(25), lName varchar2(25))") #execute method and cursor object are used to create table if one does not exist
    self.conn.commit() #commit method used to save changes
    ## Instantiate User Class Here ???
    self.user = User("guest","","",False)
    ## Menus
    self.homePage = Menu()
    self.mainMenu = Menu()
    self.jobsMenu = Menu()
    self.friendMenu = Menu()
    self.videoMenu = Menu()
    self.skillsMenu = Menu()
    self.guestSearch = Menu()
    self.joinMenu = Menu()
    
  def __del__(self): #closes connection to db
    self.conn.close() #closes connection to database
  #System Level Controls for Menus    
  def home_page(self):
   if not(self.user.loggedOn):
     self.homePage.start()
   else:
     self.mainMenu.start()
  def main_menu(self):
      self.mainMenu.start()
  def jobs_menu(self):
      self.jobsMenu.start()
  def friend_menu(self):
      self.friendMenu.start()
  def video_menu(self):
      self.videoMenu.start()
  def skills_menu(self):
      self.skillsMenu.start()
  def join_menu(self):
      self.joinMenu.start()
    
  def encryption(self, password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    hashed_pass = sha256.hexdigest()
    return hashed_pass

  ##Will need removed after testing is completed
  def deleteTable(self):
    print("Are you sure you want to delete the current accounts in the database? This operation cannot be undone. (Y/N): ")
    confirm = input()
    if confirm.upper() == "Y":
      self.cursor.execute("DROP TABLE IF EXISTS accounts")
      self.conn.commit()
      print("Table deleted successfully.")
    else:
      print("Deletion operation canceled.")
   ##Will need removed after testing is completed   
  def printTable(self):
    self.cursor.execute("SELECT * FROM accounts")
    rows = self.cursor.fetchall()
    if rows:
      print("Username\tPassword")
      for row in rows:
        print(f"{row[0]}\t\t{row[1]}")
    else:
        print("No Records Found In The Table.")

  def countRows(self,tableName):
    ##Current Number of Accounts
    query = "SELECT COUNT(*) FROM {}".format(tableName)
    self.cursor.execute(query)
    count = self.cursor.fetchone()[0]
    return count
    
  def validName(self,fName,lName):
    if len(fName) < 1 or len(fName) > 23:
      print("First Name Must Be 1-23 Characters In Length")
      return False
    if len(lName) < 1 or len(lName) > 23:
      print("Last Name Must Be 1-23 Characters In Length")
      return False
    return True

  def validatePassword(self, password,password_check): #validate password
    ## Confirm
    if(password != password_check):
      print("Passwords Must Match")
      return False
    ## Password Limits using Regex  
    if len(password) < 8 or len(password) > 12:
      print("Password Must Be 8-12 Characters In Length")
      return False
    if not re.search("[A-Z]", password):
      print("Password Must Contain At Least One Upper Case Letter")
      return False
    if not re.search("[0-9]", password):
      print("Password Must Contain At Least One Number")
      return False 
    if not re.search(r'[\!@#\$%\^&\*\(\)_\+\-\=\[\]\{\}\|\;\:\,\.\<\>\/\?\`\~\'\"\\]', password):
      print("Password Must Contain At Least One Special Character")
      return False
    return True
    
  def validateUserName(self, userName): # validate Username
      self.cursor.execute("SELECT * FROM accounts WHERE username=?", (userName,))
      exists_user = self.cursor.fetchone()
      if exists_user:
        print("Username Has Been Taken.")
        return False
       #arbitrary limit 
      if len(userName) < 1 or len(userName) > 25:
        print("Username Must Be 1-25 Characters in Length")
        return False
      return True

  def login(self): #login check
      print("Log In:\n")
      print("Enter Username: ")
      userName = input()
      print("Enter Password: ")
      password = input()
      ##Validate User Name and Password then Search
      self.cursor.execute("SELECT * FROM accounts WHERE username = ?", (userName,)) 
      #? is placeholder for username
      account = self.cursor.fetchone() #fetches first row which query returns
      if account: #if the username exists, then we check that the password in the database matches the password the user inputted
        hashed_inputpass = self.encryption(password)
        if hashed_inputpass == account[1]:
          print("You Have Successfully Logged In!")
          self.user.login(userName,account[2],account[3])
          self.home_page()
        else:
          print("Invalid Username/Password, Try Again!")
      else:
        print("Account Not Found, Check Username/Password.")
      
  def register(self):
    ## Set Account Limit
    if self.countRows("accounts") >= 5:
      print("Maximum Number Of Accounts Created!")
      return
    print("Enter Username: ")
    username = input()
    print("Enter First Name: ")
    fName = input()
    print("Enter Last Name: ")
    lName = input()
    print("Enter Password: ")
    password = input()
    print("Confirm Password: ")
    passwordCheck = input()
    ## Validate Inputs
    if self.validatePassword(password,passwordCheck) and self.validateUserName(username) and self.validName(fName,lName):
      encrypted_pass = self.encryption(password)
      self.cursor.execute("INSERT INTO accounts (username, password,fName,lName) VALUES (?, ?, ?, ?)", (username, encrypted_pass,fName,lName))
      self.conn.commit() #saving new account to database
      print("Account created successfully.")
      self.login()
      return 
    else:
      print("Account Creation Failed.")
    return

  #This is the function to find someone they know in the system
  def findUser(self):
    #Prompts for searching by first name and last name
    print("Enter First Name: ")
    fName = input()
    print("Enter Last Name: ")
    lName = input()

    # Search for the user in the database
    self.cursor.execute(
        "SELECT * FROM accounts WHERE fName = ? AND lName = ?",
        (fName, lName),
    )
    result = self.cursor.fetchall()

    #If the user is found, print 
    if len(result) > 0:
      print("They are part of the InCollege system.")
      self.join_menu()
    else:
      print("They are not yet a part of the InCollege system.")
      self.home_page()
    
    
  
  ## Sub Menu
  ## Plan to make a menu class object to simplify these
  ## Skills to Learn
  def skillA(self):
      print("Project Managment")
      print("Under Construction")
  def skillB(self):
      print("Networking")
      print("Under Construction")
  def skillC(self):
      print("System Design")
      print("Under Construction")
  def skillD(self):
      print("Coding")
      print("Under Construction")
  def skillE(self):
      print("Professional Communication")
      print("Under Construction")
  def guestSearch(self):
      print("Professional Communication")
      print("Under Construction")
  def initMenu(self):
      ## Set Home Page Items
      self.homePage.setOpening("Welcome to Our Home Page:")
      self.homePage.setSelection('1',{'label':'Login','action':self.login})
      self.homePage.setSelection('2',{'label':'Register','action':self.register})
      self.homePage.setSelection('3',{'label':'Search Users','action':self.guestSearch})
      self.homePage.setSelection('4',{'label':'Delete Users','action':self.deleteTable})
      self.homePage.setSelection('5',{'label':'See Cool Video','action':self.video_menu})
      self.homePage.setSelection('6',{'label':'Find People I Know','action':self.findUser}) #For finding people you know
      ## Set Video Page Items
      self.videoMenu.setOpening("See Our Success Story:\n(Playing Video)\n")
      ## Set Main Menu Items
      self.mainMenu.setOpening("Welcome User!")
      self.mainMenu.setSelection('1',{'label':'Job/Internship Search','action':self.jobs_menu})
      self.mainMenu.setSelection('2',{'label':'Find A Friend','action':self.friend_menu})
      self.mainMenu.setSelection('3',{'label':'Learn A Skill','action':self.skills_menu})
      # Set Skill Items
      self.skillsMenu.setOpening("Please Select a Skill:")
      self.skillsMenu.setSelection('1',{'label':'Project Managment','action':self.skillA})
      self.skillsMenu.setSelection('2',{'label':'Networking','action':self.skillB})
      self.skillsMenu.setSelection('3',{'label':'System Design','action':self.skillC})
      self.skillsMenu.setSelection('4',{'label':'Coding','action':self.skillD})
      self.skillsMenu.setSelection('5',{'label':'Professional Communication','action':self.skillE})
      self.joinMenu.setOpening("Would you like to join your friends on InCollege?")
      self.joinMenu.setSelection('1',{'label':'Login','action':self.login})
      self.joinMenu.setSelection('2',{'label':'Register','action':self.register})
      self.joinMenu.setSelection('3',{'label':'Return to Welcome Menu','action':self.home_page})