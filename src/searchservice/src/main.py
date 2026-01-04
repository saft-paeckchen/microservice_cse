import grpc
from concurrent import futures

import search_pb2
import search_pb2_grpc
from product_cache import ProductCache


class SearchService(search_pb2_grpc.SearchServiceServicer):
    def __init__(self, product_cache):
        self.product_cache = product_cache

    def Search(self, request, context):
        query = request.query
        results = self.cache.search(query)

        return search_pb2.SearchResponse(results=results)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    port = os.environ.get('PORT', "8080")
    catalog_addr = os.environ.get('PRODUCT_CATALOG_SERVICE_ADDR', '')
    if catalog_addr == "":
        raise Exception('PRODUCT_CATALOG_SERVICE_ADDR environment variable not set')

    product_cache = ProductCache(catalog_addr = catalog_addr)
    search_service = SearchService(product_cache)

    search_pb2_grpc.add_SearchServiceServicer_to_server(search_service, server)

    server.add_insecure_port("[::]:"+port)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()