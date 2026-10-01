"""Loads the data into an in-memory SQLite database and runs the .sql files."""
import sqlite3
from pathlib import Path

import pandas as pd

from .sample_data import generate

ROOT = Path(__file__).resolve().parent.parent
SQL_DIR = ROOT / "sql"
RAW_CSV = ROOT / "data" / "raw" / "hr_attrition.csv"

REQUIRED_COLUMNS = [
    "Age", "Attrition", "Department", "EducationField", "MonthlyIncome", "WorkLifeBalance",
    "YearsAtCompany", "NumCompaniesWorked", "DistanceFromHome", "JobSatisfaction",
]


def read_csv_any_encoding(path: Path) -> pd.DataFrame:
    if path.read_bytes()[:2] == b"PK":
        raise ValueError(
            "hr_attrition.csv is a zip file, not a CSV. Extract it and rename the file inside."
        )
    for encoding in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            df = pd.read_csv(path, encoding=encoding)
            df.columns = df.columns.str.strip()
            return df
        except UnicodeDecodeError:
            continue
    raise ValueError("Could not read hr_attrition.csv with a common text encoding.")


def load_dataframe() -> tuple[pd.DataFrame, bool]:
    """Return (dataframe, using_sample_data)."""
    if RAW_CSV.exists():
        df = read_csv_any_encoding(RAW_CSV)
        missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            raise ValueError(f"hr_attrition.csv is missing columns: {missing}")
        return df, False
    return generate(), True


def make_connection(df: pd.DataFrame, path: str = ":memory:") -> sqlite3.Connection:
    conn = sqlite3.connect(path, check_same_thread=False)
    df.to_sql("employees", conn, index=False, if_exists="replace")
    conn.executescript((SQL_DIR / "00_schema.sql").read_text())
    return conn


def read_sql_file(name: str) -> str:
    return (SQL_DIR / name).read_text()


def run_query(conn: sqlite3.Connection, name: str) -> pd.DataFrame:
    return pd.read_sql_query(read_sql_file(name), conn)


if __name__ == "__main__":
    # Writes data/hr.db so you can open it in DB Browser for SQLite and run the queries by hand.
    frame, sample = load_dataframe()
    out = ROOT / "data" / "hr.db"
    out.unlink(missing_ok=True)
    make_connection(frame, str(out)).close()
    print(f"Wrote {out} ({'sample' if sample else 'real'} data, {len(frame)} rows)")
