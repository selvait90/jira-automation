#!/usr/bin/env python
""" A tool which is interacts with JIRA REST API to perform operations on tickets
 like create, edit, assign, etc..."""
from core import common

def main(action, project, ticket, filename):
    if action == "list":
        projects = common.list_projects()
        for project in projects:
            print project.key
    elif action == "create":
        if file != None:
            common.create_issue(filename)
    elif action == "template":
        if project != None:
            common.create_template(project)
        else:
            print "ERROR : Please enter the project key"
    elif action == "assign":
        if ticket != None:
            common.assgin_issue(ticket)
        else:
            print "ERROR : "
    elif action == "comment":
        if ticket != None:
            common.add_comment(ticket)
if __name__ == "__main__":
    print "*** Welcome to JIRA Automation ***"
    args = common.process_args()
    main(args['action'], args['project'], args['ticket'], args['file'])
    