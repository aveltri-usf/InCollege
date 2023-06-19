import pytest
from system import System
from unittest import mock

#story: As a new user, I want to be able to learn about important information about InCollege
# inCollage important information link  appear in the home page menu 
def test_inCollegeImportantInformationHomePage():
  system_instance = System()  # Create an instance of the System class
  system_instance.initMenu()
  # Get the menu items from the homePage
  menu_items = system_instance.homePage.selections
  # Check if the "InCollege Important Links" option exists in the home page manu
  inCollege_links_option = next(
    (item
     for item in menu_items if item['label'] == 'InCollege Important Links'),
    None)
  # Assert that the option exists
  assert inCollege_links_option is not None


# inCollage Important information link appear in the main manu when user logged in 
def test_inCollageImportantInformationMainMenu():
  system_instance = System()
  # Call the initMenu method to initialize the menu
  system_instance.initMenu()
  # Get the menu items from the mainMenu
  menu_items = system_instance.mainMenu.selections
  # Check if the "InCollege Important Links" option exists in the main manu
  inCollege_links_option = next(
    (item
     for item in menu_items if item['label'] == 'InCollege Important Links'),
    None)
  # Assert that the option exists
  assert inCollege_links_option is not None


# test to check when the user select the option 6 it display the menu for inCollage important links
def test_incollege_important_links_SubMenu(capsys):
 # instance of the class system and call the initmenu
  system = System()
  system.initMenu()
  #simulate the input of the option 6 
  with mock.patch('builtins.input', side_effect=['6', '0', '0', '0']):
    system.important_links()
  # Capture the output
  captured = capsys.readouterr()
  output = captured.out
  print(output)
  # Assert that the expected message is displayed
  expected_message = '''
Welcome to the Important Links Page

[1] Copyright Notice
[2] About
[3] Accessibility
[4] User Agreement
[5] Privacy Policy
[6] Cookie Policy
[7] Brand Policy
[0] Return To Home Page
'''
  assert expected_message in output



# #Task 1:Add a "Copyright Notice" link and have it contain relevant content


def test_copyRightNoticelink(capsys, ):
  system_instance = System()
  # Call the initMenu method to initialize the menu
  system_instance.initMenu()
  # Get the menu items from the mainMenu
  menu_items = system_instance.importantLinks.selections
  # Check if the "InCollege Important Links" option exists in the main manu
  inCollege_links_option = next(
    (item for item in menu_items if item['label'] == 'Copyright Notice'), None)
  # Assert that the option exists
  assert inCollege_links_option is not None


# Select the Copy Rigth Notice Option
def test_select_copyright_notice_content(capsys):
  # Go to the "InCollege Important Links" menu
  system = System()
  system.initMenu()

  # system.importantLinks.addItem('Copyright Notice', lambda:      system.quick_menu(System.content["Copyright Notice"]))

  # # Select the "Copyright Notice" option
  with mock.patch('builtins.input', side_effect=['1', '0', '0', '0']):
    system.important_links()

  # Capture the output
  captured = capsys.readouterr()
  output = captured.out
  print(output)
  # Assert that the expected message is displayed
  expected_message = '''
---------------------------
      COPYRIGHT NOTICE
---------------------------

All content and materials displayed on the InCollege website, including but not limited to text, graphics, logos, images, audio clips, and software, are the property of InCollege and are protected by international copyright laws.

The unauthorized reproduction, distribution, or modification of any content on the InCollege website is strictly prohibited without prior written permission from InCollege.

For any inquiries regarding the use of our copyrighted materials, please contact us at legal@incollege.com.

By accessing and using the InCollege website, you agree to comply with all applicable copyright laws and regulations.

---------------------------
'''
  assert expected_message in output


# #Task 2:Add an "About" link and have it contain a history of the company and why it was created.


def test_aboutLink(capsys):
  system_instance = System()
  # Call the initMenu method to initialize the menu
  system_instance.initMenu()
  # Get the menu items from the mainMenu
  menu_items = system_instance.importantLinks.selections
  # Check if the "InCollege Important Links" option exists in the main manu
  inCollege_links_option = next(
    (item for item in menu_items if item['label'] == 'About'), None)
  # Assert that the option exists
  assert inCollege_links_option is not None


