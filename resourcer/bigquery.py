# -*- coding: utf-8 -*-

"""
Module to connect to BigQuery
"""
import argparse

from googleapiclient import discovery
from googleapiclient.errors import HttpError
from oauth2client import tools
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage

class BigQuery:
    def __init__(self, scopes, client_secrets, storage_name, project_id):
        self.scopes = scopes
        self.client_secrets = client_secrets
        self.storage_name = storage_name
        self.project_id = project_id

    def __buildArgs(self, project_id):
        parser = argparse.ArgumentParser(description=__doc__,
                                         formatter_class=argparse.RawDescriptionHelpFormatter,
        # Use oauth2client's argparse as a base, so that the flags needed
        # for run_flow are available.
                                         parents=[tools.argparser])
        parser.add_argument('project_id',
                            help='Your Google Cloud Project ID.',
                            nargs='?',
                            default=project_id)
        return parser.parse_args()

    def refresh(self):
        storage = Storage(self.storage_name)
        credentials = storage.get()
        if credentials is None or credentials.invalid:
            flow = flow_from_clientsecrets(self.client_secrets, scope=self.scopes)
            # run_flow will prompt the user to authorize the application's
            # access to BigQuery and return the credentials.
            credentials = tools.run_flow(flow, storage, self.__buildArgs(self.project_id))
        # Create a BigQuery client using the credentials.
        return discovery.build('bigquery', 'v2', credentials=credentials)
