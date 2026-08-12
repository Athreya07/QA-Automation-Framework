"""
excel_utils.py
==========================================================
OpenPyXL-based Excel reader used for Data-Driven Testing
(DDT). Reads structured test data (e.g. login credentials)
from testdata/*.xlsx and returns it as a list of dicts,
ready to be consumed by @pytest.mark.parametrize.
==========================================================
"""

from pathlib import Path
from typing import List, Dict

import openpyxl

from utilities.logger import get_logger

logger = get_logger("ExcelUtils")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TESTDATA_DIR = PROJECT_ROOT / "testdata"


class ExcelUtils:

    @staticmethod
    def read_excel_data(file_name: str, sheet_name: str = None) -> List[Dict]:
        """
        Reads an Excel file and converts it into a list of dictionaries,
        one dict per data row, keyed by the header row.

        Args:
            file_name: e.g. "login_data.xlsx" (relative to testdata/).
            sheet_name: optional sheet name; defaults to the active sheet.

        Returns:
            List[Dict[str, Any]] - e.g.
            [
                {"username": "standard_user", "password": "secret_sauce", "expected_result": "success"},
                {"username": "locked_out_user", "password": "secret_sauce", "expected_result": "locked"},
            ]
        """
        file_path = TESTDATA_DIR / file_name

        if not file_path.exists():
            raise FileNotFoundError(f"Excel test data file not found: {file_path}")

        logger.info(f"Reading test data from: {file_path} (sheet={sheet_name or 'active'})")

        workbook = openpyxl.load_workbook(file_path, data_only=True)
        sheet = workbook[sheet_name] if sheet_name else workbook.active

        rows = list(sheet.iter_rows(values_only=True))
        if not rows:
            logger.warning(f"No data found in {file_path}")
            return []

        headers = [str(h).strip() for h in rows[0]]
        data = []
        for row in rows[1:]:
            if all(cell is None for cell in row):
                continue  # skip fully blank rows
            row_dict = dict(zip(headers, row))
            data.append(row_dict)

        logger.info(f"Loaded {len(data)} row(s) of test data from {file_name}")
        return data

    @staticmethod
    def get_login_test_data() -> List[tuple]:
        """
        Convenience method specifically for login data-driven tests.
        Returns a list of tuples suitable for direct use in
        @pytest.mark.parametrize("username,password,expected_result", data).
        """
        rows = ExcelUtils.read_excel_data("login_data.xlsx")
        return [
            (row.get("username"), row.get("password"), row.get("expected_result"))
            for row in rows
        ]
