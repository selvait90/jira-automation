Introduction
============

autojira is python tool which helps to interact with JIRA tickets 
and automates the operations to make life easier. 

See the wiki documentation for detailed information
https://github.com/selvait90/jira-automation/wiki

License 
=======
autojira is python tool to interact with JIRA 
Copyright (C)2013 Selvakumar Arumugam &lt;selvait90@gmail.com>

autojira is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

autojira is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with autojira.  If not, see &lt;http://www.gnu.org/licenses/>.

Pre-requisites
==============
python modules :
jira-python
argparse

Syntax and Sample Commands
==========================

list of projects in JIRA
------------------------
./autojira.py -a list

assign the ticket to me
------------------------
./autojira.py -a assign -t &lt;issue_id>

./autojira.py -a assign -t DEV-01

comment on the ticket
---------------------
./autojira.py -a comment -t &lt;issue_id> -c "your comment"

./autojira.py -a comment -t DEV-01 -c "I commented on ticket"

generate template file to create new issue
------------------------------------------
./autojira.py -a template -p &lt;project_key>

./autojira.py -a template -p DEV

create new issue
----------------
./autojira.py -a create -i conf/&lt;template-filename>

./autojira.py -a create -i conf/DEV-Bug
