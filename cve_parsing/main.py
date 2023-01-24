from database import Database
from query.query import Query
from format.cve import CVE
from dotenv import load_dotenv


## global variables ##
# CPE_DATA = pd.read_csv('cpe/official-cpe-dictionary_v2.3.xml')


# [TODO] xmltodict 사용해서 CPE 데이터 뽑기

# 1. CPE dict -> CPE Dataframe
# 2. CVE Dataframe + CPE Dataframe Joining


def main():
    '''main function'''
    cve2002 = CVE(2002)
    # item2002_13 = cve2002.getItem(13)
    # Database.insert_cve(item2002_13)
    # print(Database.getLastCveId())
    print('finish')


if __name__ == "__main__":
    load_dotenv()
    Query.loadQuery()
    Database.connect_database()
    Database.init()
    main()
    Database.close()