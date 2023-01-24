"""pandas: to use dataframe"""
import pandas as pd


class Item:
    """
    CVE Item class
    """

    cve: pd.DataFrame = None
    configurations: pd.DataFrame = None
    impact: pd.DataFrame = None
    publishedDate: str
    lastModifiedDate: str

    def __init__(self, item: pd.DataFrame):
        self.cve = item['cve']
        self.configurations = item['configurations']
        self.impact = item['impact']
        self.publishedDate = item['publishedDate']
        self.lastModifiedDate = item['lastModifiedDate']