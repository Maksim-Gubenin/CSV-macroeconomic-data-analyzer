"""
CLI tool for analyzing macroeconomic data from CSV files and generating reports.

This script processes one or more CSV files containing economic indicators (e.g., GDP),
and outputs a formatted report to the console based on the specified report type.
"""
import argparse
import sys
import logging

from reports.report_factory import ReportFactory
from utils.file_reader import read_csv_files


logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main() -> None:
    """
    Main entry point for the script.

    Parses command-line arguments, reads data from CSV files,
    generates the specified report, and prints it to the console.
    Handles file and data processing errors using logging.
    """
    parser = argparse.ArgumentParser(
        description="Анализ макроэкономических данных и формирование отчетов",
    )
    parser.add_argument(
        "--files",
        required=True,
        nargs="+",
        help="Пути к CSV файлам через пробел",
    )
    parser.add_argument(
        "--report",
        required=True,
        choices=ReportFactory.get_available_reports(),
        help="Тип отчета для генерации",
    )

    args = parser.parse_args()

    try:
        data = read_csv_files(args.files)

        if not data:
            logging.info("Нет данных для анализа")
            return

        report = ReportFactory.get_report(args.report)
        result = report.generate(data)
        report.print_report(result)

    except FileNotFoundError as e:
        logging.error(f"Ошибка: Файл не найден - {e}")
        sys.exit(1)
    except ValueError as e:
        logging.error(f"Ошибка в данных: {e}")
        sys.exit(1)
    except (KeyError, TypeError, IOError) as e:
        logging.error(f"Ошибка при обработке данных: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()