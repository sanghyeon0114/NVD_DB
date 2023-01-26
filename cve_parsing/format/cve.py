"""pandas: to use dataframe"""
import pandas as pd

from .item import Item

# [TODO] pandas를 통해 CVE 데이터 가공


class CVE:
    """
    Class that reprocesses CVE into Dataframe
    """

    items: pd.DataFrame = None
    length: int = None

    def __init__(self, year):
        self.items = pd.read_json(
            "cve/nvdcve-1.1-{}.json".format(year)).get('CVE_Items')
        self.length = len(self.items)

    def getItem(self, number: int) -> Item:
        return Item(self.items[number])
