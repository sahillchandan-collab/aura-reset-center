# Daily Google Maps leads for the Sales CRM

`prep.py PLACES.json EXISTING_LEADS_DIR OUT_DIR BATCH` turns an Apify
`compass/crawler-google-places` export into CRM `leads` docs for Usama:
dedupes by phone and name against the CRM, skips chains, 500+ review places
and entries without a phone, and sorts newest (fewest reviews) first.
Each place needs an `area` field (added before running). Output files are
named by doc id without the `gm_` prefix; write them with ArtifactData batch
as `leads/gm_<file name>`.

Search terms per area: restaurant, cafe, beauty salon, gym, clinic + "<area> Dubai",
16 places each, skipClosedPlaces, scrapeContacts.
