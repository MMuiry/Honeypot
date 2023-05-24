import subprocess
import os
import threading
import time
wouldyou = "no"
import RPi.GPIO as GPIO
import nmap 
import warnings

# Filter the RuntimeWarning category
warnings.filterwarnings("ignore", category=RuntimeWarning)
#defines pins (CHANGE GPIO NUMBER HERE IF DIFFRENT PINS ARE USED)
UP_PIN = 2
DOWN_PIN = 4
SELECT_PIN = 3
#sets buttons up
GPIO.setmode(GPIO.BCM)
GPIO.setup(UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SELECT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
options = 0
customList = []
current_selection = 0
#pages represent what menu the user is on.
page = "main"
ipScanNum = 0
ignoreFirstTap = False

#moves selected option upwards on button press
def up_button_handler(channel):
    global current_selection
    global page
    if page == "main":
        if current_selection == 0:
            current_selection = 5
        else:
            current_selection -= 1    
        printrefresh()   

    if page == "custom":
        global customList
        if current_selection == 0:
            current_selection = 6
        else:
            current_selection -= 1    
        printrefresh() 
           


        
#moves selected option downward on button press
def down_button_handler(channel):


    global current_selection
    global page
    global ipScanNum
    if page == "main":
        
        if current_selection == 5:
            current_selection = 0
        else:
            current_selection += 1    
        printrefresh()
    
    if page == "custom":
        global customList
        if current_selection == 6:
            current_selection = 0
        else:
            current_selection += 1    
        printrefresh()
    if page == "scan":
        ipScanNum
        

#allows the user to select option on button press
def select_button_handler(channel):
    global ignoreFirstTap
    #stops button press when button is pressed on diffrent script
    if ignoreFirstTap == True:
        time.sleep(0.75) 

    global current_selection
    global page
    global customList
    #For main page
    if page == "main":
        if current_selection == 0:
            file_path = "chosenservices.txt"
            #writes the services selected to file to allow other script to read it 
            with open(file_path, "w") as file:
                 file.write("22l\n")
                 file.write("21l\n")
            ignoreFirstTap = True
            #runs logging script
            subprocess.run(["python3", "StartServices.py"])
            subprocess.run(["python3", "logging.py"])
            
            page = "main"
            print("What interaction level would you like to run?\n1. Low\n2. Medium\n3. Custom\n4. Scan local Machine\n5. Stop running services")
            print("running...")
        #runs medium leve interaction
        if current_selection == 1:
            file_path = "chosenservices.txt"
            with open(file_path, "w") as file:
                 file.write("80m\n")
                 file.write("22l\n")
                 file.write("21l\n")
            ignoreFirstTap = True
            subprocess.run(["python3", "StartServices.py"])
            subprocess.run(["python3", "logging.py"])
            page = "main"
            print("What interaction level would you like to run?\n1. Low\n2. Medium\n3. Custom\n4. Scan local Machine\n5. Stop running services")
        #runs custom interaction moving them to a diffrent page
        if current_selection == 2:
            page = "custom"
            current_selection = 0
            os.system('clear')
            printrefresh()
            return
        #stops services
        if current_selection == 3:
            subprocess.run(["sudo", "python3", "stopservices.py"])
            printrefresh()
        if current_selection == 4:
            sys.exit()
    #for the menu which allows the user to choice indiviual services
    if page == "custom":
        #user selecting their services
        if current_selection == 0:
            if "21l" in customList:
                customList.remove("21l")
            else:
                customList.append("21l")
        if current_selection == 1:
            if "22l" in customList:
                customList.remove("22l")
            else:
                customList.append("22l")
        if current_selection == 2:
            if "23l" in customList:
                customList.remove("23l")
            else:
                customList.append("23l")
        if current_selection == 3:
            if "80l" in customList:
                customList.remove("80l")
            else:
                customList.append("80l")
            if "80m" in customList:
                 customList.remove("80m")
        if current_selection == 4:
            if "80m" in customList:
                customList.remove("80m")
            else:
                customList.append("80m")
            if "80l" in customList:
                customList.remove("80l")
        #starting services
        if current_selection == 5:
            file_path = "chosenservices.txt"
            with open(file_path, 'w') as file:
                for service in customList:
                    file.write(service + "\n") 
            ignoreFirstTap = True
            subprocess.run(["python3", "StartServices.py"])
            subprocess.run(["python3", "logging.py"])
            #returns user to main page when ending the logging
            page = "main"
            print("What interaction level would you like to run?\n1. Low\n2. Medium\n3. Custom\n4. Scan local Machine\n5. Stop running services")
        #takes them back to main menu
        if current_selection == 6:
           page = "main"
        current_selection = 0
        printrefresh()

        



def printrefresh():
    global current_selection
    global page
    global customList
    os.system('clear')
    #prints the same statement but changes where the arrow is depending on the user current selection
    if page == "main":
        if current_selection == 0:
            print("What interaction level would you like to run?\n->1. Low - for Basic detection\n2. Medium - for more details about the attack\n3. Custom\n4. Scan local Machine to copy services\n5. Stop running services\n6. Quit")
        elif current_selection == 1:
            print("What interaction level would you like to run?\n1. Low - for Basic detection\n->2. Medium - for more details about the attack\n3. Custom\n4. Scan local Machine to copy services\n5. Stop running services\n6. Quit")
        elif current_selection == 2:
            print("What interaction level would you like to run?\n1. Low - for Basic detection\n2. Medium - for more details about the attack\n->3. Custom\n4. Scan local Machine to copy services\n5. Stop running services\n6. Quit")
        elif current_selection == 3:
            print("What interaction level would you like to run?\n1. Low - for Basic detection\n2. Medium - for more details about the attack\n3. Custom\n->4. Scan local Machine to copy services\n5. Stop running services\n6. Quit")
        elif current_selection == 4:
            print("What interaction level would you like to run?\n1. Low - for Basic detection\n2. Medium - for more details about the attack\n3. Custom\n4. Scan local Machine to copy services\n->5. Stop running services\n6. Quit")
        elif current_selection == 5:
            print("What interaction level would you like to run?\n1. Low - for Basic detection\n2. Medium - for more details about the attack\n3. Custom\n4. Scan local Machine to copy services\n5. Stop running services\n->6. Quit")  
    #same as above but with a diffrent menu
    if page == "custom":       
        if current_selection == 0:
            print("What service would you like to use (", *customList ,"):\n->1. 21 FTP low\n2. 22 SSH low\n3. 23 Telnet low\n4. 80 http low\n5. 80 http medium\n6. Start\n7. Back")
        if current_selection == 1:
            print("What service would you like to use (", *customList ,"):\n1. 21 FTP low\n->2. 22 SSH low\n3. 23 Telnet low\n4. 80 http low\n5. 80 http medium\n6. Start\n7. Back")            
        if current_selection == 2:
            print("What service would you like to use (", *customList ,"):\n1. 21 FTP low\n2. 22 SSH low\n->3. 23 Telnet low\n4. 80 http low\n5. 80 http medium\n6. Start\n7. Back")            
        if current_selection == 3:
            print("What service would you like to use (", *customList ,"):\n1. 21 FTP low\n2. 22 SSH low\n3. 23 Telnet low\n->4. 80 http low\n5. 80 http medium\n6. Start\n7. Back")            
        if current_selection == 4:
             print("What service would you like to use (", *customList ,"):\n1. 21 FTP low\n2. 22 SSH low\n3. 23 Telnet low\n4. 80 http low\n->5. 80 http medium\n6. Start\n7. Back")           
        if current_selection == 5:
            print("What service would you like to use (", *customList ,"):\n1. 21 FTP low\n2. 22 SSH low\n3. 23 Telnet low\n4. 80 http low\n5. 80 http medium\n->6. Start\n7. Back")            
        if current_selection == 6:
            print("What service would you like to use (", *customList ,"):\n1. 21 FTP low\n2. 22 SSH low\n3. 23 Telnet low\n4. 80 http low\n5. 80 http medium\n6. Start\n->7. Back")            



# Set up threads to listen for button events
GPIO.add_event_detect(UP_PIN, GPIO.FALLING, callback=up_button_handler, bouncetime=200)
GPIO.add_event_detect(DOWN_PIN, GPIO.FALLING, callback=down_button_handler, bouncetime=200)
GPIO.add_event_detect(SELECT_PIN, GPIO.FALLING, callback=select_button_handler, bouncetime=200)




#above code is for the buttons
#below code is for when the user wants to use a keyboard instead
#both do the same things
while True:
    #first menu 
    print("What interaction level would you like to run?\n1. Low\n2. Medium\n3. Custom\n4. Scan local Machine\n5. Stop running services\n6. Quit")
    wouldyou = input("Choice(1-6) : ")
    if page == "custom":
        wouldyou = "3"
    if page == "scan":
        wouldyou = "4"
    #start low logging
    if wouldyou == "1":
        file_path = "chosenservices.txt"
        with open(file_path, "w") as file:
             file.write("22l\n")
             file.write("21l\n")
        ignoreFirstTap = True
        subprocess.run(["sudo", "python3", "StartServices.py"])
        subprocess.run(["sudo", "python3", "logging.py"])
        


    #starts medium logging
    if wouldyou == "2":
        file_path = "chosenservices.txt"
        with open(file_path, "w") as file:
             file.write("80m\n")
             file.write("22l\n")
             file.write("21l\n")
        ignoreFirstTap = True
        subprocess.run(["sudo", "python3", "StartServices.py"])
        subprocess.run(["sudo", "python3", "logging.py"])
    
    #shows new menu for custom services
    if wouldyou == "3":
        while True:
            #user can type in the services they want
            print("\nWhat service would you like to use (", *customList ,"):\n1. 21 FTP low\n2. 22 SSH low\n3. 23 Telnet low\n4. 80 http low\n5. 80 http medium\n6. Start\n7. Back")
            customService= input("Choice(1-7) :  ")
            customList = []
            if customService == "1":
                if "21l" in customList:
                    customList.remove("21l")
                else:
                    customList.append("21l")
            if customService == "2":
                if "22l" in customList:
                    customList.remove("22l")
                else:
                    customList.append("22l")
            if customService == "3":
                if "23l" in customList:
                    customList.remove("23l")
                else:
                    customList.append("23l")
            if customService == "4":
                if "80l" in customList:
                    customList.remove("80l")
                else:
                    customList.append("80l")
                if "80m" in customList:
                    customList.remove("80m")
            if customService == "5":
                if "80m" in customList:
                    customList.remove("80m")
                else:
                    customList.append("80m")
                if "80l" in customList:
                    customList.remove("80l")
            if customService == "6":
                file_path = "chosenservices.txt"
                with open(file_path, 'w') as file:
                    for service in customList:
                        file.write(service + "\n") 
                ignoreFirstTap = True
                subprocess.run(["sudo", "python3", "StartServices.py"])
                subprocess.run(["sudo", "python3", "logging.py"])
            if customService == "7":
               break


    #scans local ip address and uses those services
    if wouldyou == "4":
        nm = nmap.PortScanner()
        print("enter ip address you would like to copy the services from")
        ip_address = input("Address: ")
        try:
            nm.scan(ip_address, '21-443')
            open_ports = []
            for port in nm[ip_address]['tcp']:
                if nm[ip_address]['tcp'][port]['state'] == 'open':
                    open_ports.append(port)
            if 21 in open_ports:
                customList.append("21l")
            if 22 in open_ports:
                customList.append("22l")
            if 23 in open_ports:
                customList.append("23l")
            if 80 in open_ports:
                customList.append("80l")        
            file_path = "chosenservices.txt"
            with open(file_path, 'w') as file:
                for service in customList:
                    file.write(service + "\n") 
            ignoreFirstTap = True
            subprocess.run(["sudo", "python3", "StartServices.py"])
            subprocess.run(["sudo", "python3", "logging.py"])
        except:
        	print("\nIP address invalid or not found on network\n")
        	 
    #ends running services
    if wouldyou == "5":
        subprocess.run(["sudo", "python3", "stopservices.py"])
    #ends
    if wouldyou == "6":
        break








