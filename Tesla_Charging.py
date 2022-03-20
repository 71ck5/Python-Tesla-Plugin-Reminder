from email.message import EmailMessage
import urllib.request
import urllib.parse
import smtplib
import json
import time
import getpass
a = 0

#min and max so -87 is less then -97 and 6 greater then 2.
min_lat="" #minimum lat; FILL
max_lat="" #maximum lat; FILL
min_long="" #minimum long; FILL
max_long="" #maximum long; FILL
base_url="https://owner-api.teslamotors.com"
api_url=(base_url + "/api/1")
CLIENT_ID = ""
CLIENT_SECRET = ""
vehicle_id=[] #this is not Vehicle_id or id but id_s; FILL
t_email=input('Please input Telsa login email\n') #tesla email; FILL
t_password=getpass.getpass('Please input Telsa login password\n') #tesla password ; FILL
e_email=input('Please input email login email\n') # email email; FILL
e_password=getpass.getpass('Please input email login password\n') # email password; FILL
e_time="3600" #time inbetween checks Default=1HR
smtp_server="" # smtp sever Example: smtp.gmail.com; FILL
smtp_port="" # smtp port Example: 587; FILL
toaddr=input('Please input destination email for notification\n') # address to send msg to

auth_para = {
            "grant_type": "password",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "email": t_email,
            "password": t_password
        }

a = 0 # for increment
auth_param = urllib.parse.urlencode(auth_para)#this is for encoding to allow for use in urlopen
auth_param = auth_param.encode('ascii')       #^ 
auth = json.load(urllib.request.urlopen(base_url + "/oauth/token", data=auth_param))
headers = {'Authorization': 'Bearer {a}'.format(a=(auth["access_token"]))} # assign access token

car = urllib.request.Request(api_url + '/vehicles', headers=headers) #car selection
ca = (json.load(urllib.request.urlopen(car)))
if (ca['count'] == 1):
    vehicle_id = ca['response'][0]['id_s']
    print ("Only car selected")
else:
    for item in ca['response']:
        a += 1
        print (str(a) + '.' + item['display_name'])
    re = int(input('\nPlease choose a vehicle by number from 1 to ' + str(a) + ' \nExample: 1\n\n')) - 1
    vehicle_id = ca['response'][re]['id_s']
    print (vehicle_id)
    
if ("@google.com" in e_email) and (smtp_sever == smtp_port): #make it slightly easier
    smtp_server="smtp.gmail.com"
    smtp_port="587"
else:
    smtp_server=input('\nPlease input your smtp server \nExample: smtp.gmail.com\n\n')
    smtp_port=int(input('\nPlease input your smtp server \nExample: 587\n\n'))

def req(req_name): #For json api calls
    reqe = urllib.request.Request(api_url + '/vehicles/{vehicle_id}/data_request/{req_name}'.format(vehicle_id=vehicle_id,req_name=req_name), headers=headers)
    new1 = json.load(urllib.request.urlopen(reqe))
    return new1

def new(): #check if in location and state of charge door
    new = req("drive_state")
    new2 = req("charge_state")
    a = new['response']['latitude']
    b = new['response']['longitude']
    c = new2['response']['charge_port_door_open']
    if ((a > lat and a < lat1) and (b > long and b < long1)):
        if (c == False):
            print ("Car unplugged, Sending email.")
            try:
                email() #email
            except smtplib.SMTPException as e:
                print ("Failed due to {e}, Retrying in 10 minutes".format(e=e))
                ResponseData = ''
            
        
def email(): #email
    msg = EmailMessage()
    msg['From'] = e_email
    msg['To'] = toaddr
    msg['Subject'] = "Car is unplugged"
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(e_email, e_password)
    text = msg.as_string()
    server.sendmail(e_email, toaddr, text)
    server.quit()

while 1:
    try:
        new() #main function
        time.sleep(int(e_time)) #sleep for loop
    except urllib.error.URLError as e:print(e); time.sleep(60); ResponseData = ''  #Catch exceptions, print err, retry in 60 seconds
    except UnicodeEncodeError as e:print(e); time.sleep(60); ResponseData = ''     #^
    except urllib.error.HTTPError as e: print(e); time.sleep(60); ResponseData = ''#^
