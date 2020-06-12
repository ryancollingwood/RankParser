from colorama import Fore, Back, Style

STYLE_MAP = {
    "ENTITY": Back.RESET + Style.BRIGHT + Fore.CYAN,
    "NOT": Back.RESET + Style.NORMAL + Fore.LIGHTRED_EX,
    "OR": Back.RESET + Style.NORMAL + Fore.LIGHTYELLOW_EX,
    "BETTER": Back.RESET + Style.NORMAL + Fore.GREEN,
    "WORSE": Back.RESET + Style.NORMAL + Fore.LIGHTMAGENTA_EX,
    "BEST": Back.RESET + Style.BRIGHT + Fore.GREEN,
    "WORST": Back.RESET + Style.BRIGHT + Fore.LIGHTMAGENTA_EX,
    "ERROR": Back.RESET + Style.BRIGHT + Fore.RED,
    "RESET": Fore.RESET + Style.NORMAL + Back.RESET,
}
