import time
from unittest.mock import MagicMock

from searchservice.src.product_cache import ProductCache
from searchservice.src.main import SearchService
import searchservice.src.demo_pb2 as demo_pb2

def make_product(pid, name):
    return demo_pb2.Product(
        id=pid,
        name=name,
        description="",
        picture="",
        price_usd=demo_pb2.Money(currency_code="USD", units=1, nanos=0),
        categories=[]
    )

# correct loading of products
def test_refresh_loads_from_catalog():
    cache = ProductCache("fake:1234")

    fake_products = [
        make_product("1", "Red Shirt"),
        make_product("2", "Blue Pants"),
    ]

    cache.stub = MagicMock()
    cache.stub.ListProducts.return_value = demo_pb2.ListProductsResponse(
        products=fake_products
    )

    cache.refresh()

    assert len(cache.products) == 2
    assert cache.products[0].name == "Red Shirt"

# search filter test
def test_search_filters_by_name():
    fake_stub = MagicMock()

    fake_stub.ListProducts.return_value = demo_pb2.ListProductsResponse(
        products=[
            make_product("1", "Red Shirt"),
            make_product("2", "Blue Pants"),
            make_product("3", "Red Hat"),
        ]
    )

    cache = ProductCache(stub=fake_stub)
    cache.refresh()

    results = cache.search("red")
    names = [p.name for p in results]

    assert "Red Shirt" in names
    assert "Red Hat" in names
    assert "Blue Pants" not in names


# case-intsensitiv search
def test_search_is_case_insensitive():
    fake_stub = MagicMock()

    fake_stub.ListProducts.return_value = demo_pb2.ListProductsResponse(
        products=[
            make_product("1", "Red Shirt"),
        ]
    )

    cache = ProductCache(stub=fake_stub)
    results = cache.search("RED")
    assert len(results) == 1

# empty search
def test_empty_query_returns_all_products():
    fake_stub = MagicMock()

    fake_stub.ListProducts.return_value = demo_pb2.ListProductsResponse(
        products=[
            make_product("1", "Red Shirt"),
            make_product("2", "Blue Pants"),
        ]
    )

    cache = ProductCache(stub=fake_stub)

    results = cache.search("")
    assert len(results) == 2

# correct cache
def test_catalog_called_only_once_when_cached():
    cache = ProductCache("fake")

    fake_products = [make_product("1", "Red Shirt")]

    cache.stub = MagicMock()
    cache.stub.ListProducts.return_value = demo_pb2.ListProductsResponse(
        products=fake_products
    )

    cache.refresh()
    cache.refresh()

    assert cache.stub.ListProducts.call_count == 1
