from colorama import Fore, Style

import sys

def clean_input(prompt: str, requirements: list[str]) -> str:
    '''
    Get output that (if the wrong input is entered) resets the line with a customizable error message.

    :param prompt: The prompt used for the input
    :param requirements: What the user input must satisfy to continue

    :type prompt: str
    :type requirements: list[str]

    :return: Returns the correct user input, iterates until it returns this.
    :rtype: str
    '''
    error = ""
    has_error = False
    
    while True:
        # 1. Clear the error line from the previous iteration.
        # INFO: \033[K clears from the cursor to the end of the line
        sys.stdout.write("\033[K" + error + "\r")
        
        # 2. If there was an error, move the cursor back to the input line
        # INFO: \033[#A moves the cursor up # line(s)
        if has_error:
            sys.stdout.write("\033[2A")
        
        # 3. Clear the input line and replace with the prompt
        sys.stdout.write("\033[K" + prompt)
        # INFO: Flush buffer
        sys.stdout.flush()
        
        # 4. Get input from the user
        u_input = sys.stdin.readline().strip()
        
        # 5. Validate the input
        # INFO: Uses the requirements parameter to determine if the input
        # *     can be accepted or not.
        if u_input in requirements:
            # [!] User input passes requirements, clear error slot
            # [!] and return the input to the function call
            sys.stdout.write("\n\033[K\033[1A\r")
            sys.stdout.flush()
            return u_input
        else:
            # [;] The loop failed to meet the requirements
            # [;] Set the error message for the next loop iteration
            has_error = True
            error = Fore.RED + Style.BRIGHT + f"Error: `{u_input}` is not a valid response. Please try again."
            
            # Print a newline so the error message goes underneath the input
            sys.stdout.write("\n")