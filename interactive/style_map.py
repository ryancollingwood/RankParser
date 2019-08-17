from colorama import Fore, Style

STYLE_MAP = {
    "PERSON": Style.BRIGHT + Fore.CYAN,
    "NOT": Style.NORMAL + Fore.LIGHTRED_EX,
    "OR": Style.NORMAL + Fore.LIGHTYELLOW_EX,
    "BETTER": Style.NORMAL + Fore.GREEN,
    "WORSE": Style.NORMAL + Fore.BLUE,
    "BEST": Style.BRIGHT + Fore.GREEN,
    "WORST": Style.BRIGHT + Fore.BLUE,
}
