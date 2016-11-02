# -*- coding: utf-8 -*-

"""
Module to interface with source{d} BigQuery database
"""
import os

from googleapiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError
from bigquery import BigQuery
from queries import *

SCOPES = ['https://www.googleapis.com/auth/bigquery']
CLIENT_SECRETS = os.getcwd() + '/share/CLIENTSECRET.json'
STORAGE_NAME = os.path.expanduser('~') +'/.resourcer-credentials.dat'
PROJECT_ID = 'srcd-playground'

class SrcdPlayground:    
    def __init__(self):
        self.bq = BigQuery(SCOPES, CLIENT_SECRETS, STORAGE_NAME, PROJECT_ID).refresh()
        self.lastQuery = ''
        
    def __getQueryObject(self, query):
        """
        Executes a query in Source{d} database

        Args:
            query: A string with the query to execute

        Returns:
            Returns a query response object
        """
        try:
            query_request = self.bq.jobs()
            query_data = {'query': (query)}
            query_response = query_request.query(projectId=PROJECT_ID,
                                                 body=query_data).execute()
            return query_response

        except HttpError as err:
            print('Error in listDatasets:')
            pprint.pprint(err.content)

        except AccessTokenRefreshError:
            print('Credentials have been revoked or expired, please re-run'
                  'the application to re-authorize')

    def __getQueryData(self, query, fieldNames):
        """
        Executes a query and returns the normalized data structure easy to read

        Args:
            query: A string with the query to execute
            fieldNames: A list with the names of the columns

        Returns:
            A list of dictionaries. Each dictionary represents a row. The structure
            of the ditionaries is the following:

            {'nameColum0': data, 'nameColumn1': data, ..., 'nameColumnN': data}
        """
        results =  self.__getQueryObject(query)
        # print results
        data = []
        if results['totalRows'] != '0':
            for row in results['rows']:
                rowData = {}
                for name, field in zip(fieldNames, row['f']):
                    rowData[name] = field['v']
                data.append(rowData)
        return data

    def __getColumnData(self, query, column):
        """
        Executes a query that return a table with 1 column

        Args:
            query: A string with the query to execute
            column: A string with the name of the column

        Returns:
            A list with the data of the column in the table
        """
        raw = self.__getQueryData(query, [column])
        cleaned = []
        for item in raw:
            if item[column] != '':
                cleaned.append(item)
                
        return cleaned

    def getCountries(self):
        """
        Returns a list with the countries from the database
        """
        return self.__getColumnData(Q_COUNTRIES, 'country')
    
    def getLanguages(self):
        """
        Returns a list with the languages from the database
        """
        return self.__getColumnData(Q_LANGUAGES, 'language')

    def getEcosystems(self):
        """
        Returns a list with the ecosystems from the database
        """
        return self.__getColumnData(Q_ECOSYSTEMS, 'ecosystem')

    def getQuery(self, langs, ecos, countries, report, ANDlangs, ANDecos):
        """
        Search for candiates according to some parameters

        Args:
            langs: A list of languages. Each element in the list is a list with this
                   structure: [string, boolean]. string is a language and boolean points
                   if the language is relevant(True) or not(False)
            ecos: A list of strings representing the ecosystems
            countries: A list of strings representing the countries
            report: A boolean that points if we need candidates with report(True) or 
                    not(False)
            ANDlangs: A boolean that points if it will apply a AND with the list of
                      languages(True) or not(False)
            ANDecos: A boolean that points if it will apply a AND with the list of
                      ecosystems(True) or not(False)

        Returns:
            A list of dictionaries. Each dictionary represents a row. The structure
            of the ditionaries is the following:

            {'nameColum0': data, 'nameColumn1': data, ..., 'nameColumnN': data}
        """
        # This refresh the connection with BigQuery every time we search something
        # Probably there is a better way to deal with expiered connections
        self.bq = BigQuery(SCOPES, CLIENT_SECRETS, STORAGE_NAME, PROJECT_ID).refresh()
        self.lastQuery = createQuery(langs, ecos, countries, report, ANDlangs, ANDecos)
        # print the last query for debug options
        # print(self.lastQuery)
        return self.__getQueryData(self.lastQuery,
                                   ['email', 'country', 'report', 'PageRank', 'hs'])

    def getLastQuery(self):
        """
        Returns a string with the last query that was executed
        """
        return self.lastQuery
    
