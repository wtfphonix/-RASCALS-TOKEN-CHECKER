import os
import threading
import requests
from datetime import datetime
from colorama import Fore, Style, init
from pystyle import Colors, Colorate

# Initialize colorama
init(autoreset=True)

# Constants
KEY_FILE = 'tokens.txt'
OUTPUT_DIR = 'output'
WORKING_FILE = os.path.join(OUTPUT_DIR, 'working.txt')
INVALID_FILE = os.path.join(OUTPUT_DIR, 'invalid.txt')

# ASCII Art (High Saturation Blue-to-White)
ascii_art = """  

                                  ████████╗ ██████╗ ██╗  ██╗███████╗███╗   ██╗
                                  ╚══██╔══╝██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║
                                     ██║   ██║   ██║█████╔╝ █████╗  ██╔██╗ ██║
                                     ██║   ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║
                                     ██║   ╚██████╔╝██║  ██╗███████╗██║ ╚████║
                                     ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝

                               ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗
                              ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
                              ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝
                              ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗
                              ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║
                               ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                              ════════════════════════════════════════════════════════
                                      TOKEN CHECKER || PHONIX || .GG/RASCALS
                              ════════════════════════════════════════════════════════
"""

# Function to display the ASCII Art permanently
def display_ascii():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
    print(Colorate.Vertical(Colors.cyan_to_blue, ascii_art))  # Bright Blue-to-White gradient

# Create output directory and files if they don't exist
def createfile():
    if not os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'w') as file:
            file.write('')
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    for filename in [WORKING_FILE, INVALID_FILE]:
        with open(filename, 'w') as file:
            file.write('')
    log_info("CREATED FILES AND FOLDER.")

# Function to format log messages with high-saturation colors
def log_info(message):
    timestamp = datetime.now().strftime("[%m/%d/%y %H:%M:%S]")  # [MM/DD/YY HH:MM:SS]
    print(f"{Fore.LIGHTMAGENTA_EX}{timestamp} {Fore.LIGHTBLUE_EX}[INFO] {Fore.LIGHTGREEN_EX}{message}")

# Function to check if a token is valid
def checktokens(token):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
        return response.status_code == 200  # True if valid, False otherwise
    except requests.exceptions.RequestException as e:
        print(f"{Fore.LIGHTRED_EX}ERROR: {e}")
        return False

# Process tokens from file
def processtokens():
    with open(KEY_FILE, 'r') as f:
        tokens = f.readlines()
    
    total = len(tokens)
    log_info(f"LOADED {total} TOKENS")

    threads = []
    
    for token in tokens:
        token = token.strip()
        thread = threading.Thread(target=process_chunk, args=(token,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Process each token
def process_chunk(token):
    current_time = datetime.now().strftime("[%m/%d/%y %H:%M:%S]")  # Format: [MM/DD/YY HH:MM:SS]

    # Mask token for security
    masked_token = token[:10] + "****************"

    if checktokens(token):
        with open(WORKING_FILE, 'a') as working_file:
            working_file.write(token + '\n')
        print(f"{Style.BRIGHT}{Fore.MAGENTA}{current_time}{Fore.BLUE}[INFO]{Fore.GREEN}VALID{Fore.CYAN}[{masked_token}]")
    else:
        with open(INVALID_FILE, 'a') as invalid_file:
            invalid_file.write(token + '\n')
        print(f"{Style.BRIGHT}{Fore.MAGENTA}{current_time}{Fore.BLUE}[INFO]{Fore.RED}INVALID{Fore.CYAN}[{masked_token}]")


if __name__ == '__main__':
    display_ascii()  # Show ASCII Art at the start
    createfile()  # Create necessary files and folders
    processtokens()  # Start processing tokens
