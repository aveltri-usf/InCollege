import sqlite3
import re
import hashlib

class MenuMediator:
  ##Constructor
  ## Hold Menu Items Internally
    def __init__(self):
      self.selections = {}
      self.skillSelections = {}
    #destructor
    def __del__(self):
      pass #not sure what to include
    ## Set Each Menu Item for the  
    def setSelection(self,hotKey,selection):
      self.selections[hotKey] = selection
    def setSkillSelection(self,hotKey,selection):
      self.skillSelections[hotKey] = selection
    ## Displays Each Set Menu Item; System Class performs the action
   ##Display List
    def displayMainMenu(self):
      for hotKey,selection in self.selections.items():
        print("["+hotKey+"] "+ selection['label'])
      print("[0] Exit")
    ##Display List  
    def displaySkillMenu(self):
      for hotKey,selection in self.skillSelections.items():
        print("["+hotKey+"] "+ selection['label'])
      print("[0] Exit")
      
    def startEnviroment(self):
    ## Main Menu Loop
      while True:
        self.displayMainMenu()
        selection = input("Please, make a selection\n")
        if(selection == '0'):
          print("Exiting")
          break
        if selection in self.selections:
          thisSelection = self.selections[selection]
          menuItem = thisSelection['action']
          menuItem()
        else:
          print("Invalid Selection! Please Try Again")
          
