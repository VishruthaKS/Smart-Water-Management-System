import paho.mqtt.client as mqtt
import sqlite3


#----------------------------------------------------------------------
broker_address= "<broker IP Address>"
port = 18753 #portNumber
user = "<username>"
password = "<password>"
topic = "server"
#----------------------------------------------------------------------
    
filestatus = False
def connect():
    global conn
    conn = sqlite3.connect('WaterManage.db')
    global c
    c = conn.cursor()
    
    
    
def Login(uname,upswd):
    c.execute("SELECT * FROM Users WHERE username = '%s' AND userpassword = '%s'" %(uname,upswd))
    if c.fetchall():
        print("Logged In")
        client.publish("webapp","loginSuccess"+","+uname)
    else:
        print("Login Failed")
        client.publish("webapp","loginFailed")  
        
def Register(username,userpassword):
    usrName_Search = c.execute("SELECT username FROM Users WHERE username = '%s'" % username).fetchone()
    if usrName_Search:  #same as if usrName_Search ==None
        print("Username already exits")
        client.publish("webapp","Username already exits")
    else:
        print("Registered")
        client.publish("webapp","registered")
        c.execute("INSERT INTO Users VALUES ('"+username+"','"+userpassword+"')") 
        conn.commit()  

def Values(username,userconsumed,water_remaining,flow_rate):
    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    capacity = 2500
    alloted  = 800
    remaining_quota = alloted - int(userconsumed)
    c.execute("INSERT INTO Data VALUES('"+username+"','"+str(userconsumed)+"','"+water_remaining+"','"+str(remaining_quota)+"','"+current_time+"')")
    consumed = ((int(userconsumed)*100)/800)
    remaining = ((int(remaining_quota)*100)/800)
    client.publish("webapp","values,"+username+","+str(capacity)+","+str(userconsumed)+","+str(consumed)+","+str(remaining_quota)+","+str(remaining)+","+str(water_remaining)+","+flow_rate+","+current_time)
    conn.commit()  

  
 
def CloseConnection():
    conn.close()

 # The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with code "+str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
    client.subscribe(topic + "/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    message = str(msg.payload)
    val=(message.split("'")[1])
    if val.split(",")[0] == "login":
        Login(val.split(",")[1],val.split(",")[2])
    elif val.split(",")[0] == "register":
         Register(val.split(",")[1],val.split(",")[2])
    elif val.split(",")[0] == "values":
         Values(val.split(",")[1],val.split(",")[2],val.split(",")[3],val.split(",")[4])
    

try:
    fh = open('WaterManage.db', 'r')
    filestatus = True
except FileNotFoundError:
    try:
        connect()
        c.execute('''CREATE TABLE Users
         (username text, userpassword text)''')
        c.execute('''CREATE TABLE Data
         (username text,userconsumed text, water_remaining text,remaining_quota text,current_time text)''')
        
    except:
        pass
if filestatus:
    connect()


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client = mqtt.Client('WaterManagement')
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address,port, 60)
client.username_pw_set(user,password)
client.loop_forever()
