from solver import RankingProblem
from solver import RankingParser


def solve_challenge():
    statements = [
        "Jessie is not the best developer",
        "Evan is not the worst developer",
        "John is not the best developer or the worst developer",
        "Sarah is a better developer than Evan",
        "Matt is not directly below or above John as a developer",
        "John is not directly below or above Evan as a developer",
    ]

    print("\r".join(statements))
    print()

    print("Solving by specifying rules")
    print("=" * 30)
    r = RankingProblem()

    r.set_items(["Jessie", "Evan", "John", "Sarah", "Matt"]).\
        not_first("Jessie").not_last("Evan").\
        not_first("John").not_last("John").\
        is_before("Sarah", "Evan").\
        not_directly_before_or_after("Matt", "John").\
        not_directly_before_or_after("John", "Evan")

    solutions = r.solve()

    for s in solutions:
        print(s)

    print()

    print("Solving by parsing")
    print("=" * 30)

    rp = RankingParser()
    print(rp.parse_statements(statements))


def main_help():
    print("Rank Parser")
    print("Determine the order of things from textual descriptions")
    print("")
    print("Commands:")
    print("\thelp - display this help text.")
    print("\tchallenge - solve the 10x developer riddle.")
    print("\tquery - enter query mode to specify own riddle.")
    print("\tquit - to leave this place.")


def query():
    rp = RankingParser()
    rp.test()


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
