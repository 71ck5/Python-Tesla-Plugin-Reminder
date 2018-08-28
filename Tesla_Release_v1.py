from email.message import EmailMessage
import urllib.request
import urllib.parse
import smtplib
import json
import time

#min and max so -87 is less then -97 and 6 greater then 2.
min_lat="" #minimum lat; FILL
max_lat="" #maximum lat; FILL
min_long="" #minimum long; FILL
max_long="" #maximum long; FILL
base_url="https://owner-api.teslamotors.com"
api_url=(base_url + "/api/1")
CLIENT_ID = "81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384"
CLIENT_SECRET = "c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3"
vehicle_id="" #this is not Vehicle_id or id but id_s; FILL
t_email="" #tesla email; FILL
t_password="" #tesla password ; FILL
e_email="" # email email; FILL
e_password="" # email password; FILL
e_time="3600" #time inbetween checks Default=1HR
smtp_server="" # smtp sever Example: smtp.gmail.com; FILL
smtp_port="" # smtp port Example: 587; FILL
toaddr = e_email # address send msg Default: e_email or your email 

auth_para = {
            "grant_type": "password",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "email": t_email,
            "password": t_password
        }

auth_param = urllib.parse.urlencode(auth_para)#this is for encoding to allow for use in urlopen
auth_param = auth_param.encode('ascii')       #^ 
auth = json.load(urllib.request.urlopen(base_url + "/oauth/token", data=auth_param))
headers = {'Authorization': 'Bearer {a}'.format(a=(auth["access_token"]))} # assign access token

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
