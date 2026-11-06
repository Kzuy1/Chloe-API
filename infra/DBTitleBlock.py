import os
import gdown
from openpyxl import load_workbook
from dotenv import load_dotenv

load_dotenv()

FIELDS = ("CUS", "SIT", "PRT", "EQU")
KEY_COLUMNS = ("PRN", "LIN", "ITESIN")


class DBTitleBlock:
    def __init__(self, database_url=os.getenv("TITLE_BLOCK_DB_URL"), database_path="./infra/dbtitleblock.xlsx"):
        self.database_url = database_url
        self.database_path = database_path
        self.rows = {}

        self.ensure_database()
        self.load()

    def ensure_database(self):
        if not os.path.exists(self.database_path) and self.database_url:
            self._download()

    def _download(self):
        gdown.download(
            self.database_url,
            self.database_path,
            quiet=False
        )

    def update_database(self):
        self._download()
        self.load()

    # Lê a planilha para a memória: {(PRN, LIN, ITESIN): {CUS, SIT, PRT, EQU}}
    def load(self):
        self.rows = {}

        if not os.path.exists(self.database_path):
            return

        sheet = load_workbook(self.database_path, read_only=True, data_only=True).active
        lines = sheet.iter_rows(values_only=True)

        header = [self._normalize(cell).upper() for cell in next(lines, ())]
        if any(column not in header for column in KEY_COLUMNS + FIELDS):
            return

        for line in lines:
            row = {column: self._normalize(value) for column, value in zip(header, line)}
            if not row.get("PRN"):
                continue

            key = (row["PRN"], self._normalize_lin(row["LIN"]), row["ITESIN"])
            self.rows[key] = {field: row[field] for field in FIELDS}

    # Busca do mais específico para o mais geral: PRN+LIN+ITESIN -> PRN+LIN -> PRN
    def get_title_block(self, prn, lin, itesin):
        prn = self._normalize(prn)
        lin = self._normalize_lin(lin)
        itesin = self._normalize(itesin)

        for key in ((prn, lin, itesin), (prn, lin, ""), (prn, "", "")):
            if key in self.rows:
                return self.rows[key]

        return None

    @staticmethod
    def _normalize(value):
        if value is None:
            return ""
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        return str(value).strip()

    # Aceita `1`, `.1` ou `1.0` na planilha e `.1` no title block
    @classmethod
    def _normalize_lin(cls, value):
        return cls._normalize(value).lstrip(".")
