# Bhubaneswar infrastructure dataset

Imported 29 September 2026 from the three screenshots supplied by the user. The screenshots appear to contain AI-generated summaries; they are not treated as government datasets.

## Coverage and deduplication

The JSON fixture at `backend/app/data/bhubaneswar.json` contains **16 records and 21 source observations**: six bridge/footbridge entries, three road/corridor entries and seven park entries. Screenshot 2 repeats screenshot 1. Rajmahal is merged across all three screenshots. Janpath, Biju Patnaik Park and the expressway retain alternate observations from screenshot 3. Subash Chandra Bose Setu and Madhusudan Das Park are added from screenshot 3.

The flyover and 8-lane expressway remain separately named components, linked through the `jaydev-corridor` shared-budget group. These 16 records must not be interpreted as 16 independent budgets. The combined footbridge and three-park entries remain grouped as supplied.

Each screenshot source includes its original filename and SHA-256 fingerprint. Screenshot files themselves are not required at runtime. Receipt date is not a publication date. Original source text remains in its supplied language; interface labels support English, Hindi and Odia.

## Conflicts and official references

- Biju Patnaik Park has different agencies, completion/renovation years and cost descriptions.
- Janpath has approximately 30 versus 36 months and a completion range versus a single year. The screenshots report ₹80 crore. Rajya Sabha question 2950, Annexure I, page 6, lists Smart Janpath under completed projects at ₹181.10 crore, from data as of 3 March 2023. Different scope or reporting dates may explain the difference; this import does not decide that question. [Official parliamentary answer](https://sansad.in/getFile/annex/259/AU2950.pdf?source=pqars).
- The expressway observations differ on executing agency, target year and whether cost is stated separately or included in the flyover budget.
- The Cabinet release dated 19 August 2025 confirms the ring road's approved capital cost of ₹8,307.74 crore and 110.875 km/6-lane scope. It does not establish the screenshots' current construction status, target completion year or execution duration. [Official PIB release](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2157887&lang=2&reg=48).

All other screenshot claims remain unverified. Official badges apply only to the corresponding observations, with dates displayed; they do not certify the entire record.

## Import and display

Run migrations, then `python -m app.db.import_datasets` from `backend` with the intended database configured. The regular seed also imports these records. Stable IDs and insert-only behavior make repeated imports safe; existing curated records are preserved. Fixture revisions require explicit review and a controlled update rather than silently overwriting database edits.

Records appear in public accountability search and detail. Missing exact coordinates, administrative district, progress, dates and sanctioned/actual costs remain unavailable. Reported year ranges and estimated/actual cost wording stay as text. Cost observations with official definitions carry units and kind; no total is computed across records. Parks use the existing `other` reporting category and preserve `Park` as the dataset asset type.

The import never feeds raw costs into planning context, creates fake project events, or assumes completed means 100% progress. Unknown locations do not appear at fabricated map positions. Historical official status does not establish current status.
