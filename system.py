import sqlite3
import re
import hashlib
from user import User
import os

#list of languages currently supported by InCollege
LANGUAGES = ('English', 'Spanish')
MSG_ERR_RETRY = "Your Request Could Not Be Competed at This Time.\nPlease Try Again Later."

class Jobs:
    def __init__(self, title, employer, location, salary, posterFirstName, posterLastName, description=None):
        self.title = title
        self.description = description
        self.employer = employer
        self.location = location
        self.salary = salary
        self.posterFirstName = posterFirstName
        self.posterLastName = posterLastName
  
class Menu:
  ## Constructor
  ## Hold Menu Items Internally
    def __init__(self):
      self.opening = ""
      self.exitStatement = "Exit"
      self.selections = []  # full list of selections(label, action, visibiliity) for the menu
      self.currSelections = [] # dyanmic list of menu selections that is updated every iteration of the menu

  
    #destructor
    def __del__(self):
      # print('Menu Deconstructed')
      pass
      
    ##clear console  
    def clear(self):
        if os.name == 'nt':
            _ = os.system('cls')
        else:
            _ = os.system('clear')

  
    ## Set Each Menu Item for the menu
    ## addItem function simply takes in menu option name and then function name
    def addItem(self, item, func, vis = lambda: True):
        self.selections.append({'label': item, 'action': func, 'visible': vis})

  
    def setOpening(self,opening):
      self.opening = opening

  
    def setExitStatement(self,exit):
      self.exitStatement = exit


    def getValidSelections(self):
      """
      Generates a list of valid selections for the menu based on 
      the current visibility of each selection in the menu's full list of selections
      """
      return [sel for sel in self.selections if sel['visible']()]
  
    ## Displays Each Set Menu Item; System Class performs the action
    ## Display List
    def displaySelections(self):
        print(f"{self.opening}\n")
        for idx, sel in enumerate(self.currSelections, start=1):
          label = sel['label']
          if callable(label):  # allow functions to be used as dynamic labels
            label = label()
          print(f"[{idx}] {label}")
        print(f"[0] {self.exitStatement}")

  
    # Function to take in number as selection
    def selectOption(self):
        while True:
            try:
                choice = int(input("\nEnter the number of your selection: "))
                if choice < 0 or choice > len(self.currSelections):
                    raise ValueError()
                return choice
            except ValueError:
                print("Invalid selection. Please try again.")

  
    def start(self):
    #Main menu loop
      selection = None
      while True:
        self.currSelections = self.getValidSelections()
        if selection is None:  # skip displaying menu & prompting user if previous selection set new selection
          #Displays selections and stores what the user chooses
          self.displaySelections()
          selection = self.selectOption()
        
        if selection == 0:
          print("Exiting")
          self.clear()
          break
        elif callable(selection):  # the previous selection returned another function
          selection = selection()
        else:
          self.clear()
          selection = self.currSelections[selection - 1]
          selection = selection['action']() # current function may return a new selection



