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
    ├── demo_video.mkv                # Video showing the functionality and use cases of this service
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

### Caching Strategy

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

- Linux or wsl
- kubectl
- skaffold
- docker
- (git, to download the repository only)
- (gcloud, runs properly without it but there are some warnings)

### Build & Run SearchService (Docker)

#### building the Docker Image

    docker build -t searchservice .

#### starting the Container

    docker run -p 9090:9090 searchservice

The service is typically bound to port 9090.

### Build & Run Demo (local)

Start a minikube local server that emulates a similiar environment to gcloud.

    minikube start --driver=docker --cpus=4 --memory=4096

From the root of the repository run:

    skaffold dev

This should deploy all microservices and therefore the demo.

There are several ways to access the demo from here. One is to direct all traffic to some port like 8080 via kubectl:

    kubectl port-forward svc/frontend 8080:80

This way you can open the demo via most browsers with the URL:

    localhost:8080/

### Quality aspect 

The following software qualities are addressed by this service:
- **Loose coupling** via gRPC
- **Performance** via Caching
- **Testibility** via Dependency Injection and Mocks

## Possible Extensions

- filter by relevancy
- expanded filter (categories, price)


# Development Approach

## Responsibilities

Early on we had a meeting to discuss the development process and gave out roles that loosely represent our responsibilities. Loosely because the project is rather small and everyone needs to contribute code and just because someone is responsible for a task, doesn't mean no one else in the group can help them with it.
Philip was responsible for the Frontend development. Specifically the search bar that is visible in the UI and the corresponding HTTP POST that is send when searching.
Julien managed the Backend, meaning the filter, gRPC call to the ProductCatalog, and the caching.
Steven was supposed to manage the whole project, keep everyone accountable for the set deadlines and overlook the codebase, which allowed for a smoother merge of Frontend and Backend.
As said previously everyone was still aware of the whole codebase and checking or fixing bugs if found anywhere. Since we are only a small team, this decision was rather helpful and not really resulting in any chaos, in retrospect. 

## Kanban

We decided to use Kanban, specifically the board provided by GitHub. In the first meeting we discussed what Issues are necessary and added them to the Backlog. With the Kanban board it was very easy to overlook what has been done, what is in development and what tasks are still open. No one in the group was overwhelmed or had taken on too many issues because of this. 

## Technology Descisions

Most of the relevant descicions have already been discussed previously in this README regarding our microservice. To summarize...

## Demo Scenario

Imagine a big online shop. One that has more than just 9 products (which realistically is most online shops). Looking through all of the products for a customer is tedious and they might overlook an item that they would otherwise be willing to buy. Imagine yourself entering this huge shop. Even when all the items are put into categories (which is difficult on its own), it is just way easier and quicker to search exactly what you need. The autofill function makes it even easier, in case you don't exactly know the name of the thing you are looking for. With just one click of a button you can see a smaller list of items that could fit your needs.

