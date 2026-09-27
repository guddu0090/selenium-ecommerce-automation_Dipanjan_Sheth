"""
Requirement #8: Read test data from Excel/JSON.
Defaults to JSON; falls back to / can be forced to Excel.
"""
import json
import os

from openpyxl import load_workbook

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(HERE, "test_data", "test_data.json")
EXCEL_PATH = os.path.join(HERE, "test_data", "test_data.xlsx")


def read_json_data():
    with open(JSON_PATH) as f:
        return json.load(f)


def read_excel_data():
    """Reads the same structure back out of test_data.xlsx."""
    wb = load_workbook(EXCEL_PATH)

    def sheet_to_dict(sheet_name):
        ws = wb[sheet_name]
        rows = list(ws.iter_rows(min_row=2, values_only=True))
        return {k: v for k, v in rows if k is not None}

    general = sheet_to_dict("General")
    data = {
        "base_url": general["base_url"],
        "search_product": general["search_product"],
        "quantity_to_set": str(general["quantity_to_set"]),
        "user": sheet_to_dict("User"),
        "signup_details": sheet_to_dict("SignupDetails"),
    }
    return data


def load_test_data(source="json"):
    """
    source: "json" or "excel"
    Falls back to JSON automatically if the Excel file hasn't been generated yet.
    """
    if source == "excel" and os.path.exists(EXCEL_PATH):
        return read_excel_data()
    return read_json_data()
