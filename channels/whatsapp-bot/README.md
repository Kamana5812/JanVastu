# Local assisted-report adapter

This is an authenticated local mock, not a WhatsApp provider connection. It requires an approved volunteer's bearer token, exact coordinates, report consent and assisted-report consent. It uses the current API's language analysis and report creation endpoints.

Set `CORE_BACKEND_URL` to the API base ending in `/api/v1`. Run `uvicorn main:app --host 127.0.0.1 --port 8001` in this directory after installing dependencies. See its `/docs` for the JSON contract.

No message is delivered to an external recipient. Real WhatsApp setup, webhook signature verification and provider delivery are deferred. Do not expose this local mock as a public provider webhook.
