import json, glob, re, os, time, hashlib
D = os.path.dirname(os.path.abspath(__file__))
REP = "u_FPuD6_Xo9MsK8GsBZqioGw"
import sys
PLACES, EXIST, OUT, BATCH = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
places = json.load(open(PLACES))
existing = [json.load(open(f)) for f in glob.glob(EXIST + "/*.json")]
existing = [x.get("data", x) for x in existing]

def digits(s):
    d = re.sub(r"\D", "", s or "")
    if d.startswith("00"): d = d[2:]
    if d.startswith("0"): d = "971" + d[1:]
    return d[-9:] if len(d) >= 9 else d

def norm(s): return re.sub(r"[^a-z0-9]", "", (s or "").lower())[:24]

seen_ph = set(); seen_nm = set()
for e in existing:
    for k in ("contact", "phone", "notes"):
        for m in re.findall(r"\+?\d[\d\s-]{7,}", e.get(k) or ""):
            seen_ph.add(digits(m))
    seen_nm.add(norm(e.get("business")))

SECTOR = {"restaurant": "Restaurant / café", "cafe": "Restaurant / café", "beauty salon": "Beauty / salon",
          "gym": "Gym / fitness", "clinic": "Clinic"}
SKIP_CAT = re.compile(r"showroom|college|home health|sports nutrition|properties|std clinic|public medical", re.I)
CHAIN = re.compile(r"caribou|jones the grocer|harvest & co|right health|nicolas & asp|aims health|starbucks|costa|tim hortons|mcdonald|kfc|subway|aster|mediclinic|nmc|fitness first|gold's gym|tashkent|marquee", re.I)

out = []; skipped = {"no phone": 0, "already in CRM": 0, "duplicate": 0, "big/chain": 0, "not a fit": 0}
for p in places:
    st = (p.get("searchString") or "").lower()
    st = next((k for k in SECTOR if k in st), "")
    ph = p.get("phoneUnformatted") or ""
    d = digits(ph); nm = norm(p.get("title"))
    rc = p.get("reviewsCount") or 0
    if not ph: skipped["no phone"] += 1; continue
    if d in seen_ph or nm in seen_nm:
        dup = d in {o["_d"] for o in out} or nm in {o["_n"] for o in out}
        skipped["duplicate" if dup else "already in CRM"] += 1; continue
    if SKIP_CAT.search(p.get("categoryName") or "") or not st: skipped["not a fit"] += 1; continue
    if rc >= 500 or CHAIN.search(p.get("title") or ""): skipped["big/chain"] += 1; continue
    seen_ph.add(d); seen_nm.add(nm)
    ig = (p.get("instagrams") or [None])[0]
    igh = ("@" + ig.rstrip("/").split("/")[-1].split("?")[0]) if ig else ""
    em = (p.get("emails") or [None])[0] or ""
    newish = rc < 30
    title = re.sub(r"\s*[|].*$", "", p["title"]).strip()[:80]
    bits = [f"{rc} Google reviews" + (" (likely new)" if newish else ""), (f"{p['totalScore']}★" if p.get("totalScore") else ""), igh and "IG " + igh, em, (p.get("website") or "")[:80], p.get("categoryName") or ""]
    out.append({"_d": d, "_n": nm, "_rc": rc, "doc": {
        "repId": REP, "business": title, "contact": "Ask for the owner", "phone": ph, "sector": SECTOR[st],
        "area": p["area"], "stage": "New",
        "nextStep": "Cold call: ask for the owner. " + (f"Look at {igh} before calling." if igh else "No Instagram found: open with that."),
        "nextDate": "", "notes": " · ".join(b for b in bits if b), "source": "Google Maps", "batch": BATCH,
        "reviews": rc, "instagram": ig or "", "email": em, "website": p.get("website") or "", "placeId": p.get("placeId") or ""}})

out.sort(key=lambda o: o["_rc"])  # fewest reviews (newest) first
now = int(time.time() * 1000)
os.makedirs(OUT, exist_ok=True)
for i, o in enumerate(out):
    doc = o["doc"]; doc["createdAt"] = now - i * 1000; doc["updatedAt"] = now - i * 1000
    did = "gm_" + hashlib.md5((doc["placeId"] or doc["phone"]).encode()).hexdigest()[:16]
    json.dump(doc, open(f"{OUT}/{did[3:]}.json", "w"), ensure_ascii=False)
import collections
print(len(out), skipped)
print(collections.Counter(o["doc"]["area"] for o in out)); print(collections.Counter(o["doc"]["sector"] for o in out))
print("likely new (<30 reviews):", sum(o["_rc"] < 30 for o in out), "| with Instagram:", sum(bool(o["doc"]["instagram"]) for o in out), "| mobile numbers:", sum(o["doc"]["phone"].startswith("+9715") for o in out))
