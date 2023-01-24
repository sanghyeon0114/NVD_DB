from dotenv import load_dotenv
from database.database import Database
from format.cve import CVE

from query.query import Query


## global variables ##
# CPE_DATA = pd.read_csv('cpe/official-cpe-dictionary_v2.3.xml')


# [TODO] xmltodict 사용해서 CPE 데이터 뽑기

# 1. CPE dict -> CPE Dataframe
# 2. CVE Dataframe + CPE Dataframe Joining


def main():
    '''main function'''
    cve2002 = CVE(2002)
    item2002_13 = cve2002.getItem(13)
    Query.insertCve(item2002_13)
    print(Query.getLastCveId())
    print('finish')


if __name__ == "__main__":
    load_dotenv()
    Database.connect()
    Database.init()
    Query.loadQuery()
    main()
    Database.close()
