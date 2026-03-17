"""
Scraper: ambil rating dari Google Maps untuk wisata, kuliner, oleholeh.
Buka setiap link di headless Chromium, ekstrak rating, simpan ke DB dan Excel.
Jalankan dari folder backend/: python scrape_ratings.py
"""
import os, sys, re, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from playwright.sync_api import sync_playwright

from app.db.session import SessionLocal
from app.models.tourism  import TourismObject
from app.models.culinary import CulinaryPlace
from app.models.souvenir import SouvenirShop

BASE = os.path.dirname(os.path.abspath(__file__))

# ─── File configs ──────────────────────────────────────────────────────────────
FILES = [
    {
        'file':       'dparis_wisata.xlsx',
        'model':      TourismObject,
        'name_col':   'Nama',
        'link_col':   'Link',
        'label':      'Wisata',
    },
    {
        'file':       'dparis_kuliner.xlsx',
        'model':      CulinaryPlace,
        'name_col':   'Nama',
        'link_col':   'Link',
        'label':      'Kuliner',
    },
    {
        'file':       'dparis_oleholeh.xlsx',
        'model':      SouvenirShop,
        'name_col':   'NAMA',
        'link_col':   'LINK',
        'label':      'OlehOleh',
    },
]


def extract_rating(page) -> float | None:
    """Try multiple selectors to extract rating from Google Maps page."""
    try:
        # Method 1: aria-label containing "bintang" or "star" or just digits like "4,5"
        # Google Maps ID for the rating span
        selectors = [
            'span[aria-hidden="true"]:near(span[role="img"])',
            'div.F7nice span[aria-hidden="true"]',
            'div.F7nice',
            'span.ceNzKf[aria-label]',
            'div.fontBodyMedium span:first-child',
        ]

        for sel in selectors:
            try:
                els = page.query_selector_all(sel)
                for el in els:
                    txt = el.inner_text().strip()
                    # Match number like "4,5" or "4.5" or "4"
                    m = re.match(r'^(\d)[,.]?(\d?)$', txt.replace(',', '.'))
                    if m:
                        val = float(txt.replace(',', '.'))
                        if 1.0 <= val <= 5.0:
                            return round(val, 1)
            except Exception:
                continue

        # Method 2: aria-label on the rating img element e.g. "Nilai: 4,5 bintang"
        try:
            img_els = page.query_selector_all('span[role="img"]')
            for el in img_els:
                label = el.get_attribute('aria-label') or ''
                m = re.search(r'(\d[,.]?\d*)', label)
                if m:
                    val = float(m.group(1).replace(',', '.'))
                    if 1.0 <= val <= 5.0:
                        return round(val, 1)
        except Exception:
            pass

        # Method 3: look at page content text for patterns like "4,5\n(123)"
        try:
            content = page.content()
            # Google Maps rating in JSON-like embedded data: ["4.5",1234]
            matches = re.findall(r'"(\d\.\d)(?:\\n|\s*)"?\s*[,\]]\s*[\[\(]?\d+', content)
            for m in matches:
                val = float(m)
                if 1.0 <= val <= 5.0:
                    return round(val, 1)

            # Also try: 4,5 followed by newline and review count
            matches2 = re.findall(r'>(\d[,.]\d)<', content)
            for m in matches2:
                val = float(m.replace(',', '.'))
                if 1.0 <= val <= 5.0:
                    return round(val, 1)
        except Exception:
            pass

    except Exception as e:
        print(f'    [extract_rating error] {e}')

    return None


def scrape_file(page, cfg: dict) -> list[dict]:
    """Scrape all ratings for one Excel file config. Returns list of {id, name, rating}."""
    path = os.path.join(BASE, cfg['file'])
    df = pd.read_excel(path)
    results = []

    total = len(df)
    for i, (_, row) in enumerate(df.iterrows()):
        rec_id   = int(row['No']) if 'No' in df.columns else int(row.get('NO', i+1))
        name     = str(row[cfg['name_col']]).strip()
        link     = str(row[cfg['link_col']]).strip() if row[cfg['link_col']] else ''

        if not link or link == 'nan':
            print(f'  [{i+1}/{total}] {name[:40]} — no link, skip')
            results.append({'id': rec_id, 'name': name, 'rating': None})
            continue

        print(f'  [{i+1}/{total}] {name[:40]}...', end=' ', flush=True)
        try:
            page.goto(link, wait_until='domcontentloaded', timeout=20000)
            # Wait a bit for JS to render the rating
            time.sleep(2.5)
            rating = extract_rating(page)
            if rating is None:
                # try waiting more and retry
                time.sleep(2)
                rating = extract_rating(page)
            print(f'rating={rating}')
            results.append({'id': rec_id, 'name': name, 'rating': rating})
        except Exception as e:
            print(f'ERROR: {e}')
            results.append({'id': rec_id, 'name': name, 'rating': None})

    return results


def update_db(model, results: list[dict]):
    """Update rating in SQLite DB for each record."""
    db = SessionLocal()
    updated = 0
    try:
        for r in results:
            if r['rating'] is not None:
                obj = db.query(model).filter(model.id == r['id']).first()
                if obj:
                    obj.rating = r['rating']
                    updated += 1
        db.commit()
        print(f'  [DB] {updated} records updated')
    except Exception as e:
        db.rollback()
        print(f'  [DB ERROR] {e}')
    finally:
        db.close()


def update_excel(cfg: dict, results: list[dict]):
    """Add/update RATING column in the Excel file."""
    path = os.path.join(BASE, cfg['file'])
    df = pd.read_excel(path)
    id_col = 'No' if 'No' in df.columns else 'NO'
    rating_map = {r['id']: r['rating'] for r in results if r['rating'] is not None}

    # Add or update RATING column (insert at position 2, after No and Nama/NAMA)
    if 'RATING' not in df.columns:
        df.insert(2, 'RATING', None)

    for idx, row in df.iterrows():
        rec_id = int(row[id_col])
        if rec_id in rating_map:
            df.at[idx, 'RATING'] = rating_map[rec_id]

    df.to_excel(path, index=False)
    non_null = df['RATING'].notna().sum()
    print(f'  [Excel] Saved. {non_null}/{len(df)} ratings populated.')


def main():
    print('=== Google Maps Rating Scraper ===\n')

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage',
                  '--lang=id-ID', '--disable-blink-features=AutomationControlled']
        )
        context = browser.new_context(
            locale='id-ID',
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        )
        page = context.new_page()

        for cfg in FILES:
            print(f'\n--- {cfg["label"]} ({cfg["file"]}) ---')
            results = scrape_file(page, cfg)
            found   = sum(1 for r in results if r['rating'] is not None)
            print(f'  Scraped: {found}/{len(results)} ratings found')
            update_db(cfg['model'], results)
            update_excel(cfg, results)

        context.close()
        browser.close()

    print('\n[DONE] Semua rating berhasil diambil dan disimpan.')


if __name__ == '__main__':
    main()
