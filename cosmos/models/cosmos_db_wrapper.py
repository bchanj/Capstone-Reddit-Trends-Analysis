#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "models"))


import os
import base64
import json
import dotenv
from azure.cosmos import CosmosClient
from bundle import Bundle
from query_filter import QueryFilter
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

    def _createContainer(self) -> None:
        try:
            self._container = self._database.create_container(id=container_name, partition_key=PartitionKey(path="/productName"))
        except exceptions.CosmosResourceExistsError:
            self._container = self._database.get_container_client(container_name)
        except exceptions.CosmosHttpResponseError:
            raise

    def createEntries(self, bundles: List[Bundle]) -> None:
        for bundle in bundles:
            # print(bundle.__dict__)
            self._container.upsert_item(bundle.__dict__)

    def readEntries(self, filters: List[QueryFilter]=None, start: int=0, limit:int=10):
        clauses = ""
        whereClause = ""
        if filters is not None:
            clauses = " AND ".join([f'RegexMatch(c.{f.key}, "{f.value}")' for f in filters])
            whereClause = f"WHERE {clauses}"
        result = []
        for item in self._container.query_items(
        query=f'''
            SELECT * 
            FROM c IN Items.items 
            {whereClause}
            OFFSET {start} LIMIT {limit}''',
        enable_cross_partition_query=True):
            result.append(item)
        return result


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    wrapper = CosmosClientWrapper()