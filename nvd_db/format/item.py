"""pandas: to use dataframe"""
import pandas as pd


class Item:
    """
    CVE Item class
    """

    cve: dict = None
    configurations: dict = None
    impact: dict = None
    publishedDate: str = None
    lastModifiedDate: str = None

    def __init__(self, item: pd.DataFrame):
        self.cve = item.get('cve')
        self.configurations = item.get('configurations')
        impact = pd.json_normalize(
            item.get('impact'), max_level=2).to_dict('records')
        self.impact = None if len(impact) == 0 else impact[0]
        self.publishedDate = item.get('publishedDate')
        self.lastModifiedDate = item.get('lastModifiedDate')
