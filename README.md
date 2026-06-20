# Auto API

Auto API is a Django REST Framework backend for a car listing platform.  
The project demonstrates role-based access control, JWT authentication, dictionary CRUD, listing moderation, currency conversion, premium statistics, profile management, and WebSocket chat.

## Tech stack

- Python 3.11
- Django 5
- Django REST Framework
- Simple JWT
- Django Channels
- Celery
- Redis
- MySQL 8
- Docker Compose
- Nginx

## Project structure

```text
Auto/
  backend/
    apps/
      users/
      users_auth/
      cars/
      listings/
      currency/
      chat/
    configs/
    core/
    manage.py
  mysql/
  storage/
  docker-compose.yml
  Dockerfile
  nginx.conf
```

## Main features

### Authentication and users

- JWT login and refresh
- Account activation by token
- Password recovery and password reset by token
- User roles:
  - buyer
  - seller
  - manager
  - admin
- User profile read/update
- Avatar upload
- Premium account request
- Self-delete endpoint

### Cars dictionary

Managers/admins can manage:

- brands
- model names
- car dictionary records

Public users can read dictionary data.

### Listings

Sellers can:

- create listings
- update their own listings
- upload listing photos
- delete their own listings
- request a missing brand/model

Public users can:

- browse active listings
- view listing details
- filter listings

Premium sellers can view listing statistics.

### Moderation

- Manager/admin permissions
- User blacklist
- Profanity check for listing descriptions
- Manager notifications for suspicious listing content
- Listing deactivation after repeated prohibited edits

### Currency

Listings store converted prices in:

- USD
- EUR
- UAH

Currency data is exposed as a read-only API endpoint.

### WebSocket chat

The project includes WebSocket chat for listings.

The WebSocket endpoint is:

```text
ws://localhost:8000/api/chat/<listing_id>/?token=<socket_token>
```

For Postman testing, use environment variables:

```text
ws://localhost:8000/api/chat/{{listing_id}}/?token={{socket_token}}
```

## Local setup

Create `.env` from `.env.example` and start the project:

```bash
docker compose up --build
```

Run migrations manually if needed:

```bash
docker compose run --rm app python manage.py migrate
```

Collect static files:

```bash
docker compose run --rm app python manage.py collectstatic --noinput
```

Run Django checks:

```bash
docker compose run --rm app python manage.py check
```

## Test roles

For local Postman testing, create test roles and users.

### Create roles

```bash
docker compose run --rm app python manage.py shell -c "from apps.users_auth.models import UserRoleModel; roles = ['buyer', 'seller', 'manager', 'admin']; [UserRoleModel.objects.get_or_create(name=role) for role in roles]; print('roles ready:', ', '.join(roles))"
```

### Create admin

```bash
docker compose run --rm app python manage.py shell -c "from django.contrib.auth import get_user_model; from apps.users_auth.models import UserRoleModel; User = get_user_model(); role, _ = UserRoleModel.objects.get_or_create(name='admin'); user, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com', 'role': role}); user.email = 'admin@example.com'; user.role = role; user.is_active = True; user.is_staff = True; user.is_superuser = True; user.set_password('ChangeMe123!'); user.save(); print('admin ready:', user.username)"
```

### Create seller

```bash
docker compose run --rm app python manage.py shell -c "from django.contrib.auth import get_user_model; from apps.users_auth.models import UserRoleModel; User = get_user_model(); role, _ = UserRoleModel.objects.get_or_create(name='seller'); user, _ = User.objects.get_or_create(username='seller', defaults={'email': 'seller@example.com', 'role': role}); user.email = 'seller@example.com'; user.role = role; user.is_active = True; user.is_staff = False; user.is_superuser = False; user.set_password('ChangeMe123!'); user.save(); print('seller ready:', user.username)"
```

### Create buyer

```bash
docker compose run --rm app python manage.py shell -c "from django.contrib.auth import get_user_model; from apps.users_auth.models import UserRoleModel; User = get_user_model(); role, _ = UserRoleModel.objects.get_or_create(name='buyer'); user, _ = User.objects.get_or_create(username='buyer', defaults={'email': 'buyer@example.com', 'role': role}); user.email = 'buyer@example.com'; user.role = role; user.is_active = True; user.is_staff = False; user.is_superuser = False; user.set_password('ChangeMe123!'); user.save(); print('buyer ready:', user.username)"
```

### Create manager

A manager can be created through the API by an admin:

```text
POST /api/users/managers/
```

Body:

```json
{
  "email": "manager@example.com",
  "username": "manager",
  "password": "ChangeMe123!"
}
```

## Create test currencies

```bash
docker compose run --rm app python manage.py shell -c "from decimal import Decimal; from apps.currency.models import CurrencyModel; data = [('UAH', '1.0000'), ('USD', '41.0000'), ('EUR', '44.0000')]; [CurrencyModel.objects.update_or_create(currency_code=code, defaults={'rate': Decimal(rate)}) for code, rate in data]; print(list(CurrencyModel.objects.values('id', 'currency_code', 'rate')))"
```

## Postman collection

Import:

```text
postman/Auto_API_sanitized_HTTP.postman_collection.json
postman/Auto_Local_sanitized.postman_environment.json
```

Select the environment:

```text
Auto Local - sanitized
```

The collection uses only test data:

```text
admin@example.com
manager@example.com
seller@example.com
buyer@example.com
```

Test password:

```text
ChangeMe123!
```

No real tokens or real personal email addresses should be committed.

## Account activation in Postman

The sanitized collection includes:

```text
01 Auth and manager creation → Activate account by email token
```

Endpoint:

```text
GET /api/auth/activate/{{activation_token}}/
```

For local testing:

1. Register a buyer.
2. Copy the activation token from the email/logs.
3. Paste it into the `activation_token` environment variable.
4. Run `Activate account by email token`.

## Password recovery in Postman

The sanitized collection includes:

```text
Password recovery request
Password reset by recovery token
```

Use `recovery_token` from the email/logs.

## WebSocket testing in Postman

Postman may import WebSocket requests from exported collections as regular HTTP `GET` requests.  
For this reason the sanitized HTTP collection does not include a fake WebSocket request.

Use the collection only to create the socket token:

```text
07 WebSocket helper → Seller create socket token
```

Then create the actual WebSocket tab manually:

```text
New → WebSocket
```

Paste this URL:

```text
ws://localhost:8000/api/chat/{{listing_id}}/?token={{socket_token}}
```

Important:

- The request type must be `WebSocket`, not HTTP `GET`.
- The URL must start with `ws://`, not `http://`.
- Select the correct Postman environment: `Auto Local - sanitized`.
- Do not save a real JWT token in the URL. Use `{{socket_token}}`.

Send message:

```json
{
  "action": "send_message",
  "body": "Hello from Postman"
}
```

## Useful API groups

- `00 Setup / public`
- `01 Auth and manager creation`
- `02 Superuser/admin dictionary`
- `03 Manager dictionary and moderation`
- `04 Seller listings`
- `05 Buyer checks`
- `06 Public listing read`
- `07 WebSocket helper`

## Notes

The project intentionally keeps simple read-only apps lightweight. Business logic is moved into services for users and listings, while serializers keep field-level validation and data formatting.
