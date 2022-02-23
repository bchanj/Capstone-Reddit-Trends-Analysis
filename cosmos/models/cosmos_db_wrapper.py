#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "models"))


import os
import base64
import json
import dotenv 
from azure.cosmos import CosmosClient
from deal import Deal
from query_filter import QueryFilter
from typing import List

class CosmosClientWrapper():
    def __init__(self):
        self._internalClient = self._clientCreateInstance()
        self.database_name = 'Deals'
        self._database = self._internalClient.get_database_client(self.database_name)
        self.container_name = 'gameDeals'
        self._container = self._database.get_container_client(self.container_name)

    def _clientCreateInstance(self):
        dotenv.load_dotenv()
        encrypted_creds: str = os.environ["COSMOS_CREDS"]
        decoded: bytes = base64.b64decode(encrypted_creds)
        json_dict = json.loads(decoded)
        return CosmosClient(
            json_dict["uri"],
            json_dict["PRIMARY_KEY"]
        )

    def _createContainer(self) -> None:
        try:
            self._container = self._database.create_container(id=container_name, partition_key=PartitionKey(path="/productName"))
        except exceptions.CosmosResourceExistsError:
            self._container = self._database.get_container_client(container_name)
        except exceptions.CosmosHttpResponseError:
            raise

    def createEntries(self, deals: List[Deal]) -> None:
        for deal in deals:
            # print(deal.__dict__)
            self._container.upsert_item(deal.__dict__)

    def readEntries(self, filters: List[QueryFilter]=None, start: int=0, limit:int=10) -> List[Deal]:
        clauses = ""
        whereClause = ""
        if filters is not None:
            clauses = " AND ".join([f'CONTAINS(c.{f.key}, "{f.value}")' for f in filters])
            whereClause = f"WHERE {clauses}"
        result = []
        q = f'''
            SELECT * 
            FROM c
            {whereClause}
            OFFSET {start} LIMIT {limit}'''
        for item in self._container.query_items(
        query=q,
        enable_cross_partition_query=True):
            excluding_private = {x: item[x] for x in item if not x.startswith("_")}
            result.append(Deal(**excluding_private))
        return result


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    wrapper = CosmosClientWrapper()