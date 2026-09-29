# JanVastu frontend

React, Vite, React Router and Leaflet. Run `npm ci` then `npm run dev`. The local API proxy defaults to port 8000. Configure a hosted API origin through `VITE_API_BASE_URL`.

Checks: `npm run lint`, `node scripts/check-i18n.mjs`, `npm run build`.

UI strings use `useI18n`; add every new key to English, Hindi and Odia dictionaries. User-entered content and proper names remain in their original language. Authorization is enforced independently by the API.

See the root deployment guide and implementation status for supported workflows and external dependencies.
