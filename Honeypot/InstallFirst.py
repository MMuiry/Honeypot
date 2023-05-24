#!/usr/bin/env python3


import subprocess
#update packages
subprocess.run(["sudo", "apt", "update"])
packagePip = "python3-pip"

#install/update pip
result = subprocess.run(["dpkg", "-s", packagePip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if result.returncode == 0:
    print(packagePip + " is already installed.")
    subprocess.run(["sudo", "pip3", "install", "--upgrade" , "pip"])
else:
    print(packagePip + " is not installed on this system. Installing it now...")
    # Install pip
    subprocess.run(["sudo", "apt-get","-y", "install", packagePip])
import os

#create log file
subprocess.run(["sudo", "touch", "ActivityLogs.txt"])


packageSSHServer = "openssh-server"

packageTelnet = "openbsd-inetd"
packageFtp = "vsftpd";


#installing Web
#configure files and add directorys to setup webpages and logs correctly
username = os.environ.get('SUDO_USER')
documents_path = os.path.join('/home', username, 'Documents')
subprocess.run(["sudo", "apt", "-y", "install", "apache2"])
subprocess.run(["sudo", "mkdir", "/var/www/html/lowInteraction"])
subprocess.run(["sudo", "mkdir", "/var/www/html/medInteraction"])
subprocess.run(["sudo", "cp", f"{documents_path}/Honeypot/htmlpage/indexLow.html", "/var/www/html/lowInteraction/index.html"])
subprocess.run(["sudo", "cp", f"{documents_path}/Honeypot/htmlpage/low.css", "/var/www/html/lowInteraction/home.css"])
subprocess.run(["sudo", "cp", f"{documents_path}/Honeypot/htmlpage/websiteBackground.jpg", "/var/www/html/lowInteraction/websiteBackground.jpg"])
subprocess.run(["sudo", "chmod", "644", "websiteBackground.jpg"])
subprocess.run(["sudo", "cp", f"{documents_path}/Honeypot/htmlpage/indexMed.html", "/var/www/html/medInteraction/index.html"])
subprocess.run(["sudo", "cp", f"{documents_path}/Honeypot/htmlpage/medium.css" , "/var/www/html/medInteraction/login.css"])



## Create the MedInteraction virtual host configuration file to get logs
subprocess.run(['sudo', 'bash', '-c', f"echo '<VirtualHost *:80>\n    DocumentRoot /var/www/html/medInteraction\n    ServerName honeypot.example.com\n    ErrorLog {documents_path}/Honeypot/htmlpage/htmlMederror.log\n    CustomLog {documents_path}/Honeypot/htmlpage/htmlMedlog.log combined\n    DumpIOInput On\n    DumpIOOutput On\n    LogLevel dumpio:trace7\n</VirtualHost>' > /etc/apache2/sites-available/medHoneypot.conf"])





# Create the lowInteraction virtual host configuration file to get logs

subprocess.run(['sudo', 'bash', '-c', f"echo '<VirtualHost *:80>\n    DocumentRoot /var/www/html/lowInteraction\n    ServerName honeypot.example.com\n    ErrorLog {documents_path}/Honeypot/htmlpage/htmlLowerror.log\n    CustomLog {documents_path}/Honeypot/htmlpage/htmlLowlog.log combined\n</VirtualHost>' > /etc/apache2/sites-available/lowHoneypot.conf"])
subprocess.run(["sudo", "a2enmod", "dump_io"])


#Checks if SSH service is installed. if not, install it
result = subprocess.run(["dpkg", "-s", packageSSHServer], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if result.returncode == 0:
    print(packageSSHServer + " is already installed.")
else:
    print(packageSSHServer + " is not installed on this system. Installing it now...")
    # Install openssh-server

    subprocess.run(["sudo", "apt-get","-y", "install", packageSSHServer])



#install telnet service
result = subprocess.run(["dpkg", "-s", "telnetd"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if result.returncode == 0:
    print("telnetd is already installed.")
else:
    print(packageTelnet + " is not installed on this system. Installing it now...")
    # Install Telnet-server

    subprocess.run(["sudo", "apt-get","-y", "install", "telnetd"])

result = subprocess.run(["dpkg", "-s", "xinetd"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if result.returncode == 0:
    print("xinetd is already installed.")
else:
    print("xinetd is not installed on this system. Installing it now...")
    subprocess.run(["sudo", "apt-get","-y", "install", "xinetd"])


# Write to /etc/inetd.conf
inetd_conf_contents = 'telnet stream tcp nowait telnetd /usr/sbin/tcpd /usr/sbin/in.telnetd'
with open('/etc/inetd.conf', 'w') as f:
    f.write(inetd_conf_contents)

# Write to /etc/xinetd.conf
xinetd_conf_contents = """# Simple configuration file for xinetd
#
# Some defaults, and include /etc/xinetd.d/
defaults
{
    instances = 60
    log_type = SYSLOG authpriv
    log_on_success = HOST PID
    log_on_failure = HOST
    cps = 25 30
}"""
with open('/etc/xinetd.conf', 'w') as f:
    f.write(xinetd_conf_contents)

# Write to /etc/xinetd.d/telnet
telnet_conf_contents = """# default: on
# description: The telnet server serves telnet sessions; it uses
# unencrypted username/password pairs for authentication.
service telnet
{
    disable = no
    flags = REUSE
    socket_type = stream
    wait = no
    user = root
    server = /usr/sbin/in.telnetd
    log_on_failure += USERID
}"""
with open('/etc/xinetd.d/telnet', 'w') as f:
    f.write(telnet_conf_contents)



#Checks FTP service is installed. if not, install it
result = subprocess.run(["dpkg", "-s", packageFtp], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if result.returncode == 0:
    print(packageFtp + " is already installed.")
else:
    print(packageFtp + " is not installed on this system. Installing it now...")
    # Install Ftp-server

    subprocess.run(["sudo", "apt-get","-y", "install", packageFtp])

#creates log file as it can result in errer if one hasn't been created because no one has connect via ftp yet
subprocess.run(["sudo", "touch", "/var/log/vsftpd.log"])



#Checks if Nmap service is installed. if not, install it
result = subprocess.run(["dpkg", "-s", "nmap"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if result.returncode == 0:
    print("Nmap is already installed.")
else:
    print("Nmap is not installed on this system. Installing it now...")
    # Install Nmap

    subprocess.run(["sudo", "apt-get","-y", "install", "nmap"])

#python modules install

#checks for getch install, if not, install
try:

    import getch
    print("getch python module installed")

except ModuleNotFoundError:

    print("getch python module is not installed on this system. Installing it now...")
    subprocess.run(["sudo", "pip3", "install", "getch"])

#keyboard install
try:

    import keyboard
    print("keyboard python module installed")

except ModuleNotFoundError:

    print("keyboard python module is not installed on this system. Installing it now...")
    subprocess.run(["sudo", "pip3", "install", "keyboard"])

#scapy install
try:

    import scapy
    print("scapy python module installed")

except ModuleNotFoundError:

    print("scapy python module is not installed on this system. Installing it now...")
    subprocess.run(["sudo", "pip3", "install", "scapy"])
#nmap module install
try:

    import nmap
    print("nmap python module installed")

except ModuleNotFoundError:

    print("nmap python module is not installed on this system. Installing it now...")
    subprocess.run(["sudo", "pip", "install", "python-nmap"])





