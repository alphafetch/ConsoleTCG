from colorama import Fore, Back, Style

styles = {
    "error": Fore.RED + Style.BRIGHT,
    "success": Fore.GREEN + Style.BRIGHT,
    "bold_cyan": Fore.CYAN + Style.BRIGHT
}

# Used to print a styled message
def format_style(text: str, style: str) -> str:
    '''
    Return a styled message.

    :param text: The text to join with the style
    :param style: Types: error, success

    :type text: str
    :type style: str

    :return: The joined text of the style and the text parameter
    :rtype: str
    '''

    match style:
        case "error":
            return styles["error"] + text
        case "success":
            return styles["success"] + text
        case _:
            return text