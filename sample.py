#!/usr/bin/env python
# sample module 
from jira.client import JIRA

def main():
    jira = JIRA()
    JIRA(options={'server': 'http://localhost:8100'})
    projects = jira.projects()
    print projects
    for project in projects:
        print project.key

# Standard boilerplate to call the main() function. 
if __name__ == '__main__':
    main()