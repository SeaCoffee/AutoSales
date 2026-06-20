# Postman testing notes

Import the sanitized collection and environment:

```text
Auto_API_sanitized_HTTP.postman_collection.json
Auto_Local_sanitized.postman_environment.json
```

Select environment:

```text
Auto Local - sanitized
```

## Activation

The collection includes:

```text
01 Auth and manager creation → Activate account by email token
```

Endpoint:

```text
GET {{base_url}}/api/auth/activate/{{activation_token}}/
```

Put the token from email/logs into:

```text
activation_token
```

## WebSocket

Postman often imports exported WebSocket requests as regular HTTP `GET` requests.  
So the collection intentionally includes only:

```text
07 WebSocket helper → Seller create socket token
```

After running it, create the WebSocket request manually:

```text
New → WebSocket
```

Use:

```text
ws://localhost:8000/api/chat/{{listing_id}}/?token={{socket_token}}
```

Check before connecting:

- selected environment: `Auto Local - sanitized`
- `listing_id` is set
- `socket_token` is set
- URL starts with `ws://`
- Postman request type is `WebSocket`, not `GET`

Message example:

```json
{
  "action": "send_message",
  "body": "Hello from Postman"
}
```
