from colorama import Fore, Style

import sys
import subprocess
from . import styles

def clean_input(prompt: str, requirements: list[str], disallowances: list[str]) -> str:
    '''
    Get output that (if the wrong input is entered) resets the line with a customizable error message.

    :param prompt: The prompt used for the input
    :param requirements: What the user input must satisfy to continue
    :param disallowances: What the user input cannot be

    :type prompt: str
    :type requirements: list[str]
    :type disallowances: list[str]

    :return: Returns the correct user input, iterates until it returns this.
    :rtype: str
    '''
    error = ""
    has_error = False
    
    while True:
        # 1. Clear the error line from the previous iteration.
        # [*] \033[K clears from the cursor to the end of the line
        sys.stdout.write("\033[K" + error + "\r")
        
        # 2. If there was an error, move the cursor back to the input line
        # [*] \033[#A moves the cursor up # line(s)
        if has_error:
            sys.stdout.write("\033[2A")
        
        # 3. Clear the input line and replace with the prompt
        sys.stdout.write("\033[K" + prompt)
        # [*] Flush buffer
        sys.stdout.flush()
        
        # 4. Get input from the user
        u_input = sys.stdin.readline().strip()
        
        # 5. Validate the input
        # [*] Uses the requirements parameter to determine if the input
        # [*] can be accepted or not.
        if u_input in requirements:
            # [!] User input passes requirements, clear error slot
            if u_input in disallowances:
                # [^] Input was disallowed
                has_error = True
                error = styles.format_style(f"Error: No user data. Please select a different option.", "error")

                # Print a newline so the error message goes underneath the input
                sys.stdout.write("\n")
            else:
                # [!] Return user input - passed all tests
                sys.stdout.write("\n\033[K\033[1A\r")
                sys.stdout.flush()
                return u_input
        else:
            # [;] The loop failed to meet the requirements
            # [;] Set the error message for the next loop iteration
            has_error = True
            error = styles.format_style(f"Error: `{u_input}` is not a valid response. Please try again.", "error")
            
            # Print a newline so the error message goes underneath the input
            sys.stdout.write("\n")

def clear() -> None:
    '''
    Quickly and efficiently clears the screen

    :rtype: None
    '''

    subprocess.run("cls", shell=True)

def quit(code:str | int) -> None:
    '''
    Exits with exit code 0

    :param code: The exit code for the program
    :type code: str | int

    :rtype: None
    '''

    sys.exit(code)