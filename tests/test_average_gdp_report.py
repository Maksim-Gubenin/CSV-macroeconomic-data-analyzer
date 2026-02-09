import os
from reports.average_gdp_report import AverageGdpReport
from utils.file_reader import read_csv_files

FILE_PATHS = [
    "test_data/economic1.csv",
    "test_data/economic2.csv",
]

for p in FILE_PATHS:
    if not os.path.exists(p):
        raise FileNotFoundError(f"Тестовый файл не найден: {p}")


def test_average_gdp_report_generation():
    """
    Tests that the average GDP report generates correctly with known test data.
    """
    all_data = read_csv_files(FILE_PATHS)
    report_generator = AverageGdpReport()
    result = report_generator.generate(all_data)

    assert result["headers"] == ["Country", "Average GDP"]
    rows = result["rows"]

    assert len(rows) == 20
    assert rows[0] == ['United States', 23923.67]
    assert rows[1] == ['China', 17810.33]
    assert rows[2] == ['Japan', 4467.0]


def test_average_gdp_empty_data():
    """
    Tests the handling of an empty data list provided to the generator.
    """
    report_generator = AverageGdpReport()
    result = report_generator.generate([])

    assert result["headers"] == ["Country", "Average GDP"]
    assert result["rows"] == []