def test_aboutLinkContent(capsys, monkeypatch):
  # Go to the "InCollege Important Links" menu
  system = System()
  system.initMenu()
  # select about option
  with mock.patch('builtins.input', side_effect=['2', '0', '0', '0']):
    system.important_links()

  # Capture the output
  captured = capsys.readouterr()
  output = captured.out
  print(output)
  # Assert that the expected message is displayed
  expected_message = '''
--------------------------------------
               ABOUT US
--------------------------------------

Welcome to InCollege - Where Connections and Opportunities Thrive!

At InCollege, we are dedicated to providing a vibrant online platform for college students to connect with friends, explore exciting career opportunities, and foster meaningful professional relationships. Our mission is to empower students like you to unleash your full potential and shape a successful future.

Through our innovative features and cutting-edge technology, we strive to create a dynamic virtual space that bridges the gap between your academic journey and the professional world. Whether you're searching for internships, part-time jobs, or launching your post-graduation career, InCollege is your trusted companion.

Join our vibrant community today and embark on an exciting journey of personal growth, professional development, and lifelong connections.

--------------------------------------
'''
  assert expected_message in output


#Task 3:Add a "User Agreement" link and have it contain relevant content
def test_userAgreement(capsys):
  system_instance = System()
  # Call the initMenu method to initialize the menu
  system_instance.initMenu()
  # Get the menu items from the mainMenu
  menu_items = system_instance.importantLinks.selections
  # Check if the "InCollege Important Links" option exists in the main manu
  inCollege_links_option = next(
    (item for item in menu_items if item['label'] == 'User Agreement'), None)
  # Assert that the option exists
  assert inCollege_links_option is not None

def test_userAgreementContent(capsys, monkeypatch):
  # Go to the "InCollege Important Links" menu
  system = System()
  system.initMenu()
  # select about option
  with mock.patch('builtins.input', side_effect=['4', '0', '0', '0']):
    system.important_links()

  # Capture the output
  captured = capsys.readouterr()
  output = captured.out
  print(output)
  # Assert that the expected message is displayed
  expected_message = '''
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
'''
  assert expected_message in output


#Task 4:Add a "Privacy Policy" link and have it contain relevant content

def test_privacyPolicy(capsys):
  system_instance = System()
  # Call the initMenu method to initialize the menu
  system_instance.initMenu()
  # Get the menu items from the mainMenu
  menu_items = system_instance.importantLinks.selections
  # Check if the "InCollege Important Links" option exists in the main manu
  inCollege_links_option = next(
    (item for item in menu_items if item['label'] == 'Privacy Policy'), None)
  # Assert that the option exists
  assert inCollege_links_option is not None
# this test will test the content  inside the privacy policy 
def test_privacyPolicyContent(capsys, monkeypatch):
  # Go to the "InCollege Important Links" menu
  system = System()
  system.initMenu()
  # select about option
  with mock.patch('builtins.input', side_effect=['5', '0', '0', '0']):
    system.important_links()

  # Capture the output
  captured = capsys.readouterr()
  output = captured.out
  print(output)
  # Assert that the expected message is displayed
  expected_message = '''
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
'''
  assert expected_message in output


# #Task5:Add a "Cookie Policy" link and have it contain relevant content

def test_cookiePolicy(capsys):
  system_instance = System()
  # Call the initMenu method to initialize the menu
  system_instance.initMenu()
  # Get the menu items from the mainMenu
  menu_items = system_instance.importantLinks.selections
  # Check if the "InCollege Important Links" option exists in the main manu
  inCollege_links_option = next(
    (item for item in menu_items if item['label'] == 'Cookie Policy'), None)
  # Assert that the option exists
  assert inCollege_links_option is not None

def test_cookiePolicyContent(capsys, monkeypatch):
  # Go to the "InCollege Important Links" menu
  system = System()
  system.initMenu()
  # select about option
  with mock.patch('builtins.input', side_effect=['6', '0', '0', '0']):
    system.important_links()

  # Capture the output
  captured = capsys.readouterr()
  output = captured.out
  print(output)
  # Assert that the expected message is displayed
  expected_message = '''
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
'''
  assert expected_message in output

# #Task6: Clicking the Privacy Policy link will provide the user with the option to access Guest Controls, but only when they are logged in
def test_PrivacyPolicyGuestControls(capsys):
  system = System()
  system.initMenu()
  # assert that user is logged in to have language option appear
  system.user.loggedOn = True
  with mock.patch('builtins.input', side_effect=['5', '0', '0', '0']):
    system.important_links()

  captured = capsys.readouterr()
  output = captured.out
  print(output)
  # Assert that the expected message is displayed
  expected_message = '''
[1] Guest Controls
[0] Exit
'''
  assert expected_message in output

# check the guess control link

def test_GuestControlslink(capsys):
  system = System()
  system.initMenu()
  # assert that user is logged in to have language option appear
  system.user.loggedOn = True
  with mock.patch('builtins.input', side_effect=['1', '0', '0', '0']):
    system.guest_controls()

  captured = capsys.readouterr()
  output = captured.out
  print(output)
  # Assert that the expected message is displayed
  expected_message = '''
[1] Email [ON]
[2] SMS [ON]
[3] Targeted Advertising [ON]
[0] Back
'''
  assert expected_message in output

