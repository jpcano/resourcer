# -*- coding: utf-8 -*-

"""
Module to interface with source{d} REST API
"""
import json
import urllib2
import operator

REST_URL = "https://SOURCEDRESTURL"
GITHUB_URL = "https://github.com/"

class SrcdRest:
    def __init__(self):
        self.email = None
        self.person = None

    def getGithub(self, email):
        return self.__getProfile(email, 'github')

    def getLinkedin(self, email):
        return self.__getProfile(email, 'linkedin')

    def getFullName(self, email):
        self.__cachePerson(email)
        if self.person['Personal'] == None or self.person['Personal']['DefaultFullName'] == None:
            return ''
        return self.person['Personal']['DefaultFullName']
        
    def __getProfile(self, email, profile):
        self.__cachePerson(email)
        if self.person['Profiles'] == None or profile not in self.person['Profiles']:
            if (profile == 'github'):
                return self.__guestGithubProfile(self.person)
            return ''
        return self.person['Profiles'][profile]['URL']

    def __cachePerson(self, email):
        if email != self.email:
            self.email = email
            self.person = self.__retrievePerson(email)
            
    def __retrievePerson(self, email):
        parsed_entity = json.load(urllib2.urlopen(REST_URL + email))
        person = parsed_entity['_embedded']['person']
        if len(person) == 0:
            raise ValueError('The entity with email=%s does not exist in srcd database' % (email))
        else:
            return person[0]
    
    def __guestGithubProfile(self, person):
        counts = {}
        for index  in person['Contributions']:
            username = self.__getUserFromGithubURL(index['URL'])
            if username not in counts:
                counts[username] = 0
            else:
                counts[username] += 1
        sorted_names = sorted(counts.items(), key=operator.itemgetter(1))
        return GITHUB_URL + sorted_names[-1][0]

    def __getUserFromGithubURL(self, url):
        # "URL": "http:\/\/githubn .com\/jpcano"
        parts = url.split('/')
        return parts[3]

