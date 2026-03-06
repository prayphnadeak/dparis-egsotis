"""Master script to run all data seeders."""
import os
import sys
import logging

# Add root backend to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import seed_akomodasi, seed_wisata, seed_kuliner, seed_oleholeh

logger = logging.getLogger("dparis.seed")

def seed():
    logger.info("Starting master seeding process...")
    try:
        logger.info("Seeding Akomodasi...")
        seed_akomodasi.seed()
        
        logger.info("Seeding Wisata...")
        seed_wisata.seed()
        
        logger.info("Seeding Kuliner...")
        seed_kuliner.seed()
        
        logger.info("Seeding Oleh-oleh...")
        seed_oleholeh.seed()
        
        logger.info("✅ All seeders completed successfully.")
    except Exception as e:
        logger.error("❌ Master seeding failed: %s", e)
        # We don't raise here to allow app startup even if seeding fails partially
        # But we logged the error.

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    seed()
