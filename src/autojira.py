#!/usr/bin/env python

"""
This file is part of autojira.
Copyright (C)2013 Selvakumar Arumugam <selvait90@gmail.com>

autojira is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

autojira is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with autojira.  If not, see <http://www.gnu.org/licenses/>.
"""

from core import common
import logging
import sys

""" A tool which is interacts with JIRA REST API to perform operations on tickets
 like create, edit, assign, etc...
 """

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
    