import sqlite3
import requests
import time

API_KEY = "yccFZbxfERrEAtHao2mXAEuQxGtB4R4aTbvbCe5acidHTYEqBrsAiGlw"
HEADERS = {"Authorization": API_KEY}
BASE = "https://api.pexels.com/v1"

# Define categories you want
CATEGORIES = ["standing pose", "sitting pose", "arms up", "hands on hips", "side pose", "back pose"]
PER_PAGE = 15   # Number of photos per API call per category
MAX_PER_CATEGORY = 20  # Maximum photos per category
DELAY = 1.5    # seconds between API calls to be polite

# Setup SQLite DB
DB_FILE = "pexels_photos.db"
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS photos (
    id INTEGER PRIMARY KEY,
    photo_id INTEGER UNIQUE,
    photographer TEXT,
    url TEXT,
    width INTEGER,
    height INTEGER,
    category TEXT
)
""")
conn.commit()

def get_photos(query, page=1):
    params = {"query": query, "per_page": PER_PAGE, "page": page}
    r = requests.get(f"{BASE}/search", headers=HEADERS, params=params, timeout=30)
    r.raise_for_status()
    return r.json().get("photos", [])

# Loop through each category
for category in CATEGORIES:
    print(f"Fetching category: {category}")
    downloaded = 0
    page = 1
    while downloaded < MAX_PER_CATEGORY:
        photos = get_photos(category, page)
        if not photos:
            break
        for p in photos:
            if downloaded >= MAX_PER_CATEGORY:
                break
            pid = p["id"]
            url = p.get("src", {}).get("large") or p.get("src", {}).get("original")
            photographer = p.get("photographer")
            width = p.get("width")
            height = p.get("height")
            # Insert into DB
            cur.execute("""
            INSERT OR IGNORE INTO photos (photo_id, photographer, url, width, height, category)
            VALUES (?,?,?,?,?,?)
            """, (pid, photographer, url, width, height, category))
            conn.commit()
            downloaded += 1
        page += 1
        time.sleep(DELAY)

print("✅ Done! Metadata stored in database:", DB_FILE)
conn.close()
