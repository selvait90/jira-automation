#!/usr/bin/env python

# Collection of functions to work with JIRA tickets

# gettext internationalisation function requisite:
'''
Created on Jul 4, 2013

@author: Selvakumar Arumugam
'''
from jira.client import JIRA

jira = JIRA()
def create_issue(project):
    metadata = create_metadata(project)
    print metadata
#     for meta in metadata:
#         print meta.key
    """issue_dict = {'key' : 'DEV',
                 'summary' : 'Creating Issue from Code',
                                  
                 
                 }
    jira.create_issue(fields=issue_dict,)"""
    

def create_metadata(projectKeys, projectIds=None, issuetypeIds=None, issuetypeNames='Bug', expand='projects'):
    jira = configure_jira()
    metadata = jira.createmeta(projectKeys, projectIds, issuetypeIds, issuetypeNames, expand)
    return metadata

def configure_jira():
    server = 'http://localhost:8100'
    #jira = JIRA(options={'sever' : sever}, basic_auth=None, oauth=None)
    jira = JIRA(options={'server': server}, basic_auth=('selva', 'selva'), oauth=None)
    return jira

def list_projects():
    jira = configure_jira()
    projects = jira.projects()
    return projects

def assgin_issue(ticket):
    user = "selvait90"
    print "User : ", user,"Ticket : ", ticket
    jira = configure_jira()
    issue = jira.issue(ticket)
    jira.assign_issue(issue, user)
    
    
def process_args():
    print "Inside pares_args"
    import argparse
    parser = argparse.ArgumentParser(
                                     description='Manage JIRA tickets in a quick manner',
                                     epilog='Example : '                                     
                                     )
    parser.add_argument('-t', '--ticket',
                        dest='ticket',
                        help='specify the ticket number',
                        required=False,
                        type=str,                        
                        )
    parser.add_argument('-a', '--action',
                        dest='action',
                        choices=['list','create','update','close','assign'],
                        help='type of action to perform',
                        required=True,
                        type=str,
                        )
    parser.add_argument('-i', '--input',
                        dest='file',
                        help='input file path which contains data to create ticket',
                        required=False,
                        type=str,
                        )
    parser.add_argument('-p', '--project',
                        dest='project',
                        help='key value of the project',
                        required=False,
                        type=str,
                        )
    args = vars(parser.parse_args())
    return args
 
