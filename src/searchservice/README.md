# Search Service

## Überblick

Der **Search Service** ist ein eigenständiger Microservice der Google Online Boutique (HipsterShop).  
Er stellt eine **Suchfunktion für Produkte** bereit, die über gRPC vom Frontend aufgerufen wird.

Der Service filtert Produkte anhand eines Suchstrings (Substring-Suche im Produktnamen) und liefert eine passende Produktliste zurück.  
Die Produktdaten werden **nicht selbst verwaltet**, sondern über den bestehenden `ProductCatalogService` bezogen.

---
## Projektstruktur
    searchservice/
    ├── proto/
    │   └── search.proto              # gRPC-Definition des SearchService
    ├── src/
    │   ├── main.py                   # Startet den gRPC-Server
    │   ├── product_cache.py          # Cache + ProductCatalog-gRPC-Client
    │   ├── search_pb2.py             # Generierter gRPC-Code
    │   ├── search_pb2_grpc.py
    │   ├── demo_pb2.py               # ProductCatalog Protos
    │   └── demo_pb2_grpc.py
    ├── tests/
    │   └── test.py                   # Unit-Tests (Mock des ProductCatalog)
    ├── Dockerfile
    ├── .dockerignore
    ├── requirements.in
    ├── requirements.txt
    └── README.md

---

## Architektur & Design

### Verantwortlichkeiten

- **Search Service**
  - gRPC-Server für Suchanfragen
  - Caching von Produktdaten
  - Filterlogik (Substring-Suche)
- **ProductCatalogService**
  - Quelle der Produktdaten
  - Wird per gRPC als externer Service genutzt

### Datenfluss

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
        rpc Search (SearchRequest) returns (SearchResponse);
    }

#### Messages

    message SearchRequest {
        string query = 1;
    }

    message SearchResponse {
        repeated Product products = 1;
    }

Das Product-Schema basiert auf dem bestehenden HipsterShop-Produktmodell.

### Caching-Strategie 

Der Service nutzt einen **In-Memory-Cache**, um unnötige Aufrufe des ProductCatalogService zu vermeiden.
- Produkte werden einmal geladen und zwischengespeichert
- Suchanfragen werden ausschließlich auf dem lokalen Cache ausgeführt

**Vorteile**:
- geringere Latenz
- Entlastung des ProductCatalogService
- bessere Skalierbarkeit

Der Cache ist bewusst einfach gehalten (kein LRU / keine Persistenz), da der Fokus auf Verständlichkeit und Korrektheit liegt.

### Tests

Es existieren Unit-Tests für die Kernlogik des Services.

Getestet wird unter anderem:
- korrekte Filterung nach Produktname
- Case-insensitive Suche
- Verhalten bei leerer Suche

Tests ausführen:

    pytest

### Abhängigkeiten


### Build & Run (Docker)

#### Docker Image bauen

    docker build -t searchservice .

#### Container starten

    docker run -p 8080:8080 searchservice

Der Service lauscht standardmäßig auf Port 8080.

### Qualitätsaspekte 

Der Service adressiert folgende Software-Qualtitäten:
- **Lose Kopplung** durch gRPC
- **Performance** durch Caching
- **Testbarkeit** durch Dependency Injection und Mocks

## Mögliche Erweiterungen

- Relevanzbewertung
- erweiterter Filter (Kategorien,Preis)