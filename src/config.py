from pathlib import Path

class Config:
    DATA_DIR = Path("data")
    RAW_DIR = DATA_DIR / "raw"
    CLEAN_DIR = DATA_DIR / "cleaned"
    
   
    BANKS = ["CBE", "Abyssinia", "Dashen"]

config = Config()


config.DATA_DIR.mkdir(parents=True, exist_ok=True)
config.RAW_DIR.mkdir(parents=True, exist_ok=True)
config.CLEAN_DIR.mkdir(parents=True, exist_ok=True)