# #Task7:Add a "Brand Policy" link and have it contain relevant content

def test_brandPolicy(capsys):
  system_instance = System()
  # Call the initMenu method to initialize the menu
  system_instance.initMenu()
  # Get the menu items from the mainMenu
  menu_items = system_instance.importantLinks.selections
  # Check if the "InCollege Important Links" option exists in the main manu
  inCollege_links_option = next(
    (item for item in menu_items if item['label'] == 'Brand Policy'), None)
  # Assert that the option exists
  assert inCollege_links_option is not None

# test the content for the brand policy option 

def test_brandPolicyContent(capsys, monkeypatch):
  # Go to the "InCollege Important Links" menu
  system = System()
  system.initMenu()
  # select about option
  with mock.patch('builtins.input', side_effect=['7', '0', '0', '0']):
    system.important_links()

  # Capture the output
  captured = capsys.readouterr()
  output = captured.out
  print(output)
  # Assert that the expected message is displayed
  expected_message = '''
------------------------
     BRAND POLICY
------------------------

InCollege is committed to protecting its brand identity and ensuring consistent and accurate representation across all platforms. This Brand Policy outlines the guidelines for using the InCollege brand assets.

   1. Logo Usage: The InCollege logo should be used in its original form and should not be altered, distorted, or modified in any way.
   2. Colors and Typography: The official InCollege colors and typography should be used consistently to maintain brand consistency.
   3. Prohibited Usage: The InCollege brand assets should not be used in any manner that implies endorsement, affiliation, or partnership without proper authorization.

Any unauthorized usage of the InCollege brand assets is strictly prohibited.

------------------------
'''
  assert expected_message in output
# Accessibility link option 
def test_Accessibility(capsys):
  system_instance = System()
  # Call the initMenu method to initialize the menu
  system_instance.initMenu()
  # Get the menu items from the mainMenu
  menu_items = system_instance.importantLinks.selections
  # Check if the "InCollege Important Links" option exists in the main manu
  inCollege_links_option = next(
    (item for item in menu_items if item['label'] == 'Accessibility'), None)
  # Assert that the option exists
  assert inCollege_links_option is not None
# Accessibility link content test
def test_AccessibilityContent(capsys, monkeypatch):
  # Go to the "InCollege Important Links" menu
  system = System()
  system.initMenu()
  # select about option
  with mock.patch('builtins.input', side_effect=['3', '0', '0', '0']):
    system.important_links()

  # Capture the output
  captured = capsys.readouterr()
  output = captured.out
  print(output)
  # Assert that the expected message is displayed
  expected_message = '''
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
'''
  assert expected_message in output

# #Task8:Add a "Language" link Note:
def test_languageLink(capsys):
  system_instance = System()  # Create an instance of the System class
  system_instance.initMenu()
  # Get the menu items from the homePage
  menu_items = system_instance.importantLinks.selections
  # Check if the "InCollege Important Links" option exists in the home page manu
  inCollege_links_option = next(
    (item for item in menu_items if item['label'] == 'Languages'), None)
  # Assert that the option exists
  assert inCollege_links_option is not None


# #story: As a signed in user, I want to be able to switch the language

# #Task 1:Add an option to switch to Spanish

def test_languageSpanish(capsys):
  system = System()
  system.initMenu()
  # assert that user is logged in to have language option appear
  system.user.loggedOn = True
  with mock.patch('builtins.input', side_effect=['8', '0', '0', '0']):
    system.important_links()

  # capture output
  captured = capsys.readouterr()

  # check that spanish option is available and turned off by default
  assert "Spanish [ ]" in captured.out


# #Task2: Add an option to switch to English,
def test_slanguageEnglish(capsys):
  system = System()
  system.initMenu()
  # assert that user is logged in to have language option appear
  system.user.loggedOn = True

  with mock.patch('builtins.input', side_effect=['8', '0', '0', '0']):
    system.important_links()

  # capture output
  captured = capsys.readouterr()

  # check that english option is available and turned on by default
  assert "English [X]" in captured.out
# check the option to switch to Spanish 
def test_switchToSpanish(capsys):
  system = System()
  system.initMenu()
  # simulate the option spanish is the user select it 
  with mock.patch('builtins.input', side_effect=['2', '0', '0', '0',]):
    system.language_menu()

   # capture output
  captured = capsys.readouterr()

  # check that spanish option is available and turn on 
  assert "Spanish [X]" in captured.out
# check the option to switch to English
def test_switchToEnglish(capsys):
  system = System()
  system.initMenu()
  with mock.patch('builtins.input', side_effect=['1', '0', '0', '0',]):
    system.language_menu()

   # capture output
  captured = capsys.readouterr()

  # check that English option is available and turned on 
  assert "English [X]" in captured.out