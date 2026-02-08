from reports.base_report import BaseReport
from collections import defaultdict


class AverageGdpReport(BaseReport):
    """
    Generates a report calculating the average GDP for each country from raw data.

    This report sorts countries in descending order of their average GDP.
    """
    def generate(self, data: list) -> dict:
        """
        Processes raw data to calculate the average GDP per country.

        Args:
            data: A list of dictionaries, where each dictionary represents a row
                  from a CSV file with keys like 'country' and 'gdp'.

        Returns:
            A dictionary formatted for display, containing 'headers' (list of strings)
            and 'rows' (list of lists of data).
        """
        gdp_by_country = defaultdict(list)
        for row in data:
            country = row.get('country')
            gdp_str = row.get('gdp')
            if country and gdp_str:
                try:
                    gdp = float(gdp_str)
                    gdp_by_country[country].append(gdp)
                except ValueError:
                    continue

        average_gdp_results = []
        for country, gdp_list in gdp_by_country.items():
            if gdp_list:
                average_gdp = sum(gdp_list) / len(gdp_list)
                average_gdp_results.append({
                    'Country': country,
                    'Average GDP': round(average_gdp, 2)
                })

        average_gdp_results.sort(key=lambda x: x['Average GDP'], reverse=True)

        headers = ["Country", "Average GDP"]
        rows = [[item['Country'], item['Average GDP']] for item in average_gdp_results]

        return {
            "headers": headers,
            "rows": rows
        }