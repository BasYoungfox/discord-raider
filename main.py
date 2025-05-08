import requests
from colorama import Fore, Back, Style, init
import shutil
import os

init(autoreset=True)

def center_text(text):
    terminal_width = shutil.get_terminal_size().columns
    lines = text.split("\n")
    return "\n".join(line.center(terminal_width) for line in lines)

def print_clean_banner():
    os.system("cls")
    banner = '''
  _   _ _____ ____ _____ _   _ _   _ _____ 
 | \ | | ____|  _ \_   _| | | | \ | | ____|
 |  \| |  _| | |_) || | | | | |  \| |  _|  
 | |\  | |___|  __/ | | | |_| | |\  | |___ 
 |_| \_|_____|_|    |_|  \___/|_| \_|_____| 
                                           
    '''
    print(Fore.BLUE + Style.BRIGHT + center_text(banner))
    
    # Display number of tokens loaded
    with open('tokens.txt', 'r') as f:
        tokens = [line.strip() for line in f if line.strip()]
    print(Fore.BLUE + center_text(f"Tokens loaded: {len(tokens)}\n"))

def print_questions():
    print(Fore.BLUE + " " * 40 + f"{Fore.WHITE}[{Fore.BLUE}~{Fore.WHITE}]{Fore.BLUE}    Message: ", end="")
    message = input(Fore.WHITE).strip()
    
    print(Fore.BLUE + " " * 40 + f"{Fore.WHITE}[{Fore.BLUE}~{Fore.WHITE}]{Fore.BLUE}    Channel ID: ", end="")
    channel_id = input(Fore.WHITE).strip()

    return message, channel_id

def display_progress(status, partial_token):
    if status == "Sent":
        progress_message = f"{Fore.WHITE}[{Fore.BLUE}~{Fore.WHITE}]{Fore.BLUE} Sent | {partial_token}"
    else:
        progress_message = f"{Fore.WHITE}[{Fore.RED}~{Fore.WHITE}]{Fore.BLUE} Failed |{partial_token}"
    
    print(" " * 40 + (progress_message))

print_clean_banner()

message, channel_id = print_questions()

with open('tokens.txt', 'r') as f:
    tokens = [line.strip() for line in f if line.strip()]

url = f'https://discord.com/api/v9/channels/{channel_id}/messages'

while True:
    if not hasattr(print_clean_banner, "printed"):
        print_clean_banner()
        print_clean_banner.printed = True

    for token in tokens:
        headers = {
            'authorization': token
        }

        try:
            payload = {'content': message}
            response = requests.post(url, data=payload, headers=headers)
            partial_token = token[:20] + "*" * 10

            if response.status_code == 200:
                display_progress("Sent", partial_token)
            else:
                display_progress("Failed", partial_token)

        except requests.exceptions.RequestException as e:
            partial_token = token[:10] + "..."
            display_progress("Failed", partial_token)
