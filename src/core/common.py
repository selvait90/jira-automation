#!/usr/bin/env python

""" Collection of functions to work with JIRA tickets

 gettext internationalisation function requisite:"""
'''
Created on Jul 4, 2013

@author: Selvakumar Arumugam
'''
from jira.client import JIRA
import cStringIO
import ConfigParser

jira = JIRA()
def create_issue(filename):
    jira = configure_jira()
    print "Creating issue"
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.read(filename)
    issuefields = dict(config.defaults())
    #print issuefields
    dictfields={}
    for ifield in issuefields:
        if ifield == "project":
            tempdict = {}
            tempdict[issuefields[ifield].split(':')[0]] = issuefields[ifield].split(':')[1]
            dictfields[ifield] = tempdict
        elif ifield == "issuetype":
            tempdict = {}
            tempdict[issuefields[ifield].split(':')[0]] = issuefields[ifield].split(':')[1]
            dictfields[ifield] = tempdict
        else:
            dictfields[ifield] = issuefields[ifield]
#    print "DICT : ", dictfields
    new_issue = jira.create_issue(dictfields)
    #new_issue = jira.create_issue(project={'key': 'CHANGE'},issuetype={'name': 'Production Change'},summary='Auto : Fourth ticket')
    
    print dir(new_issue)
    print "Key :", new_issue.key

    #new_issue = jira.create_issue(project={'key': 'CHANGE'},issuetype={'name': 'Production Change'},summary="Auto : Second ticket",)
    #new_issue = jira.create_issue(project={'key': 'CHANGE'},issuetype={'name': 'Production Change'},summary="Auto : first ticket",)
    #new_issue = jira.create_issue(issuefields)
    #new_issue = jira.create_issue(fields=issuefields)
    #print new_issue
def get_issuetype_id(metadata, project):
    print "*** PROJECT : %s ***" % project
    print "ID | Issue Type"
    count = 0
    metadata = create_metadata(project)
    #print metadata
    for issuetype in metadata['projects'][0]['issuetypes']:
        #print count," | ",issuetype['name']
        print "%s | %s" % (count, issuetype['name'])
        count += 1
    issuetypeid = int(raw_input("Choose IssueType by entering id :"))
    return issuetypeid

def create_template(project):
    metadata = create_metadata(project)
    issuetypeid = get_issuetype_id(metadata, project)
    template = cStringIO.StringIO()
    try:
        issuedata = metadata['projects'][0]['issuetypes'][issuetypeid]['fields']
        print issuedata
        for field in issuedata:
            if field == 'project':
                template.write('[project]\n')
                template.write('mandatory=True\n')
                fieldname = "%s=key:%s\n\n" % (field, issuedata[field]['allowedValues'][0]['key'])
                template.write(fieldname)
            elif field == 'issuetype':
                template.write('[issuetype]\n')
                template.write('mandatory=True\n')
                fieldname = "%s=name:%s\n\n" % (field, issuedata[field]['allowedValues'][0]['name'])
                template.write(fieldname)
            else:
                fieldname = "[%s]\n" % field
                template.write(fieldname)
                fieldname = "# Field : %s\n" % issuedata[field]['name']
                template.write(fieldname)
                # listing the possible values of the field
                if 'allowedValues' in issuedata[field].keys():
                    values = ""
                    for val in issuedata[field]['allowedValues']:
                        values += val['value']+","
                    value = "# values : %s\n" % values
                    template.write(value)
                # datatype of the field/custom field and jira UI type of custom field 
                datatypes = "datatype="+issuedata[field]['schema']['type']+"\n"
                template.write(datatypes)
                if 'custom' in issuedata[field]['schema'].keys():
                    customtype = issuedata[field]['schema']['custom']
                    customtype = customtype.split(':')
                    customtype = customtype[1]
                    datatypes = "jiratype=%s\n" % customtype
                    template.write(datatypes)
                # listing field mandatory status
                required = issuedata[field]['required']
                hashsymbol = "# "
                if required:
                    template.write('mandatory=True\n')
                    hashsymbol=""
                else:
                    template.write('mandatory=False\n')
                fieldname = "%s%s=\n" % (hashsymbol, field)
                template.write(fieldname)
                
                template.write("\n")
                
        print "#############################################"
        temp = template.getvalue()
        f = open('templates/CHANGE','w')
        f.write(temp)
        f.close()
    except Exception as e:
        print "ERROR : Please enter valid ID", e


def create_metadata(projectKeys, projectIds=None, issuetypeIds=None, issuetypeNames=None, expand='projects.issuetypes.fields'):
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
    '''
    Assigns the tickets to a user
    '''
    user = "selva"
    print "User : ", user,"Ticket : ", ticket
    jira = configure_jira()
    issue = jira.issue(ticket)
    jira.assign_issue(issue, user)
    jira.add_watcher(issue, user)
    
def add_comment(ticket):
    body = "I commented on ticket"
    jira = configure_jira()
    issue = jira.issue(ticket)
    jira.add_comment(issue, body)    
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
                        choices=['list','create','template','update','close','assign', 'comment'],
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
    parser.add_argument('-c', '--comment',
                        dest='comment',
                        help='Add a comment to ticket',
                        required=False,
                        type=str,
                        )
    args = vars(parser.parse_args())
    return args
 
