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
    print new_issue

    #new_issue = jira.create_issue(project={'key': 'CHANGE'},issuetype={'name': 'Production Change'},summary="Auto : Second ticket",)
    #new_issue = jira.create_issue(project={'key': 'CHANGE'},issuetype={'name': 'Production Change'},summary="Auto : first ticket",)
    #new_issue = jira.create_issue(issuefields)
    #new_issue = jira.create_issue(fields=issuefields)
    #print new_issue


def create_template(project):
    metadata = create_metadata(project)
    print metadata
    print "##########"
    print "ID | Issue Type"
    count = 0
    for issuetype in metadata['projects'][0]['issuetypes']:
        print count," | ",issuetype['name']
        count += 1
    issuetypeid = int(raw_input("Choose Issue type by entering id :"))
    #print issuetypeid, ":", issuetypes[issuetypeid]
    template = cStringIO.StringIO()
    try:
        template.write('[DEFAULT]\n\n')
        
        issuedata = metadata['projects'][0]['issuetypes'][issuetypeid]['fields']
        for field in issuedata:
            if field == 'project':
                template.write('# mandatory field\n')
                #fieldname = issuedata[field]['name']+"={'name': '"+issuedata[field]['allowedValues'][0]['name']+"'}\n\n"
                fieldname = field+"=key:"+issuedata[field]['allowedValues'][0]['key']+"\n\n"
                template.write(fieldname)
            elif field == 'issuetype':
                template.write('# mandatory field\n')
                #fieldname = issuedata[field]['name']+"='name': '"+issuedata[field]['allowedValues'][0]['name']+"'}\n\n"
                fieldname = field+"=name:"+issuedata[field]['allowedValues'][0]['name']+"\n\n"
                template.write(fieldname)
            else:
                required = issuedata[field]['required']
                if required:
                    template.write('# mandatory field\n')
                if 'allowedValues' in issuedata[field].keys():
                    values = ""
                    for val in issuedata[field]['allowedValues']:
                        values += val['value']+","
                    value = "# values : "+values+"\n"
                    template.write(value)
                customtype = ""
                if 'custom' in issuedata[field]['schema'].keys():
                    customtype = issuedata[field]['schema']['custom']
                    customtype = customtype.split(':')
                    customtype = customtype[1]
                    datatypes = "# data type : "+issuedata[field]['schema']['type']+", UI type : "+customtype+"\n"
                    template.write(datatypes)
                else:
                    datatypes = "# data type : "+issuedata[field]['schema']['type']+"\n"
                    template.write(datatypes)
                #fieldname = "# "+issuedata[field]['name']+"="+"\n\n"
                fieldname = "# "+field+"="+"\n\n"
                template.write(fieldname)
                
        print "#############################################"
        temp = template.getvalue()
        f = open('conf/CHANGE','w')
        f.write(temp)
        f.close()
                #print field+"="+"\n"
            #print type(field)
            #print issuedata[field]
#             if 'allowedValues' in issuedata[field].keys():
#                 print field,"=",issuedata[field]['allowedValues'][0]['name']
#             else:
#                 print field
                
    except Exception as e:
        print "ERROR : Please enter valid ID", e
#     for meta in metadata:
#         print meta.key
    """issue_dict = {'key' : 'DEV',
                 'summary' : 'Creating Issue from Code',
                                  
                 
                 }
    jira.create_issue(fields=issue_dict,)"""
    

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
 
