# RankParser

# Introduction

This is a tutorial on using the RankParser application in a Linux or Mac terminal.
The tutorial was developed using Google Cloud Shell.

## Getting Started
In the terminal at the bottom of the screen type: 

```bash
chmod 775 ./go_macosx.sh
./go_macosx.sh
```

This will do the following:
- Allow us to execute the startup script
- Execute the startup script.

The startup scripts does the following: 
- Install the virtual environment Python module.
- Create a Python virtual environment.
- Activate the virtual environment.
- Install the required packages into the environment.
- Run the application tests.
- Launch the application. 

# Using the Application
Once the application is started the following commands are available to you.

- `help` - Display the available commands.
- `challenge` - Solve the 10x developer riddle.
- `query` - Enter query mode to specify own riddles.
- `quit` - Exit the application.

## Solving the challenge

The challenge to solve is as follows:
- **Jessie** is not the best developer
- **Evan** is not the worst developer
- **John** is not the best developer or the worst developer
- **Sarah** is a better developer than **Evan**
- **Matt** is not directly below or above **John** as a developer
- **John** is not directly below or above **Evan** as a developer

To see the solution to the above riddle type the following command:
```
challenge
```

## Imperative Problem Solving

The challenge is solved both through a imperative and declarative means.

The class `RankingProblem` is the imperative interface, as defined in 'solver/ranking_problem.py'

This class is descendant of the `Problem` from the `python-constraints` package. To see the documentation for this class, refer to: [Python Constraints Problem API](http://labix.org/doc/constraint/public/constraint.Problem-class.html)

## Declarative Problem Solving

Declarative solving is achieved using the PLY (Python Lex-Yacc) module. To see a detailed overview of the module and it's usage: [PLY Overview](https://www.dabeaz.com/ply/ply.html#ply_nn2).

### Lex - aka. converting text to tokens
The first part of the declarative solving is Lexxinng. Which can be summarised as parsing input from simple human readable text into tokens that are meaningful to the program. The matching of tokens is done using regular expressions.
To see the tokens and the regex patterns used to match them, as defined in `solver/ranking_lexer.py`.

### Yacc - aka. mapping patterns of tokens to functions
The second part of declarative solving is once we have extracted the tokens from user input is to match token pattern to desired functions of our imperative interface. This is the 'compiling' step (although we aren't generating a binary file, which is often associated with compiling in software development). 

This is achieved using doc string pattern matching on functions names starting with `p_` in the `RankingParser` class.
To see the token patterns and how they are mapped to the imperative interface, as defined in `solver/ranking_parser.py`.

# Interactive Mode
Given we have the means to parse simple textual descriptions into tokens and then match the tokens to a function call, it is possible to provide an interactive interface for solving ranking problems.

The `Session` class wraps the aforementioned lex and yacc steps into a interface where you can type the "rules" of your own ranking problems/riddles. Along with some basic highlighting for an improved user experience, as defined in `interactive/session.py`.

Next we'll review the syntax of defining ranking problems in the interactive mode.

## Query Syntax
To enter query mode enter the following command:
```
query
```

The prompt will change from `>` to `RankParser>` showing you've entered query mode.

If you enter query mode, you can enter your own riddles using using rank statements. These statements have a specific format that you need to follow.

The general format of a rank statement is: 
`<Person> <Relative Placement> <Person or Position>`

For example:
```
Ryan is not first
John is before Ryan
```

### Person
People are specified using proper case.
For example:
- `Ryan` is a valid
- `ryan` is not

### Relative Placement
The following terms are valid for determining the placement of People:
- `before <Person>`
- `after <Person>`
- `not <Position>`
- `not <Position>`
- `not <Position> or <Postion>`
- `not directly above or below <Person>`

### Position
There are two Positions we can refer to:
- `first`
- `last`

# Cleaning Up (Optional)

To exit the application type in the following command:
```
quit
```

Once you're done you might want to remove the RankParser application.
You can do this be entering the following into the terminal:
```bash
cd ..
rm -r -f RankParser/
```