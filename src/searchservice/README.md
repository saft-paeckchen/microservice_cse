# Search Service

## Overview

The **Search Service** is an independant microservice of the Google Online Boutique (HipsterShop).  
It enables a **search function for products**, that is called via gRPC from the frontend.

Products are filtered by looking at the search query and returning every product that includes the query as a substring.  
Furthermore, the product data is **not managed seperately**, but uses the existing `ProductCatalogService`.

---
## Project Structure
    searchservice/
    ├── proto/
    │   └── search.proto              # gRPC-definition of the SearchService (legacy)
    ├── src/
    │   ├── main.py                   # Starts the grpc server
    │   ├── product_cache.py          # Cache + ProductCatalog-gRPC-Client
    │   ├── demo_pb2.py               # ProductCatalog Protos
    │   └── demo_pb2_grpc.py
    ├── tests/
    │   └── test.py                   # Unit-Tests (ProductCatalog mock)
    ├── Dockerfile
    ├── genproto.sh                   # generating the pb files
    ├── .dockerignore
    ├── requirements.in
    ├── requirements.txt
    └── README.md

---

## Architecture & Design

### Responsibilities

- **Search Service**
  - gRPC-Server for search queries
  - Caching of product data
  - Filter logic (substring-search)
- **ProductCatalogService**
  - Source of product data
  - Is used via gRPC externally
- **Frontend**
  - Receives and handles HTTP requests from UI
  - Sends search query to SearchService
  - Reloads proper HTML page

### Dataflow

    HTML Page
    |
    | HTTP query
    v
    Frontend
    |
    | gRPC Search(query)
    v
    SearchService
    |
    | gRPC ListProducts()
    v
    ProductCatalogService


### gRPC APi

#### Service

    service SearchService {
      rpc SearchedProducts (SearchedRequest) returns (SearchedResponse) {}
    }

#### Messages

    message SearchedRequest {
      string query = 1;
    }
    
    message SearchedResponse {
      repeated Product products = 1;
    }

The product-scheme is based of of the existing HipsterShop product model.

### Caching Strategie 

The service utilises an **in-memory-cache**, to circumvent unnecessary calls to the ProductCatalogService.
- products are loaded once and saved for later calls
- search requests will only be handled on the local cache

**Advantages**:
- lower latency
- relieving the ProductCatalogService
- better scalability

The cache is kept simple on purpose (no LRU / no persistence), to keep the focus on comprehensibility and correctness.

### Tests

There are unit-tests for the main logic of the service.

The tests are covering:
- correct filtering of products
- case-insensitive search
- behaviour of empty searches

Run tests via:

    pytest

### Dependencies


### Build & Run (Docker)

#### building the Docker Image

    docker build -t searchservice .

#### starting the Container

    docker run -p 9090:9090 searchservice

The service is typically bound to port 9090.

### Quality aspect 

The following software qualities are addressed by this service:
- **Loose coupling** via gRPC
- **Performance** via Caching
- **Testibility** via Dependency Injection and Mocks

## Possible Extensions

- filter by relevancy
- expanded filter (categories, price)
