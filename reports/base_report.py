from abc import ABC, abstractmethod

from tabulate import tabulate


class BaseReport(ABC):
    @abstractmethod
    def generate(self, data: list) -> dict:
        pass

    def print_report(self, result: dict) -> None:
        if not result:
            print("Нет данных для отображения")
            return

        headers = result.get("headers", [])
        rows = result.get("rows", [])

        print(tabulate(rows, headers=headers, tablefmt="grid", stralign="center"))