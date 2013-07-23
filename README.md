jira-automation-docs
====================

User Documentation
------------------
# list of projects in JIRA
./autojira.py -a list

# assign the ticket to me
./autojira.py -a assign -t <issue_id>
Example :
./autojira.py -a assign -t DEV-01

# comment on the ticket
./autojira.py -a comment -t <issue_id> -c "<your comment>"
Example :
./autojira.py -a comment -t DEV-01 -c "I commented on ticket"

# generate template file to create new issue
./autojira.py -a template -p <project_key>
Example :
./autojira.py -a template -p DEV

# create new issue
./autojira.py -a create -i conf/<project_key>-<issue_type>
Example :
./autojira.py -a create -i conf/DEV-Bug