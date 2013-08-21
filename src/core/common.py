#!/usr/bin/env python
"""
autojira is python tool to interact with JIRA
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

from jira.client import JIRA
import cStringIO
import ConfigParser
import helper
import sys
import logging

""" Collection of functions to work with JIRA tickets
 gettext internationalisation function requisite:
"""
jira = JIRA()
def create_issue(filename):
    jira = helper.configure_jira()
    issueFields = {}
    #print "Creating issue"
    logging.info('*** Create Issue Initiated ***')
    logging.debug('Create Issue template is %s ', filename)
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.read(filename)
    for section in config.sections():
        logging.debug("*** Processing Field %s ***" % section)
        if config.has_option(section, section):
            #print config.get(section, section)
            options = helper.create_section_dict(config.items(section))
            if options[section]:
                value = helper.format_element(section, options)
                issueFields[section] = value
            elif options['mandatory'] == 'True':
                errorMsg = "%s mandatory field is empty, check %s" % (section, filename)
                try:
                    raise CustomException(errorMsg)
                except CustomException, e:
                    logging.error(e)
                    sys.exit(1)
        else:
            mandatory = config.get(section, 'mandatory')
            if mandatory == 'True':
                errorMsg = "%s mandatory field is not defined, check %s" % (section, filename)
                try:
                    raise CustomException(errorMsg)
                except CustomException, e:
                    logging.error(e)
                    sys.exit(1)
    logging.debug('create issue fields dictionary %s' % issueFields)
    new_issue = jira.create_issue(issueFields)
    print repr(new_issue)
    logging.info('*** Create Issue Completed ***')

def create_template(project):
    logging.info('*** Create Issue Template Initiated ***')
    metadata = helper.create_metadata(project)
    issuetypeid = helper.get_issuetype_id(metadata, project)
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
                    children=False
                    if 'custom' in issuedata[field]['schema'].keys():
                        customtype = issuedata[field]['schema']['custom']
                        if 'cascadingselect' in customtype:
                            children = True
                    for val in issuedata[field]['allowedValues']:
                        if children is True:
                            allchild=""
                            for child in val['children']:
                                allchild +=child['value']+","
                                #print child
                            print "All :"+allchild
                            values += "Parent:Children-"+val['value']+":"+allchild+" | "
                        else:
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
                
        #print "#############################################"
        temp = template.getvalue()
        f = open('templates/CHANGE','w')
        f.write(temp)
        f.close()
    except Exception as e:
        logging.error(e)
    logging.info('*** Create Issue Template Completed ***')



def list_projects():
    logging.info('*** List the Projects Initiated ***')
    jira = helper.configure_jira()
    projects = jira.projects()
    logging.info('*** List the Projects Completed ***')
    return projects

def assgin_issue(ticket):
    '''
    Assigns the tickets to a user
    '''
    logging.info('*** Assign the ticket Initiated ***')
    config = helper.get_global_config()
    user = config.get('jira','user')
    logging.info('User :%s and Ticket %s ' % (user, ticket))
    print "User : ", user,"Ticket : ", ticket
    jira = helper.configure_jira()
    try :
        issue = jira.issue(ticket)
        jira.assign_issue(issue, user)
        jira.add_watcher(issue, user)
        logging.info('*** Watcher Enabled ***')
    except Exception, e:
        logging.error(e)
    logging.info('*** Assign the ticket Completed ***')
    
def add_comment(ticket, comment):
    logging.info('*** Comment on ticket Initiated ***')
    if comment:
        body = comment
        jira = helper.configure_jira()
        try :
            user = helper.get_global_config().get('jira','user')
            issue = jira.issue(ticket)
            jira.add_comment(issue, body)
            jira.add_watcher(issue, user)
            logging.info('*** Watcher Enabled ***')
        except Exception, e:
            logging.error(e)
    else:
        logging.error('comment value is expected')
        sys.exit(1)    
    logging.info('*** Comment on ticket Completed ***')
def add_watcher(ticket, user):
    logging.info('*** Enable watcher Initiated ***')
    if not user:
        user = helper.get_global_config().get('jira','user')
    jira = helper.configure_jira()
    try :
        issue = jira.issue(ticket)
        jira.add_watcher(issue, user)
    except Exception, e:
        logging.error(e)
    logging.info('*** Enable watcher Completed ***')
    
def process_args():
    logging.info('*** Parse the logs Initiated ***')
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
    logging.info("*** Argument parsing completed ***")
    return args
 
class CustomException(Exception):
    pass