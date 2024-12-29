from operator import contains
import os
from pyexpat.errors import messages
import time
from turtle import end_fill
import requests
import re
import random
import sys
import subprocess
import bs4
import json
import urllib.request
import datetime
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def die(msg, timer):
   print (bcolors.WARNING+msg+bcolors.ENDC)
   time.sleep(timer)
   exit()
def update():

   script_name = sys.argv[0]
   if 'smscommander_new_version.exe' in str(script_name):
       die("Rename the script to smscommander before you can run it", 20)
   ###############
   version = "1.5"
   ###############
   print("Checking for updates..")
   url = f"https://store.cloudjet.org/api/smscommander/api.php?action=update"
   response = requests.get(url)
   json_data = response.json()
   lastver = json_data["last"]
   if lastver != version:   
    print("A newer version found, updating..")
    url = "https://github.com/0x054m4/smscommander/raw/main/smscommander.exe"
    urllib.request.urlretrieve(url, "smscommander_new_version.exe")
    script_name = sys.argv[0]
    print ("Update downloaded and saved as smscommander_new_version.exe, please rename it to smscommander.exe then run it.")
    die("", 20)
   else:
    print("You're up to date.")
    time.sleep(1)
    os.system('cls')
def tutorial():
 try: 
   isFirstTime = ('smscommander/isf.txt')
   os.remove('smscommander/isf.txt')
 except:
     isFirstTime = '0'
 if isFirstTime != '0':
     print(bcolors.OKBLUE+'''
     It looks like it is the first time for you to use this version from SMSCommander.
     Do you want to see a quick tutorial of how to use? 
     1) Yes
     2) No, I know how to use it
     '''+bcolors.ENDC)
     tutorialOption = input(bcolors.OKCYAN+'Input option number: '+bcolors.ENDC)
     if tutorialOption == '2':
        return   
     else:
         print(bcolors.OKBLUE+'''
         Follow the next steps to setup SMS Commander:- 
         1- Open smscommander/config.json file and set your credentials, get your api keys from store dashboard.
         2- The shortener api key exist in shortener dashboard
         3- After setting your credentials, restart SMS Commander and start your journey!
         '''+bcolors.ENDC)
         die("", 500)
def checkurl(url):
   urlr = f"https://store.cloudjet.org/api/smscommander/api.php?action=checkurl&url={url}"
   response = requests.get(urlr)
   json_data = response.json()
   if json_data["status"] == 'red':
      r = 'red'
   else:
      r = 'green'
   return r
def preChecks():
   with open('smscommander/config.json', 'r') as f:
    config_data = json.load(f)
    license_key = config_data['licensekey']
   print(bcolors.OKBLUE+"Checking your license.."+bcolors.ENDC)
   url = f"https://store.cloudjet.org/api/smscommander/api.php?action=checkLicense&license={license_key}"
   response = requests.get(url)
   json_data = response.json()
   if json_data["status"] == 'failed':
      error = json_data["error"]
      die("An error occured while checking your SMS Commander license, error: "+error, 7)
   elif json_data["status"] == "success":
      credit = json_data["credit"]
      if int(credit) > 20:
         print(bcolors.OKGREEN+"License check passed, remaining SMS credits: "+credit+bcolors.ENDC)
      else:
         print(bcolors.WARNING+"License check passed, remaining SMS credits: "+credit+bcolors.ENDC)
      time.sleep(2)
      return [credit]
