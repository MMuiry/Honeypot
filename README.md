# Honeypot
This is a honeypot honours project created for ubuntu OS with Raspberry Pi and ease of use in mind 

Capabilitys:
logs services listed - ssh,telnet,ftp,http.
As of right now, only http has medium interaction

Information on honeypot 
Honours Honeypot install instructions or watch Yotube video here - (https://www.youtube.com/watch?v=2Jpk63-NUGE&ab_channel=XxMuiryxX).

1. Place the whole "Honeypot" folder in the documents folder at /home/[username]/Documents/ 

2. Open command terminal and type "cd /home/[Username]/Document/Honeypot/". [Username] can be seen to the left of the command line interface before the "@". In the picture, the username is "honeypot".Don't include the brackets![image](https://github.com/MMuiry/Honeypot/assets/97714730/a2085486-5d32-44c9-9c8e-b514e7a874b9).

3.  In the command terminal, run "sudo python3 /home/[Username]/Documents/Honeypot/InstallFirst.py".
This can take a minute or two. 



. To use the application, just type in the terminal "sudo python3 /home/[Username]/Documents/Honeypot/Start.py" and use either buttons or 
keyboard c

To read the logs again, open "ActivityLogs.txt"


GPIO config (not nessary if buttons arn't wanting to be used):
GPIO 2 = Up button
GPIO 3 = Select button
GPIO 4 = Down button
