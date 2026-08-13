import os
import sqlite3
import gdown
from dotenv import load_dotenv

load_dotenv()

class DBArticoli: 
    def __init__(self, database_url=os.getenv("DB_ARTICOLI_URL"), database_path="./infra/dbarticoli.db"): 
        self.database_url = database_url 
        self.database_path = database_path 
        self.conn = None 

        self.ensure_database()
        self.connect()

    def connect(self):
        self.conn = sqlite3.connect(self.database_path)
        self.conn.row_factory = sqlite3.Row

    def ensure_database(self): 
        if not os.path.exists(self.database_path): 
            self._download()

    def _download(self): 
        gdown.download(
            self.database_url,
            self.database_path,
            quiet=False
        )

    def update_database(self):
        if self.conn:
            self.conn.close()
            self.conn = None

        self._download()

        self.connect()

    def get_article(self, code, article_type):
        if article_type == "FASTENERS":
            table = "DBR_TFASTENERS"
        else:
            table = "DBR_OTHERS"

        cursor = self.conn.cursor()

        cursor.execute(
            f"""
            SELECT *
            FROM {table}
            WHERE CODE = ?
            """,
            (code,)
        )

        return cursor.fetchone()

    def normalize_article(self, article, quantity, block_type):
        quantity = float(quantity or 0)

        if block_type == "FASTENERS":
            weight = (
                0
                if article["WEIGHT"] is None
                else float(str(article["WEIGHT"]).replace(",", "."))
            )

            return {
                "DESCL1": article["DescriptionENG"],
                "UNI": "N.",
                "WEIGHT": weight,
                "TOTAL": round(weight * quantity, 3),
                "MATERIAL": article["MATERIAL"] or "",
                "NORM": article["NORM"] or "",
                "STANDARD": article["STANDARD"] or "",
                "STYPE": article["STYPE"] or "",
                "TYPE": article["TYPE"] or "",
                "DIAMETER": article["DIAMETER"] or "",
            }

        if block_type in ("GASKET", "RAW+INSULATION", "FITTINGS+OTHERS"):
            weight = (
                0
                if article["Unitweight"] is None
                else float(str(article["Unitweight"]).replace(",", "."))
            )

            normalized = {
                "DESCL1": article["DescriptionENG"],
                "WEIGHT": weight,
                "TOTAL": round(weight * quantity, 3),
                "MATERIAL": article["MATERIAL"] or "",
                "NORM": "",
                "STANDARD": article["Standard"] or "",
                "STYPE": article["STYPE"] or "",
                "TYPE": article["TYPE"] or "",
            }

            if block_type in ("GASKET", "RAW+INSULATION"):
                normalized["UNI"] = article["Unit"] or ""

            return normalized

        return None
        
        