def gg(type, platformName, url):
   welcomeWords = ["Dear Sir/Madam", "To whom it may concern", "Dear valued customer", "Good day", "Hello"]
   class accountSuspended:
    accountSuspended = [
    "we regret to inform you that your "+platformName+" account has been temporarily suspended.",
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
        print("Message check passed.")
def messageSerializer(msg, url):
  print(bcolors.OKBLUE+"Serializing your message.."+bcolors.ENDC)
  preparedMessage = msg.replace("[url]", url)
  return preparedMessage
def secondaryMessageSerializer(msg):
   n = str(random.randint(10000,99999))
   msg = msg.replace("[rand]", n)
   tdate = str(datetime.date.today())
   msg = msg.replace("[date]", tdate)
   return msg

def shortenUrl(url):
   with open('smscommander/config.json', 'r') as f:
    config_data = json.load(f)
    apikey = config_data['apikey']
   print(bcolors.OKBLUE+"Shortening your url.."+bcolors.ENDC)
   url = f"https://store.cloudjet.org/api/shortener/shorten.php?apikey={apikey}&url={url}"
   response = requests.get(url)
   json_data = response.json()
   if json_data["status"] == 'failed':
      error = json_data["error"]
      die("An error occured while shortening your url, error: "+error, 7)
   elif json_data["status"] == "success":
      print(bcolors.OKGREEN+"Your url has been shortened successfully."+bcolors.ENDC)
      shortenedUrl = json_data["shortenedurl"]
      return shortenedUrl
def saveNumber(number):
   url = f"https://store.cloudjet.org/api/smscommander/api.php?action=saveNumber&number={number}"
   response = requests.get(url)
   
def send(message, uurl, ggoption, ggtype, platformName, creds):
   with open('smscommander/config.json', 'r') as f:
    config_data = json.load(f)
    license_key = config_data['licensekey']
    
   if ggoption == 0:
      list_filename = "smscommander/list.txt"
      filename = "smscommander/list.txt"
      list_filename2 = open(filename, "r")
      lenx = len(list_filename2.readlines())
      if lenx > int(creds):
        
         die("The numbers list contains numbers count more than the credits you have, for your safety, the sendout has been aborted.", 12)
      numbers = []
      with open(list_filename, "r") as file:
          for line in file:
              numbers.append(int(line.strip()))  # convert each line to an integer and append to list
      
      failed_numbers = []

      
      for i, number in enumerate(numbers):
            saveNumber(number)
            if i == 0:
               url = shortenUrl(uurl)
               message = messageSerializer(message, url)
               print(bcolors.OKGREEN+"Message serialized, and will look like (Random numbers will change with every message): "+secondaryMessageSerializer(message)+bcolors.ENDC)
               print(bcolors.OKBLUE+'''Is that ok for you?
               1) Yes
               2) No (will abort the sendout)'''+bcolors.ENDC)
               accepted = input(bcolors.OKCYAN+'Input option number: '+bcolors.ENDC)
               if accepted != '1':
                  die("Aborted by user.", 3)
            if checkurl(uurl) == 'red':
             die("Your page url is detected as red and the sendout has been aborted, why don't you use cloudjet.org Anti-Red cPanels?", 10)
            mmessage = secondaryMessageSerializer(message)
            url = f"https://store.cloudjet.org/api/smscommander/api.php?action=send&number={number}&message={mmessage}&licensekey={license_key}"
            response = requests.get(url)
            json_data = response.json()
            if json_data["status"] == 'success':  
              print(bcolors.OKGREEN+"SENT => "+str(number)+" | MESSAGE => "+str(mmessage)+" | ~THANKS TO CLOUDJET.ORG"+bcolors.ENDC)
              time.sleep(3)
              if (i+1) % 100 == 0:
                  print(bcolors.OKBLUE+"Re-shortening your url.."+bcolors.ENDC)
                  url = shortenUrl(uurl)
                  message = messageSerializer(message, url)
                  print(bcolors.OKBLUE+"Your url has been re-shortened, sending will continue."+bcolors.ENDC)
            else:
               error = json_data["error"]
               print(bcolors.FAIL+"FAILED => "+str(number)+" | ERROR=> "+error+" | ~THANKS TO CLOUDJET.ORG"+bcolors.ENDC)
               failed_numbers.append(number)
      print('''
            Total numbers: '''+str(i+1)+'''
            Failed: '''+str(len(failed_numbers))+'''
            Succeeded: '''+str(i+1-len(failed_numbers))+'''
            All failed numbers has been saved in a file in smscommander/fails folder for your safety.
            ''')
      input(bcolors.OKCYAN+'Press enter to exit'+bcolors.ENDC)
      if failed_numbers:
          now = datetime.datetime.now()
          filename = f"smscommander/fails/failed-{now.strftime('%Y-%m-%d-%H-%M-%S')}.txt"
          with open(filename, "w") as file:
              file.write("\n".join(str(number) for number in failed_numbers))
   else:

      list_filename = "smscommander/list.txt"
      filename = "smscommander/list.txt"
      list_filename2 = open(filename, "r")
      lenx = len(list_filename2.readlines())
      
      if lenx > int(creds):
         die("The numbers list contains numbers count more than the credits you have, for you safety, the sendout has been aborted.", 12)
      numbers = []
      with open(list_filename, "r") as file:
          for line in file:
              numbers.append(int(line.strip()))  # convert each line to an integer and append to list
      
      failed_numbers = []
      i = 0
      for i, number in enumerate(numbers):
            saveNumber(number)
            if i == 0:
               url = shortenUrl(uurl)

            if checkurl(uurl) == 'red':
             die("Your page url is detected as red and the sendout has been aborted, why don't you use cloudjet.org Anti-Red cPanels?", 10)
            message = gg(ggtype, platformName, url)
            urlr = f"https://store.cloudjet.org/api/smscommander/api.php?action=send&number={number}&message={message}&licensekey={license_key}"
            response = requests.get(urlr)
            json_data = response.json()
            if json_data["status"] == 'success':  
              print(bcolors.OKGREEN+"SENT => "+str(number)+" | MESSAGE => "+str(message)+" | ~THANKS TO CLOUDJET.ORG"+bcolors.ENDC)
              time.sleep(3)
              if (i+1) % 100 == 0:
                  print(bcolors.OKBLUE+"Re-shortening your url.."+bcolors.ENDC)
                  url = shortenUrl(uurl)
                  print(bcolors.OKGREEN+"Your url has been re-shortened, sending will continue."+bcolors.ENDC)
            else:
               error = json_data["error"]
               print(bcolors.FAIL+"FAILED => "+str(number)+" | ERROR=> "+error+" | ~THANKS TO CLOUDJET.ORG"+bcolors.ENDC)
               failed_numbers.append(number)
      print('''
            Total numbers: '''+str(i+1)+'''
            Failed: '''+str(len(failed_numbers))+'''
            Succeeded: '''+str(i+1-len(failed_numbers))+'''
            All failed numbers has been saved in a file in smscommander/fails folder for your safety.
            ''')
      input(bcolors.OKCYAN+'Press enter to exit'+bcolors.ENDC)
      if failed_numbers:
          now = datetime.datetime.now()
          filename = f"smscommander/fails/failed-{now.strftime('%Y-%m-%d-%H-%M-%S')}.txt"
          with open(filename, "w") as file:
              file.write("\n".join(str(number) for number in failed_numbers))
def sendPreChecks(message, ggopt):
   print(bcolors.OKBLUE+"Running a quality check on your numbers list.."+bcolors.ENDC)
   lines = open('smscommander/list.txt').read().splitlines()
   number =random.choice(lines)
   url = f"https://store.cloudjet.org/api/smscommander/api.php?action=checkListQuality&number={number}"
   response = requests.get(url)
   json_data = response.json()
   if json_data["quality"] == 'poor':
      print(bcolors.OKBLUE+'''
      According to the quality check results, it looks like your list has been sent before by somebody.
      Do you want to continue anyway?
      1) Yes
      2) No, abort the sendout
      '''+bcolors.ENDC)
      qualityaccept = input(bcolors.OKCYAN+'Input option number: '+bcolors.ENDC)
      if(qualityaccept == '2'):
         die("Aborted by user", 3)
   else:
      print(bcolors.OKGREEN+"Quality check passed."+bcolors.ENDC)
   return
update()
print(bcolors.HEADER+'''


   _____ __  ________    ______                                          __         
  / ___//  |/  / ___/   / ____/___  ____ ___  ____ ___  ____ _____  ____/ /__  _____
  \__ \/ /|_/ /\__ \   / /   / __ \/ __ `__ \/ __ `__ \/ __ `/ __ \/ __  / _ \/ ___/
 ___/ / /  / /___/ /  / /___/ /_/ / / / / / / / / / / / /_/ / / / / /_/ /  __/ /    
/____/_/  /_//____/   \____/\____/_/ /_/ /_/_/ /_/ /_/\__,_/_/ /_/\__,_/\___/_/     
                                                                                    
-------------------------------BY CLOUDJET.ORG------------------------------------
VERSION: 1.0
'''+bcolors.ENDC)
tutorial()
creds = preChecks()[0]
print(bcolors.OKCYAN+'''
--------------------------------------------
'''+bcolors.ENDC)
url = input(bcolors.OKCYAN+'Input your target url (Do NOT shorten it): '+bcolors.ENDC)
print(bcolors.OKBLUE+"Checking your page url status.."+bcolors.ENDC)
if checkurl(url) == 'red':
   die("Your page url is detected as red and the sendout has been aborted.", 10)
else:
   print(bcolors.OKGREEN+"Url check passed."+bcolors.ENDC)
print(bcolors.OKBLUE+'''
Do you want to use Generic-Generate® feature? 
1) Yes
2) No, I want to type my message manually
3) What is it?
'''+bcolors.ENDC)
ggoption = input(bcolors.OKCYAN+'Input option number: '+bcolors.ENDC)
if(ggoption == '3'):
   print(bcolors.OKBLUE+'''
    With Generic-Generate® feature, your message will be generated separately for each number using alternative words for each one, 
    we use AI large datasets to give the best accurate formal message 
    in the same time of giving unique words for each message.
    '''+bcolors.ENDC)
   die('', 12)
elif(ggoption == '2'):
   print(bcolors.OKBLUE+'''
   Message guide: Input your message without any urls, put "[url]" instead of your url.
   You can use "[rand]" to put random 5 digits.
   You can use "[date]" to put today's date.
   Example: Your account has been suspended, please follow the next link: [url]. Message REF:- [rand]. DATE: [date]
   '''+bcolors.ENDC)
   message = input(bcolors.OKCYAN+'Input your message: '+bcolors.ENDC)
   messageCheck(message)
   sendPreChecks(message, 0)
   send(message, url, 0, 0, 0, creds)
else:
   print(bcolors.OKBLUE+'''
   With Generic-Generate® feature, your message will be generated separately for 
   each number using alternative words for each one.
         

   '''+bcolors.ENDC)
   print(bcolors.OKBLUE+'''
   Choose your message type:
   1) Account suspension.
   ~More types coming soon~
   '''+bcolors.ENDC)
   type = input(bcolors.OKCYAN+'Input your message type: '+bcolors.ENDC)
   if type == '1':
      platformName = input(bcolors.OKCYAN+'Input the company name: '+bcolors.ENDC)
      sendPreChecks(0, 1)
      send(0, url, 1, 1, platformName, creds)
