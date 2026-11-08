"""Original CSV export boundary inspired by EDB-49805; no spreadsheet is launched."""
import csv
from io import StringIO
from pathlib import Path


def export_cell(value):
    # VULNERABLE: CSV quoting preserves structure but does not neutralize formulas.
    return value


def run(rows):
    if (not isinstance(rows, list) or not 1 <= len(rows) <= 20
            or any(not isinstance(row, list) or len(row) != 2
                   or any(not isinstance(cell, str) or len(cell) > 512 or "\x00" in cell
                          for cell in row) for row in rows)):
        return {"status": 400, "error": "invalid rows"}
    buffer = StringIO(newline="")
    writer = csv.writer(buffer, quoting=csv.QUOTE_ALL, lineterminator="\r\n")
    writer.writerow(["description", "owner"])
    writer.writerows([export_cell(cell) for cell in row] for row in rows)
    result = buffer.getvalue()
    try:
        encoded = result.encode("utf-8")
    except UnicodeEncodeError:
        return {"status": 400, "error": "invalid rows"}
    Path("export.csv").write_bytes(encoded)
    return {"status": 200, "csv": result}
