#!/usr/bin/env python
""" A tool which is interacts with JIRA REST API to perform operations on tickets
 like create, edit, assign, etc..."""
from core import common
import logging
import sys

def main(action, project, ticket, filename, comment):
    logging.basicConfig(filename='logs/autojira.log', format='%(asctime)s %(levelname)s : %(message)s', datefmt='[ %Y-%m-%d %H:%M:%S ]', level=logging.DEBUG)
    
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
            logging.error('expected project key')
            sys.exit(1)
    elif action == "assign":
        if ticket != None:
            common.assgin_issue(ticket)
        else:
            logging.error('expected ticket id')
    elif action == "comment":
        if ticket != None:
            common.add_comment(ticket, comment)
        else:
            logging.error('expected ticket id')
    else:
        logging.error('%s is not valid action', action)
            
if __name__ == "__main__":
    logging.info("*** Welcome to JIRA Automation ***")
    args = common.process_args()
    main(args['action'], args['project'], args['ticket'], args['file'], args['comment'])
    