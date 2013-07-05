#!/usr/bin/env python
# A tool which is interacts with JIRA REST API to perform operations on tickets
# like create, edit, assign, etc...
from core import common

def main(action, project):
    if action == "list":
        common.list_projects()
    elif action == "create":
        if project != None:
            common.create_issue(project)
        else:
            print "ERROR : Please enter the project key"
    
if __name__ == "__main__":
    print "*** Welcome to JIRA Automation ***"
    args = common.process_args()
    main(args['action'], args['project'])
    