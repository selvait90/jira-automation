#!/usr/bin/env python

"""
supports functions of common.py
"""

from jira.client import JIRA

import ConfigParser
import logging

def format_element(section, options):
    logging.debug('Constructing the field %s and it value %s')
    if 'project' in options.keys():
        valuedict = {}
        value = options[section]
        valuedict[value.split(':')[0]] = value.split(':')[1]
        logging.debug('Constructed field value - %s : %s' % (section, valuedict))
        return valuedict
    elif 'issuetype' in options.keys():
        valuedict = {}
        value = options[section]
        valuedict[value.split(':')[0]] = value.split(':')[1]
        logging.debug('Constructed field value - %s : %s' % (section, valuedict))
        return valuedict
    else:
        valuedict = {}
        if 'jiratype' in options.keys():
            if options['jiratype'] == 'radiobuttons':
                key = 'value'
                value = options[section]
                valuedict[key]=value
                logging.debug('Constructed field value - %s : %s' % (section, valuedict))
                return valuedict
            elif options['jiratype'] == 'multicheckboxes':
                valuearray = []
                key = 'value'
                value = options[section].split(',')
                for val in value:
                    valuedict[key] = val
                    valuearray.append(valuedict)
                    valuedict = {}
                logging.debug('Constructed field value - %s : %s' % (section, valuedict))
                return valuearray
            elif options['jiratype'] == 'select':
                key = 'value'
                value = options[section]
                valuedict[key]=value
                logging.debug('Constructed field value - %s : %s' % (section, valuedict))
                return valuedict
            elif options['jiratype'] == 'cascadingselect':
                key = 'value'
                childdict = {}
                (parent, child) = options[section].split(':')
                childdict[key] = child
                valuedict[key] = parent
                valuedict['child'] = childdict
                logging.debug('Constructed field value - %s : %s' % (section, valuedict))
                return valuedict
            elif options['jiratype'] == 'datetime':
                (date, time) = options[section].split()
                value = date+"T"+time+".0-0500"
                logging.debug('Constructed field value - %s : %s' % (section, valuedict))
                return value
            else:
                logging.debug('Constructed field value - %s : %s' % (section, valuedict))
                return options[section]
        else:
            logging.debug('Constructed field value - %s : %s' % (section, valuedict))               
            return options[section] 
        
def create_section_dict(items):
    '''
    Load options of a section into dictionary
    '''
    options = {}
    for pair in items:
        options[pair[0]] = pair[1]
        logging.debug(" constructing dict of config sections : %s" % options)
    return options
        
def create_issue_old(filename):
    jira = configure_jira()
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
    
    print repr(new_issue)
    print "Key :", new_issue.key

    #new_issue = jira.create_issue(project={'key': 'CHANGE'},issuetype={'name': 'Production Change'},summary="Auto : Second ticket",)
    #new_issue = jira.create_issue(project={'key': 'CHANGE'},issuetype={'name': 'Production Change'},summary="Auto : first ticket",)
    #new_issue = jira.create_issue(issuefields)
    #new_issue = jira.create_issue(fields=issuefields)
    #print new_issue
def get_issuetype_id(metadata, project):
    print "*** PROJECT : %s ***" % project
    logging.debug("*** PROJECT : %s ***" % project)
    print "ID | Issue Type"
    logging.debug("ID | Issue Type")
    count = 0
    metadata = create_metadata(project)
    #print metadata
    for issuetype in metadata['projects'][0]['issuetypes']:
        #print count," | ",issuetype['name']
        print "%s | %s" % (count, issuetype['name'])
        count += 1
    issuetypeid = int(raw_input("Choose IssueType by entering id :"))
    return issuetypeid

def create_metadata(projectKeys, projectIds=None, issuetypeIds=None, issuetypeNames=None, expand='projects.issuetypes.fields'):
    jira = configure_jira()
    metadata = jira.createmeta(projectKeys, projectIds, issuetypeIds, issuetypeNames, expand)
    return metadata

def configure_jira():
    config = get_global_config()
    server = config.get('jira', 'server')
    user = config.get('jira', 'user')
    passwd = config.get('jira', 'passwd')
    #server = 'http://localhost:8100'
    #jira = JIRA(options={'sever' : sever}, basic_auth=None, oauth=None)
    jira = JIRA(options={'server': server}, basic_auth=(user, passwd), oauth=None)
    return jira
def get_global_config():
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.read('templates/global')
    return config