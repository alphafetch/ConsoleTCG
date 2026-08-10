from colorama import Fore, Back, Style

styles = {
    "error": Fore.RED + Style.BRIGHT,
    "success": Fore.GREEN + Style.BRIGHT,
    "bold_cyan": Fore.CYAN + Style.BRIGHT,
    "warn": Fore.YELLOW + Style.NORMAL,
    "progress": Fore.MAGENTA + Style.NORMAL,
    "cyan_back": Fore.BLACK + Back.CYAN + Style.NORMAL,
    "cyan": Fore.CYAN + Style.NORMAL,
    "red": Fore.RED + Style.NORMAL,
    "yellow": Fore.YELLOW + Style.NORMAL,
    "green": Fore.GREEN + Style.NORMAL,
    "bright_red": Fore.LIGHTRED_EX + Style.NORMAL
}

# Used to print a styled message
def format_style(text: str, style: str) -> str:
    '''
    Return a styled message.

    :param text: The text to join with the style
    :type text: str
    
    :param style: Types: error, success
    :type style: str

    :return: The joined text of the style and the text parameter
    :rtype: str
    '''

    return styles[style] + text

def clear_styles() -> str:
    '''
    Clears any remaining styles.

    :return: The reset code
    :rtype: str
    '''

    return Style.RESET_ALL