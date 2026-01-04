import grpc
import time
from typing import List

import demo_pb2
import demo_pb2_grpc


class ProductCache:
    def __init__(self, catalog_addr: str = None,stub = False):
        if stub:
            self.stub = stub
        else:
            channel = grpc.insecure_channel(catalog_addr)
            self.stub = demo_pb2_grpc.ProductCatalogServiceStub(channel)
        self.products = []
        self.last_update = 0

    def refresh(self):
        if time.time() - self.last_update < 120:
            return
        
        response = self.stub.ListProducts(demo_pb2.Empty())
        self.products = response.products
        self.last_update = time.time()

    def search(self, query: str):
        self.refresh()

        q = query.lower()
        return [p for p in self.products
                    if q in p.name.lower()
        ]

