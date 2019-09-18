import sys
from time import sleep
from colorama import Fore, Back, Style
from colorama import init as colorama_init
from solver import RankingProblem, RankingLexer
from solver import RankingParser
from interactive import HighLighter
from interactive import STYLE_MAP
from test_data import programmer_riddle, tea_steps
from interactive import Session


def solve_challenge():
    rl = RankingLexer()
    hl = HighLighter(rl, STYLE_MAP)

    print()

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


def solve_tea():
    ranking_problem = RankingProblem()

    ranking_problem.set_items([
        "Boil water in the kettle",
        "Pour boiled water into cup",
        "Get a cup from the cupboard",
        "Put tea bag into cup",
        "Drink tea",
    ])

    ranking_problem.not_first("Drink tea").\
        not_last("Boil water in the kettle").\
        is_before("Boil water in the kettle", "Pour boiled water into cup").\
        is_before("Get a cup from the cupboard", "Pour boiled water into cup").\
        is_after("Put tea bag into cup", "Get a cup from the cupboard").\
        is_before("Put tea bag into cup", "Drink tea").\
        is_before("Pour boiled water into cup", "Drink tea")

    solutions = ranking_problem.solve()
    print(solutions)

# for a bit of fun as per: https://stackoverflow.com/a/29932609/2805700
def typewrite_print(words):
    for char in words:
        sleep(0.05)
        sys.stdout.write(char)
        sys.stdout.flush()
    print("\n")


def main_help():
    print(Style.RESET_ALL)
    print(Style.BRIGHT + Fore.CYAN + "Rank Parser" + Fore.RESET + Style.NORMAL)
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
        elif command == "tea":
            solve_tea()
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
    colorama_init()

    main()

    print("")
    input("Press any key to exit...")
