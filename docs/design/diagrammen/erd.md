# ERD PixelDepot WMS

Eerste versie, week 1 · Kien (review: Daniel)

Gebaseerd op het hoofdstuk *Datamodel en voorraadregels* uit het projectplan. Elke tabel heeft een automatische `id` als primaire sleutel (PK). `FK` is een verwijzing naar een andere tabel, `UK` een unieke waarde.

```mermaid
erDiagram
    GROUP }o--o{ USER : "rol (Medewerker of Admin)"
    USER ||--o{ ORDER : "plaatst"
    USER ||--o{ STOCK_MOVEMENT : "voert uit"
    CUSTOMER ||--o{ ORDER : "bestelt"
    ORDER ||--|{ ORDER_LINE : "bevat"
    PRODUCT ||--o{ ORDER_LINE : "staat in"
    PRODUCT ||--o{ STOCK : "ligt op"
    LOCATION ||--o{ STOCK : "bevat"
    ORDER_LINE ||--o{ STOCK_ALLOCATION : "wordt geleverd door"
    STOCK ||--o{ STOCK_ALLOCATION : "levert"
    PRODUCT ||--o{ STOCK_MOVEMENT : "betreft"
    LOCATION |o--o{ STOCK_MOVEMENT : "van vak"
    LOCATION |o--o{ STOCK_MOVEMENT : "naar vak"

    GROUP {
        int id PK
        string name UK "Medewerker of Admin"
    }
    USER {
        int id PK
        string username UK
        string password "gehasht door Django"
        bool is_active
    }
    CUSTOMER {
        int id PK
        string type "consumer of business"
        string name
        string email
        string phone
        string address
        decimal credit_limit "alleen zichtbaar voor Admin"
    }
    PRODUCT {
        int id PK
        string sku UK
        string name
        string category
        text description
        string compatibility
        decimal price
        bool is_active
        int min_stock "drempel voor melding lage voorraad"
    }
    LOCATION {
        int id PK
        string code UK "bijv. A-01"
        string description
    }
    STOCK {
        int id PK
        int product_id FK
        int location_id FK
        int on_hand "fysiek aantal"
        int reserved "0 <= reserved <= on_hand"
    }
    ORDER {
        int id PK
        string order_number UK
        int customer_id FK
        int created_by_id FK "medewerker"
        string status "new, processing, shipped, cancelled"
        datetime created_at
        datetime updated_at
    }
    ORDER_LINE {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
        decimal unit_price "prijs op moment van bestellen"
    }
    STOCK_ALLOCATION {
        int id PK
        int order_line_id FK
        int stock_id FK
        int quantity "aantal uit dit vak"
    }
    STOCK_MOVEMENT {
        int id PK
        string type "receive, write_off, transfer"
        int product_id FK
        int from_location_id FK "leeg bij receive"
        int to_location_id FK "leeg bij write_off"
        int quantity
        string reason "verplicht bij write_off"
        string delivery_reference "bij receive"
        int performed_by_id FK
        datetime created_at
    }
```

## Unieke combinaties en constraints

| Tabel | Regel | Waarom |
| --- | --- | --- |
| Product | `sku` uniek | Een dubbele SKU geeft een duidelijke fout (US-04) |
| Location | `code` uniek | Elk vak bestaat één keer |
| Stock | (`product`, `location`) uniek | Eén voorraadrij per product per vak |
| Stock | `0 ≤ reserved ≤ on_hand` | Nooit meer reserveren dan er fysiek ligt |
| Order | `order_number` uniek | Zoeken op ordernummer (US-06) |
| OrderLine | (`order`, `product`) uniek | Eén orderregel per product |
| StockAllocation | (`order_line`, `stock`) uniek | Eén toewijzing per orderregel en vak |

## Keuzes

- **Beschikbaar** is geen kolom: `on_hand − reserved` wordt berekend, zodat het nooit uit de pas loopt.
- **Rol** loopt via Django-groepen in plaats van een eigen kolom, zodat Django's rechtensysteem meteen werkt.
- **Orders** hebben geen verwijderactie; annuleren zet `status` op `cancelled`.
- **Geld** (`price`, `unit_price`, `credit_limit`) is decimaal. Een orderregel bewaart zijn eigen prijs, zodat een prijswijziging oude orders niet verandert.
- **StockMovement** heeft twee optionele vakken: `receive` vult alleen `to`, `write_off` alleen `from`, `transfer` allebei.
