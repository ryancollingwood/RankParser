# RankParser

# Introduction

This is a tutorial on using the RankParser application in a Linux or Mac terminal.
The tutorial was developed using Google Cloud Shell.

## Getting Started
In the terminal at the bottom of the screen type: 

`./go_macosx.sh`

This will do the following:
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
	
## Query Syntax
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