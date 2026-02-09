from typing import Dict, List, Type

from reports.base_report import BaseReport
from reports.average_gdp_report import AverageGdpReport


class ReportFactory:
    """
    A factory class for creating instances of different report generators based on their name.
    """
    _reports: Dict[str, Type[BaseReport]] = {}
    """A registry storing available report classes mapped by report name."""

    @classmethod
    def get_report(cls, report_name: str) -> BaseReport:
        """
        Retrieves an instance of a registered report class.

        Args:
            report_name: The string identifier for the desired report type.

        Returns:
            An instance of the specified BaseReport subclass.

        Raises:
            ValueError: If the report name is not registered in the factory.
        """
        report_class = cls._reports.get(report_name)
        if not report_class:
            raise ValueError(f"Неизвестный тип отчета: {report_name}")
        return report_class()

    @classmethod
    def get_available_reports(cls) -> List[str]:
        """
        Returns a list of all currently registered report names.
        """
        return list(cls._reports.keys())

    @classmethod
    def register_report(cls, report_name: str, report_class: Type[BaseReport]) -> None:
        """
        Registers a new report type with the factory.

        Args:
            report_name: The string identifier for the report.
            report_class: The class (subclass of BaseReport) to register.
        """
        cls._reports[report_name] = report_class


ReportFactory.register_report("average-gdp", AverageGdpReport)