"""
Abstract base class for all reports.

Provides an abstract 'generate' method and a concrete 'print_report' method
for displaying the report results using the tabulate library.
"""

import logging
from abc import ABC, abstractmethod

from tabulate import tabulate


class BaseReport(ABC):
    @abstractmethod
    def generate(self, data: list) -> dict:
        """
        Abstract method to process raw data and format it for a specific report.

        Args:
            data: A list of dictionaries representing raw data.

        Returns:
            A dictionary with 'headers' (list of strings) and 'rows' (list of lists).
        """
        pass

    def print_report(self, result: dict) -> None:
        """
        Prints the report data to the console in a grid format.

        Args:
            result: A dictionary containing 'headers' and 'rows' for display.
        """
        if not result:
            logging.info("Нет данных для отображения")
            return

        headers = result.get("headers", [])
        rows = result.get("rows", [])

        print(tabulate(rows, headers=headers, tablefmt="grid", stralign="center"))