class System:
  def __init__(self,loggedOn): #create and connect to db
    self.conn = sqlite3.connect("accounts.db") #establishes connection to SQLite database called accounts
    self.cursor = self.conn.cursor() #creates cursor object which is later used to execute SQL queries
    self.cursor.execute("CREATE TABLE IF NOT EXISTS accounts (username varchar2(25) PRIMARY KEY, password varchar2(12))") #execute method and cursor object are used to create table if one does not exist
    self.conn.commit() #commit method used to save changes
    ##Instantiate User Class Here ???
    self.loggedOn = loggedOn
    self.mediator = MenuMediator()

  def __del__(self): #closes connection to db
    self.conn.close() #closes connection to database
    
  def encryption(self, password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    hashed_pass = sha256.hexdigest()
    return hashed_pass

  ##Will need removed after testing is completed
  def deleteTable(self):
    confirm = input("Are you sure you want to delete the current accouns in the database? This operation cannot be undone. (Y/N): ")
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
        print("No records found in the table.")

  def countRows(self):
    ##Current Number of Accounts
    self.cursor.execute("SELECT COUNT(*) FROM accounts")
    count = self.cursor.fetchone()[0]
    return count

  def validatePassword(self, password,password_check): #validate password
    ## Confirm
    if(password != password_check):
      print("Passwords must match")
      return False
    ## Password Limits using Regex  
    if len(password) < 8 or len(password) > 12:
      print("Password must be 8-12 Characters in Length")
      return False
    if not re.search("[A-Z]", password):
      print("Password must contain at least one upper case letter")
      return False
    if not re.search("[0-9]", password):
      print("Password must contain at least one number")
      return False 
    if not re.search(r'[\!@#\$%\^&\*\(\)_\+\-\=\[\]\{\}\|\;\:\,\.\<\>\/\?\`\~\'\"\\]', password):
      print("Password must contain at least one special character")
      return False
    return True
    
  def validateUserName(self, userName): #validate Username
      self.cursor.execute("SELECT * FROM accounts WHERE username=?", (userName,))
      exists_user = self.cursor.fetchone()
      if exists_user:
        print("Username has been taken.")
        return False
       #arbitrary limit 
      if len(userName) < 1 or len(userName) > 25:
        print("Username must be 1-25 Characters in Length")
        return False
      return True

  def login(self, username, password): #login check
      self.cursor.execute("SELECT * FROM accounts WHERE username = ?", (username,)) 
      #? is placeholder for username
      account = self.cursor.fetchone() #fetches first row which query returns
      if account: #if the username exists, then we check that the password in the database matches the password the user inputted
        hashed_inputpass = self.encryption(password)
        if hashed_inputpass == account[1]:
          print("You have successfully logged in!")
          return True
        else:
          print("Invalid username/password, try again!")
          return False
      else:
        print("Account not found, check credentials.")
      return False
      
  def register(self, username, password, password_check):
    ## Set Account Limit
    if self.countRows() >= 5:
      print("Maximum number of accounts created!")
      return False
    ## Validate Inputs
    if self.validatePassword(password,password_check) and self.validateUserName(username):
    
      encrypted_pass = self.encryption(password)
      self.cursor.execute("INSERT INTO accounts (username, password) VALUES (?, ?)", (username, encrypted_pass))
      self.conn.commit() #saving new account to database
      print("Account created successfully.")
      return True
    return False
    
  def loginMenu(self):
    print("Welcome to the InCollege sign in page!\n")
    print("[0] Exit \n[1] Login \n[2] Create Account\n")
    choice = input()
    while(True):
        if(choice == '0'):
          break
        if not(self.loggedOn):
          if(choice == "1"):
            print("Log In:\n")
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            self.loggedOn = self.login(username, password)
          elif(choice == "2"):
            registered = False
            print("Account Creation:\n")
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            passwordCheck = input("Confirm Password: ")
            registered = self.register(username, password, passwordCheck)
            if(registered == True):
              choice = "1"
            else:
              choice = input("[0] Exit \n[1] Login \n[2] Create Account\n")
          elif(choice == "8"):
            self.deleteTable()
            choice = input("[1] Login [2] Create Account [0] Exit\n")
          elif(choice == "9"):
            self.printTable()
            choice = input("[1] Login [2] Create Account [0] Exit\n")
          else:
            print("Incorrect input. Please try again.")
            choice = input("[1] Login [2] Create Account [0] Exit\n")
        else:
          break
  def mainMenu(self):
      ##Set Main Menu Items
      self.mediator.setSelection('1',{'label':'Job/Internship Search','action':self.jobsMenu})
      self.mediator.setSelection('2',{'label':'Find A Friend','action':self.friendMenu})
      self.mediator.setSelection('3',{'label':'Learn a Skill','action':self.skillsMenu})
      #Set Skill Items
      self.mediator.setSkillSelection('1',{'label':'Learn Skill A','action':self.skillA})
      self.mediator.setSkillSelection('2',{'label':'Learn Skill B','action':self.skillB})
      self.mediator.setSkillSelection('3',{'label':'Learn Skill C','action':self.skillC})
      self.mediator.setSkillSelection('4',{'label':'Learn Skill D','action':self.skillD})
      self.mediator.setSkillSelection('5',{'label':'Learn Skill E','action':self.skillE})
      #Start Main Menu Loop
      self.mediator.startEnviroment()
  ## Sub Menus
  ## Plan to make a menu class object to simplify these
  def jobsMenu(self):
      print("Under Construction")
  def friendMenu(self):
      print("Under Construction")
  def skillsMenu(self):
      while True:
        self.mediator.displaySkillMenu()
        choice = input("Make a Selection to Learn A Skill: ")
        if(choice == '0'):
          break
        if choice in self.mediator.skillSelections:
          thisSelection = self.mediator.skillSelections[choice]
          menuItem = thisSelection['action']
          menuItem()
        else:
          print("Invalid Selection! Please Try Again")
  ## Skills to Learn
  ## Needs to Skill Object
  def skillA(self):
      print("Learn Skill A")
      print("Under Construction")
  def skillB(self):
      print("Learn Skill B")
      print("Under Construction")
  def skillC(self):
      print("Learn Skill C")
      print("Under Construction")
  def skillD(self):
      print("Learn Skill D")
      print("Under Construction")
  def skillE(self):
      print("Learn Skill E")
      print("Under Construction")