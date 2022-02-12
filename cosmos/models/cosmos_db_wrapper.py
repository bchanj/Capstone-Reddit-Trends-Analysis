import sys
import path
# directory reach
directory = path.path(__file__).abspath()
# setting path
sys.path.append(directory.parent.parent)

import os
import base64
import json
import dotenv
from azure.cosmos import CosmosClient
from deal import Bundle
from typing import List

class CosmosClientWrapper():
    def __init__(self):
        self._internalClient = CosmosClient(
            "https://cs2215newtest.documents.azure.com:443/",
            "o2rmrQEOk9rAqBCVmh4nxpzwRfJQ2y5Ayr2g8q7GTEcRhPuBudjgIrBRgIjrvKOimrO0066nBmb9oSXsrYIfew==",
        )
        database_name = 'ToDoList'
        self._database = self._internalClient.get_database_client(database_name)
        container_name = 'Items'
        self._container = self._database.get_container_client(container_name)

    def _createContainer(self):
        try:
            self._container = self._database.create_container(id=container_name, partition_key=PartitionKey(path="/productName"))
        except exceptions.CosmosResourceExistsError:
            self._container = self._database.get_container_client(container_name)
        except exceptions.CosmosHttpResponseError:
            raise
        pass

    def createEntries(self, deals):
        pass

    def readEntries(self, filters: List[QueryFilter]=None):
        result = []
        for item in self._container.query_items(
        query='SELECT * FROM c IN Items.items WHERE RegexMatch(c.Game, "[F|f][R|r][E|e][E|e]")',
        enable_cross_partition_query=True):
            result.append(item)
        return result


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    wrapper = CosmosClientWrapper()
    res = wrapper.readEntries()
    for r in res:
        print(r)