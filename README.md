# RankParser

## Overview

From textual descriptions of People and sequence (before, after, not first) get the potential orderings.

![RankParser in action](resources/demo.gif "RankParser in action")

Using `python-constraint` for defining and solving the problem, and `ply` for lexing and parsing textual descriptions.

## Syntax

See [the tutorial](resources/tutorial.md) for a detailed view of the syntax.

## Preview in Google Cloud Shell
[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/ryancollingwood/RankParser&tutorial=resources/tutorial.md)

This will create an temporary playground in Google Cloud for you to see the application in action. 
It does require a Google Cloud account, as of August 2019 there is no charge for using Google Cloud Shell ([link](https://cloud.google.com/shell/pricing)).   

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