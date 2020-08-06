# Smart Water Management System
## Team LilHax
### Problem
Global warming being a great issue of this era, requires solutions which help the present generation as well as helps in sustainable development. Human kind has been irresponsible in terms of water usage. We see inappropriate and excessive usage of water especially in Metropolitan cities, where people don’t actually value the natural resource. Our project deals with management of water and water flow from a small society to entire urban infrastructure. 
### Approach
* NodeMCU(ESP8266) is used as an interface to publish the gathered data to the MQTT broker.
* A python script running as a server subscribes to the topics, processes and stores the data in a SQL database.
* Cross platform app subscribes to the appropriate topics and displays the appropriate information to user and admin. 
<p align="center"><br><br><img src="Picture1.png" width="500" alt="accessibility text"></p><br><br>

### Outcomes

* It estimates the amount of water consumed by user on a day to day basis, which can be used to regulate water supply to a particular user. 
* It allows the admin to control the amount of water distributed to each user based on continuous evaluation. 
* It can also be used for remotely controlling the water flow, cutting the water supply, monitoring and analyzing the water consumption across different users, with the help of cross platform app and cloud connectivity. 
* Furthermore statistical data gathered can be used by govt. authorities for defining policies, strategies and billing calculations.
 

