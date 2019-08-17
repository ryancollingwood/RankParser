import sys
from time import sleep
from colorama import Fore, Back, Style
from colorama import init as colorama_init
from solver import RankingProblem
from solver import RankingParser
from solver import RankingLexer
from interactive import HighLighter
from interactive import STYLE_MAP
from test_data import programmer_riddle
from interactive import Session

colorama_init()


def solve_challenge():
    rl = RankingLexer()
    hl = HighLighter(rl, STYLE_MAP)

    for s in programmer_riddle:
        print(hl.highlight(s))

    print()
    print("Solving by specifying rules")
    print(Fore.CYAN + ("=" * 30) + Fore.RESET)
    r = RankingProblem()

    r.set_items(["Jessie", "Evan", "John", "Sarah", "Matt"]).\
        not_first("Jessie").not_last("Evan").\
        not_first("John").not_last("John").\
        is_before("Sarah", "Evan").\
        not_directly_before_or_after("Matt", "John").\
        not_directly_before_or_after("John", "Evan")

    solutions = r.solve()

    for s in solutions:
        typewrite_print(", ".join(s))

    print()

    print("Solving by parsing")
    print(Fore.CYAN + ("=" * 30) + Fore.RESET)

    rp = RankingParser()
    typewrite_print(", ".join(rp.parse_statements(programmer_riddle)))


# for a bit of fun as per: https://stackoverflow.com/a/29932609/2805700
def typewrite_print(words):
    for char in words:
        sleep(0.05)
        sys.stdout.write(char)
        sys.stdout.flush()
    print("\n")

def main_help():
    typewrite_print(Style.BRIGHT + Fore.CYAN + "Rank Parser" + Fore.RESET + Style.NORMAL)
    print("Determine the order of things from textual descriptions")
    print("")
    print("Commands:")
    print("\t" + Style.BRIGHT + "help" + Style.NORMAL + " - display this help text.")
    print("\t" + Style.BRIGHT + "challenge" + Style.NORMAL + " - solve the 10x developer riddle.")
    print("\t" + Style.BRIGHT + "query" + Style.NORMAL + " - enter query mode to specify own riddle.")
    print("\t" + Style.BRIGHT + "quit" + Style.NORMAL + " - to leave this place.")


def query():
    session = Session()
    session.start()


def main():
    main_help()

    while True:
        command = input(">").strip().lower()
        if command == "challenge":
            solve_challenge()
        elif command == "help":
            main_help()
        elif command == "query":
            query()
            # assuming if quit is called in query mode
            # user wants to quit entirely
            break
        elif command == "quit":
            break


if __name__ == "__main__":
    main()

    print("")
    input("Press any key to exit...")
