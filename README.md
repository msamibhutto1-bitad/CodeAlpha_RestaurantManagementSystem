# CodeAlpha Task 3: Restaurant Management System

A Django backend for running a restaurant: menu, orders, table reservations and inventory. Placing an order checks and deducts ingredients automatically, reservations can't double-book a table, and staff get low-stock alerts and daily sales reports.

## Features

- **Menu** with categories, prices and per-serving recipes (which inventory items a dish uses); `in_stock` flag computed live
- **Orders** with all-or-nothing processing: stock is checked and deducted in one transaction, totals use the price at order time, cancelling restocks
- **Order status flow:** `pending -> preparing -> served`, or `cancelled` (customers can cancel only while pending)
- **Tables and reservations:** availability check for a time slot and party size, overlap detection (90-minute slots by default), automatic assignment of the smallest fitting table
- **Inventory** management with restock and low-stock thresholds
- **Reports:** daily sales (revenue, orders, items sold) and low-stock alerts
- Token authentication, customer and staff roles, Django admin panel at `/admin/`
- pytest suite

## Project structure

```
CodeAlpha-Task-3/
├── main.py            # entry point (migrates, then runs the server)
├── config.py          # settings (env-overridable)
├── requirements.txt
├── pytest.ini
├── src/
│   ├── models.py      # menu, recipe, inventory, tables, reservations, orders
│   ├── services.py    # order processing, inventory update, table availability
│   ├── views.py       # JSON API
│   ├── api.py         # auth decorators, parsing, serializers
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
├── tests/test_api.py
└── screenshots/
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py                   # applies migrations and starts http://127.0.0.1:8000
python main.py createsuperuser   # staff account for the admin panel and staff endpoints
```

Staff accounts are the ones with `is_staff` set (superusers are). Customers sign up through the API.

## API

Authenticate with `Authorization: Token <key>` (returned by register/login).

| Method | Endpoint | Who | Description |
|--------|----------|-----|-------------|
| POST | `/api/auth/register/` `/login/` `/logout/` | - / - / user | Account and token |
| GET | `/api/menu/` | public | Menu (`?category=`, `?all=1` includes unavailable) |
| GET | `/api/menu/<id>/` | public | One dish |
| POST | `/api/menu/` | staff | Add dish with optional `recipe` |
| PATCH | `/api/menu/<id>/` | staff | Change price, availability, description, category |
| GET | `/api/tables/` | public | List tables |
| POST | `/api/tables/` | staff | Add table `{number, seats}` |
| GET | `/api/tables/available/?start_time=...&party_size=4` | public | Free tables for a slot |
| POST | `/api/reservations/` | user | Reserve `{start_time, party_size, table_id?}` |
| GET | `/api/reservations/` | user / staff | Own reservations (staff: all) |
| DELETE | `/api/reservations/<id>/` | owner / staff | Cancel |
| POST | `/api/orders/` | user | Place order `{items:[{menu_item_id, quantity}], table_id?}` |
| GET | `/api/orders/` `/api/orders/<id>/` | owner / staff | View orders |
| PATCH | `/api/orders/<id>/` | staff | Set status `{status}` |
| POST | `/api/orders/<id>/cancel/` | owner / staff | Cancel and restock |
| GET/POST | `/api/inventory/` | staff | List (`?low=1`) or add stock items |
| PATCH | `/api/inventory/<id>/` | staff | `{add: n}` to restock or `{quantity: n}` to set |
| GET | `/api/reports/daily-sales/?date=YYYY-MM-DD` | staff | Revenue and items sold (cancelled orders excluded) |
| GET | `/api/reports/low-stock/` | staff | Items at or below their threshold |

### Example

```bash
# Staff: add stock and a dish that uses it
curl -X POST localhost:8000/api/inventory/ -H "Authorization: Token $STAFF" \
  -H "Content-Type: application/json" -d '{"name":"Flour","unit":"kg","quantity":10,"low_stock_threshold":2}'
curl -X POST localhost:8000/api/menu/ -H "Authorization: Token $STAFF" \
  -H "Content-Type: application/json" \
  -d '{"name":"Pizza","price":"8.50","category":"main","recipe":[{"inventory_item_id":1,"quantity":0.5}]}'

# Customer: order two pizzas (deducts 1 kg flour)
curl -X POST localhost:8000/api/orders/ -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" -d '{"items":[{"menu_item_id":1,"quantity":2}]}'

# Customer: reserve a table for 4 (one is auto-assigned)
curl -X POST localhost:8000/api/reservations/ -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" -d '{"start_time":"2026-12-20T19:00:00Z","party_size":4}'
```

Errors return `{"error": "..."}` with 400 (invalid input), 401, 403, 404, 405, or 409 (not enough stock, table taken, wrong status change).

## Configuration

Environment variables: `SECRET_KEY`, `DATABASE`, `DEBUG`, `ALLOWED_HOSTS`, `HOST`, `PORT`, `TIME_ZONE`, `RESERVATION_MINUTES`. Set a real `SECRET_KEY` and `DEBUG=0` in production.

## Tests

```bash
pytest
```

## Screenshot

Add a screenshot (for example the admin panel or an API response) as `screenshots/project-preview.png`.

---
Built for the CodeAlpha Backend Development internship.