class System:
  def __init__(self): #create and connect to db
    self.conn = sqlite3.connect("accounts.db") #establishes connection to SQLite database called accounts
    self.cursor = self.conn.cursor() #creates cursor object which is later used to execute SQL queries
    self.cursor.execute("CREATE TABLE IF NOT EXISTS accounts (username varchar2(25) PRIMARY KEY, password varchar2(12), fName varchar2(25), lName varchar2(25))") #execute method and cursor object are used to create table if one does not exist
    self.conn.commit() #commit method used to save changes
    # SQL code to create the jobs table if one does not exist
    create_jobs_table = """
    CREATE TABLE IF NOT EXISTS jobs (
      title VARCHAR(128) PRIMARY KEY,
      description TEXT,
      employer VARCHAR(128) NOT NULL,
      location VARCHAR(128) NOT NULL,
      salary INT NOT NULL,
      posterFirstName VARCHAR(128),
      posterLastName VARCHAR(128)
    );
    """
    # Execute the SQL code
    self.cursor.execute(create_jobs_table)
    
    # Commit the transaction
    self.conn.commit()

    #create account settings table
    table_acc_settings = """
    CREATE TABLE IF NOT EXISTS account_settings (
      username VARCHAR(25) PRIMARY KEY, 
      email BOOLEAN,
      sms BOOLEAN,
      targetedAds BOOLEAN,
      language VARCHAR(12),
      FOREIGN KEY(username) REFERENCES accounts(username));
    """
    self.cursor.execute(table_acc_settings)
    self.conn.commit()

    #create trigger add account settings trigger on accounts table
    default_lang = LANGUAGES[0].replace("'", "''")
    default_lang = f"'{default_lang}'"
    trigger_add_settings = f"""
    CREATE TRIGGER IF NOT EXISTS add_acc_settings
    AFTER INSERT ON accounts
    BEGIN
      INSERT INTO account_settings (username, email, sms, targetedAds, language)
      VALUES(NEW.username, True, True, True, {default_lang});
    END;
    """
    self.cursor.execute(trigger_add_settings)
    self.conn.commit()

    #create trigger remove account settings trigger on accounts table
    trigger_add_settings = """
    CREATE TRIGGER IF NOT EXISTS rm_acc_settings
    AFTER DELETE ON accounts
    BEGIN
      DELETE FROM account_settings WHERE username = OLD.username;
    END;
    """
    self.cursor.execute(trigger_add_settings)
    self.conn.commit()
    
    ## Instantiate User Class Here
    self.user = User("guest","","",False)
    ## Menus
    self.homePage = Menu()
    self.mainMenu = Menu()
    self.jobsMenu = Menu()
    self.friendMenu = Menu()
    self.videoMenu = Menu()
    self.skillsMenu = Menu()
    self.joinMenu = Menu()
    self.importantLinks = Menu()
    self.usefulLinks = Menu()
    self.privacyMenu = Menu()
    self.guestControls = Menu()
    self.generalMenu = Menu()
    self.quickMenu = Menu() # generic menu used to display content to user with no selections
    self.languageMenu = Menu()
    
  def __del__(self): #closes connection to db
    self.conn.close()
    
  #System Level Controls for Menus    
  def home_page(self):
   if not(self.user.loggedOn):
     self.homePage.start()
   else:
     self.mainMenu.start()
     self.user.logout()
     
  def join_menu(self):
   if not(self.user.loggedOn):
     self.joinMenu.start()
   else:
     self.mainMenu.start()
     self.user.logout()
     

  def quick_menu(self, opening, exit='Back'):
    """
    Allows the caller to display text to the user in a simple menu with no selections.
    
    Args:
      opening (str): The menu's opening statement.
      exit (str): Optional label for the menu's exit statement/hotkey. The default is 'Back'. 
    """
    
    self.quickMenu.setOpening(opening)
    self.quickMenu.setExitStatement(exit)
    self.quickMenu.start()

  
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
  def important_links(self):
      self.importantLinks.start()
  def privacy_menu(self):
      self.privacyMenu.start()
  def guest_controls(self):
      self.guestControls.start()
  def useful_links(self):
      self.usefulLinks.start()
  def general_menu(self):
      self.generalMenu.start()
  def language_menu(self):
      self.languageMenu.start()
    
  def encryption(self, password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    hashed_pass = sha256.hexdigest()
    return hashed_pass

  def deleteTable(self):
    print("Are You Sure You Want To Delete The Current Accounts In The Database? This Operation Cannot Be Undone.(Y/N): ")
    confirm = input()
    if confirm.upper() == "Y":
      self.cursor.execute("DROP TABLE IF EXISTS accounts")
      self.conn.commit()
      print("Table Deleted Successfully.")
    else:
      print("Deletion Operation Canceled.")
  
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
    
  def validPosNum(self,name,num):
    if num.isdigit():
      if int(num) < 0:
        print(name + " Must Be Greater Than Or Equal to Zero.")
        return False
    else:
      print(name + " Must Be A Number Value")
      return False
    return True
        
  def validString(self,name,string):
    if len(string) > 128:
      print(name + " Must Be 1-128 Characters")
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
      acc_fields = 'username, password, fName, lName, email, sms, targetedAds, language'
      select_account = f"""
        SELECT {acc_fields} FROM accounts NATURAL JOIN account_settings WHERE username = (?)
      """
      self.cursor.execute(select_account, (userName,)) 
      #? is placeholder for username
      account = self.cursor.fetchone() #fetches first row which query returns
      if account: #if the username exists, then we check that the password in the database matches the password the user inputted
        hashed_inputpass = self.encryption(password)
        if hashed_inputpass == account[1]:
          print("You Have Successfully Logged In!")
          self.user.login(userName,
                          fName=account[2],
                          lName=account[3], 
                          email=account[4], 
                          sms=account[5], 
                          targetedAds=account[6], 
                          language=account[7])
          return self.home_page
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
      return self.login
    else:
      print("Account Creation Failed.")
    return

  def postJob(self):
    ## Set Account Limit
    if self.countRows("jobs") >= 5:
      print("Maximum Number Of Jobs Posts Created!")
      return
    print("Enter Title: ")
    title = input()
    print("Enter Description: ")
    description = input()
    print("Enter Employer: ")
    employer = input()
    print("Enter Location: ")
    location = input()
    print("Enter Salary: ")
    salary = input()
    ## Validate Inputs
    if self.validString("Title",title) and self.validString("Description",description) and self.validString("Employer",employer)and self.validString("Location",location) and self.validPosNum("Salary",salary):
      self.cursor.execute("INSERT INTO jobs (title, description,employer,location,salary,posterFirstName,posterLastName) VALUES (?, ?, ?, ?, ?, ?, ?)", (title, description,employer,location,salary,self.user.fName,self.user.lName))
      self.conn.commit() #saving new account to database
      print("Job Posted Successfully.")
      return 
    else:
      print("Job Posting Creation Failed.")
    return

  #This is the function to find someone they know in the system
  def findUser(self):
    #Prompts for searching by first name and last name
    print("Enter First Name: ")
    fName = input()
    print("Enter Last Name: ")
    lName = input()
    # Validate
    if(self.validName(fName,lName)):
        # Search for the user in the database
        self.cursor.execute("SELECT * FROM accounts WHERE UPPER(fName) = UPPER(?) AND UPPER(lName) = UPPER(?)", (fName, lName))
        result = self.cursor.fetchall()
        ## If the user is found, print 
        if len(result) > 0:
            print("They Are Part Of The InCollege System.")
            return self.join_menu
        else:
            print("They Are Not Yet A Part Of The InCollege System.")
        
    else:
      print("Invalid Name Given. Please Try Again.")

  def setUserEmail(self):
    """
    Toggles the user's email setting between True (ON) and False (OFF). 
    If an exception occurs when updating the DB then no change is made, 
    and a message is displayed informing the user to try again later.
    """
    username = self.user.userName
    newEmail = not self.user.email
    update = 'UPDATE account_settings SET email = ? WHERE username = ?'
    try:
      self.cursor.execute(update, (newEmail, username))
      self.conn.commit()
      self.user.email = newEmail
    except Exception:
      print(MSG_ERR_RETRY)

  def setUserSMS(self):
    """
    Toggles the user's sms setting between True (ON) and False (OFF). 
    If an exception occurs when updating the DB then no change is made, 
    and a message is displayed informing the user to try again later.
    """
    username = self.user.userName
    newSMS = not self.user.sms
    update = 'UPDATE account_settings SET sms = ? WHERE username = ?'
    try:
      self.cursor.execute(update, (newSMS, username))
      self.conn.commit()
      self.user.sms = newSMS
    except Exception:
      print(MSG_ERR_RETRY)

  def setUserTargetedAds(self):
    """
    Toggles the user's targeted advertising setting between True (ON) and False (OFF). 
    If an exception occurs when updating the DB then no change is made, 
    and a message is displayed informing the user to try again later.
    """
    username = self.user.userName
    newtargetedAds = not self.user.targetedAds
    update = 'UPDATE account_settings SET targetedAds = ? WHERE username = ?'
    try:
      self.cursor.execute(update, (newtargetedAds, username))
      self.conn.commit()
      self.user.targetedAds = newtargetedAds
    except Exception:
      print(MSG_ERR_RETRY)

  def setUserLanguage(self, language):
    """
    Sets the user's language setting to the specified language. 
    If an exception occurs when updating the DB then no change is made, 
    and a message is displayed informing the user to try again later.
    
    Args:
      language (str): A language from the system's LANGUAGES list.
    """
    uName = self.user.userName
    update = 'UPDATE account_settings SET language = ? WHERE username = ?' 
    try:
        self.cursor.execute(update, (language, uName))
        self.conn.commit()
        self.user.language = language
    except Exception:
        print(MSG_ERR_RETRY)

  ## Function for the important links to print
  def printLink(self, link):
        content = {
            'Copyright Notice': '''
---------------------------
      COPYRIGHT NOTICE
---------------------------

All content and materials displayed on the InCollege website, including but not limited to text, graphics, logos, images, audio clips, and software, are the property of InCollege and are protected by international copyright laws.

The unauthorized reproduction, distribution, or modification of any content on the InCollege website is strictly prohibited without prior written permission from InCollege.

For any inquiries regarding the use of our copyrighted materials, please contact us at legal@incollege.com.

By accessing and using the InCollege website, you agree to comply with all applicable copyright laws and regulations.

---------------------------
''',
            'About': '''
--------------------------------------
               ABOUT US
--------------------------------------

Welcome to InCollege - Where Connections and Opportunities Thrive!

At InCollege, we are dedicated to providing a vibrant online platform for college students to connect with friends, explore exciting career opportunities, and foster meaningful professional relationships. Our mission is to empower students like you to unleash your full potential and shape a successful future.

Through our innovative features and cutting-edge technology, we strive to create a dynamic virtual space that bridges the gap between your academic journey and the professional world. Whether you're searching for internships, part-time jobs, or launching your post-graduation career, InCollege is your trusted companion.

Join our vibrant community today and embark on an exciting journey of personal growth, professional development, and lifelong connections.

--------------------------------------
''',
            'Accessibility': '''
------------------------
ACCESSIBILITY STATEMENT
------------------------

InCollege is committed to ensuring accessibility and inclusion for all users of our text-based app. We strive to provide a user-friendly experience for individuals with diverse abilities.

Accessibility Features:
- Clear Text Formatting: We use clear and legible text formatting to enhance readability for all users.
- Keyboard Navigation: Our app supports keyboard navigation, allowing users to navigate through the app using keyboard shortcuts.
- Text Resizing: You can easily adjust the text size within the app to suit your preferences.
- Simple and Intuitive Design: Our app features a simple and intuitive design, making it easy to navigate and use.

Feedback and Support:
We value your feedback and are continuously working to improve the accessibility of our app. If you have any suggestions or encounter any barriers while using the app, please let us know. 

------------------------
''',
            'User Agreement': '''
------------------------
    USER AGREEMENT
------------------------

Welcome to InCollege! This User Agreement ("Agreement") governs your use of our text-based app. By accessing or using our app, you agree to be bound by the terms and conditions outlined in this Agreement.

1. Acceptance of Terms:
   By using our app, you acknowledge that you have read, understood, and agreed to be bound by this Agreement. If you do not agree with any part of this Agreement, please refrain from using our app.

3. Privacy:
   We respect your privacy and are committed to protecting your personal information. Our Privacy Policy outlines how we collect, use, and disclose your information. By using our app, you consent to the collection and use of your data as described in our Privacy Policy.

4. Limitation of Liability:
   In no event shall InCollege or its affiliates be liable for any damages arising out of or in connection with the use of our app.

5. Modification of Agreement:
   We reserve the right to modify or update this Agreement at any time. 

6. Termination:
   We reserve the right to terminate your access to our app at any time, without prior notice, if we believe you have violated this Agreement or any applicable laws.

By continuing to use our app, you acknowledge that you have read and agreed to this User Agreement.

------------------------
''',
            'Cookie Policy': '''
------------------------
   COOKIE POLICY
------------------------

At InCollege, we use cookies to enhance your browsing experience and improve our services. This Cookie Policy explains how we use cookies on our website.

   We use cookies for the following purposes:

   - Authentication: Cookies help us authenticate and secure your account.
   - Preferences: Cookies remember your settings and preferences.
   - Analytics: Cookies gather information about your usage patterns to improve our website's performance.
   - Advertising: Cookies may be used to display relevant ads based on your interests.
------------------------
''',
            'Brand Policy': '''
------------------------
     BRAND POLICY
------------------------

InCollege is committed to protecting its brand identity and ensuring consistent and accurate representation across all platforms. This Brand Policy outlines the guidelines for using the InCollege brand assets.

   1. Logo Usage: The InCollege logo should be used in its original form and should not be altered, distorted, or modified in any way.
   2. Colors and Typography: The official InCollege colors and typography should be used consistently to maintain brand consistency.
   3. Prohibited Usage: The InCollege brand assets should not be used in any manner that implies endorsement, affiliation, or partnership without proper authorization.

Any unauthorized usage of the InCollege brand assets is strictly prohibited.

------------------------
''',
            'Help Center': '''
            We're here to help
            '''}
        print("You selected:", link)
        print(content[link])
        input("Press Enter to return to the Important Links page")
        self.importantLinks.clear()
        return

  #Under useful links
  def browse(self):
      print("Browse InCollege")
      print("Under Construction")
      input("Press Enter to return to the Useful Links page")
      self.importantLinks.clear()
      return
  def solutions(self):
      print("Business Solutions")
      print("Under Construction")
      input("Press Enter to return to the Useful Links page")
      self.importantLinks.clear()
      return
  def directories(self):
      print("Directories")
      print("Under Construction")
      input("Press Enter to return to the Useful Links page")
      self.importantLinks.clear()
      return
  
  ## Skills to Learn ##
  def skillA(self):
      print("Project Management")
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
  def initMenu(self):
      ## Set Home Page Items
      hpOpening = """
    Welcome To The InCollege Home Page!
      
    The Place Where Students Take The Next Big Step.

    "I Had To Battle With Anxiety Every Day Until I Signed Up For InCollege.
    Now, My Future Is On The Right Track And Im Able To Apply My Education To My Dream Career.
    Finding A Place In My Field Of Study Was A Breeze"
    - InCollege User

    """
      self.homePage.setOpening(hpOpening)
      self.homePage.addItem("Login", self.login)
      self.homePage.addItem("Register", self.register)
      self.homePage.addItem("Find People I Know", self.findUser)
      ##self.homePage.setSelection('4',{'label':'Delete Users','action':self.deleteTable})
      self.homePage.addItem("See Our Success Video", self.video_menu)
      self.homePage.addItem('Useful Links', self.useful_links)
      self.homePage.addItem('InCollege Important Links', self.important_links)
      ## Set Video Page Items
      self.videoMenu.setOpening("See Our Success Story:\n(Playing Video)\n")
      ## Set Main Menu Items
      self.mainMenu.setOpening("Welcome User!")
      self.mainMenu.addItem('Job/Internship Search', self.jobs_menu)
      self.mainMenu.addItem('Find A Friend', self.friend_menu)
      self.mainMenu.addItem('Learn A Skill', self.skills_menu)
      self.mainMenu.addItem('Useful Links', self.useful_links)
      self.mainMenu.addItem('InCollege Important Links', self.important_links)
      self.mainMenu.setExitStatement("Log Out")
      # Set Skill Items
      self.skillsMenu.setOpening("Please Select a Skill:")
      self.skillsMenu.addItem('Project Management',self.skillA)
      self.skillsMenu.addItem('Networking',self.skillB)
      self.skillsMenu.addItem('System Design',self.skillC)
      self.skillsMenu.addItem('Coding',self.skillD)
      self.skillsMenu.addItem('Professional Communication',self.skillE)
      self.skillsMenu.setExitStatement("Return To Main Menu")
      # Set Join Items
      self.joinMenu.setOpening("Would You Like To Join Your Friends On InCollege?")
      self.joinMenu.addItem('Login',self.login)
      self.joinMenu.addItem('Register',self.register)
      self.joinMenu.setExitStatement("Return To Home Page")
      # Set Post A Job Items
      self.jobsMenu.setOpening("Welcome to the Job Postings Page")
      self.jobsMenu.addItem('Post Job',self.postJob)
      self.jobsMenu.setExitStatement("Return To Main Menu")
      # Set InCollege Important Links
      self.importantLinks.setOpening("Welcome to the Important Links Page")
      self.importantLinks.addItem('Copyright Notice', lambda: self.printLink("Copyright Notice"))
      self.importantLinks.addItem('About', lambda: self.printLink("About"))
      self.importantLinks.addItem('Accessibility', lambda: self.printLink("Accessibility"))
      self.importantLinks.addItem('User Agreement', lambda: self.printLink("User Agreement"))
      self.importantLinks.addItem('Privacy Policy', self.privacy_menu)
      self.importantLinks.addItem('Cookie Policy', lambda: self.printLink("Cookie Policy"))
      self.importantLinks.addItem('Brand Policy', lambda: self.printLink("Brand Policy"))
      self.importantLinks.addItem('Languages', self.language_menu, lambda: True if self.user.loggedOn else False)
      self.importantLinks.setExitStatement("Return To Home Page")
      # Set Guest Controls Items  
      self.guestControls.setOpening("Account Preferences:\n")
      self.guestControls.addItem((lambda: f"Email [{'ON' if self.user.email else 'OFF'}]"), self.setUserEmail)
      self.guestControls.addItem((lambda: f"SMS [{'ON' if self.user.sms else 'OFF'}]"), self.setUserSMS)
      self.guestControls.addItem(
        (lambda: f"Targeted Advertising [{'ON' if self.user.targetedAds else 'OFF'}]"), 
        self.setUserTargetedAds)
      self.guestControls.setExitStatement("Back")
      # Set Languages Items
      self.languageMenu.setOpening("Languages:")
      for language in LANGUAGES:
        """give parameter to lambda functions here 
        as workaround for python's lambda function late binding issue 
        otherwise all menu items will be created with the last language in the list """
        label = lambda lang=language: f"{lang} [{'X' if self.user.language == lang else ' '}]"
        action = lambda lang=language: self.setUserLanguage(lang)
        self.languageMenu.addItem(label, action)
      
      for sel in self.languageMenu.selections:
        print(sel['label']())
      self.languageMenu.setExitStatement("Back")
      # Privacy page
      privacyPolicy = """
------------------------
   PRIVACY POLICY
------------------------

At InCollege, we value your privacy and are committed to protecting your personal information. Here's a summary of our privacy practices:

1. Information Collection:
   We collect limited personal information when you register and interact with our platform.

2. Data Usage:
   We use your information to personalize your experience, deliver relevant content, and improve our services. We employ industry-standard security measures to protect your information from unauthorized access.

3. Cookies and Tracking:
   We may use cookies to enhance your browsing experience.
------------------------
      """
      #Privacy menu just to have the option for guest controls if logged in
      self.privacyMenu.setOpening(privacyPolicy)
      self.privacyMenu.addItem('Guest Controls', self.guest_controls, lambda: True if self.user.loggedOn else False)
      #Useful links menu
      self.usefulLinks.setOpening("Welcome to the Useful Links Page")
      self.usefulLinks.addItem('General', self.general_menu)
      self.usefulLinks.addItem('Browse InCollege', self.browse)
      self.usefulLinks.addItem('Business Solutions', self.solutions)
      self.usefulLinks.addItem('Directories', self.directories)
      #General links menu navigation links
      self.generalMenu.setOpening('General Links')
      self.generalMenu.addItem('Sign Up', self.join_menu , lambda: True if not self.user.loggedOn else False) #finish this
      self.generalMenu.addItem('Help Center', lambda: self.printLink("Help Center"))
    