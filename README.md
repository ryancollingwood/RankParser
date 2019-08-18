# RankParser


## Overview

From textual descriptions of People and sequence (before, after, not first) get the potential orderings.

![RankParser in action](demo.gif "RankParser in action")

Using `python-constraint` for defining and solving the problem, and `ply` for lexing and parsing textual descriptions.

## Running

Assuming:
- Python 3.6+ installed
- `virtualenv` installed

I've created a go script for Windows and Mac. The go script will: 
- Create a virtual python environment.
- Install the requirements.
- Run the tests.
- Run the application.

### Mac and Linux:
`$ ./go_macosx.sh`

May need to `$ chmod 755 go_macosx.sh`

### Windows
`go_windows.bat`