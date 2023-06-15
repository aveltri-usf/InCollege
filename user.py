class User:
  ## Not in Use Yet but will hold saved progress and relationships eventually
  ## Probably instantiate in system class and hold logged in status as well
  def __init__(self, userName,fName,lName,loggedOn):
    from system import LANGUAGES
    self.userName = userName
    self.fName = fName
    self.lName = lName
    self.email = True
    self.sms = True
    self.targetedAds = True
    self.language = LANGUAGES[0]
    self.loggedOn = loggedOn
  def login(self, userName, fName, lName, email, sms, targetedAds, language):
    self.userName = userName
    self.fName = fName
    self.lName = lName
    self.email = email
    self.sms = sms
    self.targetedAds = targetedAds
    self.language = language
    self.loggedOn = True
  def logout(self):
    self.userName = "guest"
    self.fName = ""
    self.lName = ""
    self.loggedOn = False
  
    