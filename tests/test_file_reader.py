import csv
import os
import tempfile
from typing import List

import pytest

from utils.file_reader import read_csv_files


class TestFileReader:
    def test_read_single_valid_file(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, newline='') as f:
            writer = csv.writer(f)
            writer.writerow(
                ["country", "year", "gdp", "gdp_growth", "inflation", "unemployment", "population", "continent"]
            )
            writer.writerow(
                ["United States", "2023", "25462", "2.1", "3.4", "3.7", "339", "North America"]
            )
            temp_file = f.name

        try:
            data = read_csv_files([temp_file])
            assert len(data) == 1
            assert data[0]["country"] == "United States"
            assert data[0]["gdp"] == "25462"
            assert data[0]["continent"] == "North America"
        finally:
            os.unlink(temp_file)

    def test_read_multiple_files(self) -> None:
        files: List[str] = []
        try:
            for i in range(2):
                f = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, newline='')
                writer = csv.writer(f)
                writer.writerow(["country", "gdp"])
                writer.writerow([f"Country_{i}", f"{i*1000}"])
                files.append(f.name)
                f.close()

            data = read_csv_files(files)
            assert len(data) == 2
            assert data[0]["country"] == "Country_0"
            assert data[1]["country"] == "Country_1"
        finally:
            for file in files:
                os.unlink(file)

    def test_file_not_found(self) -> None:
        with pytest.raises(
            FileNotFoundError, match="Файл nonexistent.csv не существует"
        ):
            read_csv_files(["nonexistent.csv"])

    def test_empty_file(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["country", "gdp"])
            temp_file = f.name

        try:
            data = read_csv_files([temp_file])
            assert len(data) == 0
        finally:
            os.unlink(temp_file)

    def test_file_with_special_characters(self) -> None:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8", newline=''
        ) as f:
            writer = csv.writer(f)
            writer.writerow(["country", "gdp"])
            writer.writerow(["Страна с-ёЁ", "1000"])
            temp_file = f.name

        try:
            data = read_csv_files([temp_file])
            assert len(data) == 1
            assert data[0]["country"] == "Страна с-ёЁ"
        finally:
            os.unlink(temp_file)
