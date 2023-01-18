"""pymysql: to use database"""
import pymysql


class Database:
    """Database setting class"""
    connect = None
    cursor = None

    @staticmethod
    def print(message: str) -> None:
        """print 'database class' message function"""
        print("[database]", message)

    @staticmethod
    def connect_database():
        """Connect to database function"""
        if Database.connect is None:
            try:
                Database.connect = pymysql.connect(
                    host='localhost',
                    port=3307,
                    user='root',
                    password='asdf',
                    charset='utf8'
                )
            except pymysql.err.InternalError as err:
                code, msg = err.args
                Database.print(
                    "Database connect error : [" + code + "] " + msg)
        else:
            Database.print("Already connected database")

    @staticmethod
    def close():
        """Close to database function"""
        try:
            Database.connect.close()
        except pymysql.err.InternalError as err:
            code, msg = err.args
            Database.print("Database close error : [" + code + "] " + msg)

    @staticmethod
    def init():
        """Create database cursor and table function"""
        if Database.connect is None:
            Database.print("Database is not connected")
        try:
            Database.cursor = Database.connect.cursor()
            ####################################################
            sql = '''
            CREATE TABLE IF NOT EXISTS `mariadb`.`cve` (
                `id`                                  INTEGER NOT NULL AUTO_INCREMENT,
                `data_type`                           VARCHAR(10) NOT NULL,
                `data_format`                         VARCHAR(15) NOT NULL,
                `data_version`                        VARCHAR(10) NOT NULL,
                `CVE_data_meta_ID`                    VARCHAR(30) NOT NULL,
                `CVE_data_meta_ASSIGNER`              VARCHAR(50) NOT NULL,
                `configurations_CVE_data_version`     VARCHAR(10) NOT NULL,
                `publishedDate`                       DATETIME NOT NULL,
                `lastModifiedDate`                    DATETIME NOT NULL,
                PRIMARY KEY(`id`)
            ) ENGINE=InnoDB;
            '''
            Database.cursor.execute(sql)
            ####################################################
            sql = '''
            CREATE TABLE IF NOT EXISTS `mariadb`.`problemtype` (
                `id`      INT NOT NULL AUTO_INCREMENT,
                `cveId`   INTEGER,
                `lang`    VARCHAR(15) NOT NULL,
                `value`   TEXT NOT NULL,
                PRIMARY KEY(id),
                FOREIGN KEY (`cveId`) REFERENCES `mariadb` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
            ) CHARSET=utf8;
            '''
            Database.cursor.execute(sql)
            ####################################################
            sql = '''
            CREATE TABLE IF NOT EXISTS `mariadb`.`references` (
                `id`          INT NOT NULL AUTO_INCREMENT,
                `cveId`       INTEGER,
                `url`         TEXT NOT NULL,
                `name`        TEXT NOT NULL,
                `refsource`   VARCHAR(20) NOT NULL,
                PRIMARY KEY(id),
                FOREIGN KEY (`cveId`) REFERENCES `mariadb` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
            ) CHARSET=utf8;
            '''
            Database.cursor.execute(sql)
            ####################################################
            sql = '''
            CREATE TABLE IF NOT EXISTS `mariadb`.`references_tag` (
                `id`          INT NOT NULL AUTO_INCREMENT,
                `referenceId` INTEGER,
                `content`     TEXT NOT NULL,
                PRIMARY KEY(id),
                FOREIGN KEY (`referenceId`) REFERENCES `references` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
            ) CHARSET=utf8;
            '''
            Database.cursor.execute(sql)
            ####################################################
            sql = '''
            CREATE TABLE IF NOT EXISTS `mariadb`.`description` (
                `id`      INT NOT NULL AUTO_INCREMENT,
                `cveId`   INTEGER,
                `lang`    VARCHAR(15) NOT NULL,
                `value`   TEXT NOT NULL,
                PRIMARY KEY(id),
                FOREIGN KEY (`cveId`) REFERENCES `mariadb` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
            ) CHARSET=utf8;
            '''
            Database.cursor.execute(sql)
            ####################################################
            sql = '''
            CREATE TABLE IF NOT EXISTS `mariadb`.`configurations_nodes` (
                `id`          INT NOT NULL AUTO_INCREMENT,
                `cveId`       INTEGER,
                `operator`    VARCHAR(10) NOT NULL,
                PRIMARY KEY(id),
                FOREIGN KEY (`cveId`) REFERENCES `mariadb` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
            ) CHARSET=utf8;
            '''
            Database.cursor.execute(sql)
            #####################################################
            sql = '''
            CREATE TABLE IF NOT EXISTS `mariadb`.`cpe_match` (
                `id`                      INT NOT NULL AUTO_INCREMENT,
                `cveId`                   INTEGER,
                `nodeId`                  INTEGER,
                `vulnerable`              BOOL NOT NULL,
                `cpe23Uri`                TEXT NOT NULL,
                `versionStartIncluding`   VARCHAR(25),
                `versionEndExcluding`     VARCHAR(25),
                `metadata_title_text`     TEXT NOT NULL,
                `metadata_title_locale`   VARCHAR(10) NOT NULL,
                PRIMARY KEY(id),
                FOREIGN KEY (`cveId`) REFERENCES `mariadb` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (`nodeId`) REFERENCES `configurations_nodes` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
            ) CHARSET=utf8;
            '''
            Database.cursor.execute(sql)
            #####################################################
            sql = '''
            CREATE TABLE IF NOT EXISTS `mariadb`.`cpe_metadata_references` (
                `id`      INT NOT NULL AUTO_INCREMENT,
                `cpeId`   INTEGER,
                `type`    VARCHAR(20) NOT NULL,
                `url`     TEXT NOT NULL,
                PRIMARY KEY(id),
                FOREIGN KEY (`cpeId`) REFERENCES `cpe_match` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
            ) CHARSET=utf8;
            '''
            Database.cursor.execute(sql)
            #####################################################
            sql = '''
            CREATE TABLE IF NOT EXISTS `mariadb`.`cpe_name` (
                `id`          INT NOT NULL AUTO_INCREMENT,
                `cpeId`       INTEGER,
                `cpe23Uri`    TEXT NOT NULL,
                PRIMARY KEY(id),
                FOREIGN KEY (`cpeId`) REFERENCES `cpe_match` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
            ) CHARSET=utf8;
            '''
            Database.cursor.execute(sql)
            #####################################################
            sql = '''
            CREATE TABLE IF NOT EXISTS `mariadb`.`impact` (
                `id`        INT NOT NULL AUTO_INCREMENT,
                `cveId`   INTEGER,
                `baseMetricV3_cvssV3_version`             VARCHAR(10) NOT NULL,
                `baseMetricV3_cvssV3_vectorString`        TEXT NOT NULL,
                `baseMetricV3_cvssV3_baseScore`           INTEGER NOT NULL,
                `baseMetricV3_cvssV3_baseSeverity`        VARCHAR(10) NOT NULL,
                `baseMetricV3_exploitabilityScore`        INTEGER NOT NULL,
                `baseMetricV3_impactScore`                INTEGER NOT NULL,
                `baseMetricV2_cvssV2_version`             VARCHAR(10) NOT NULL,
                `baseMetricV2_cvssV2_vectorString`        TEXT NOT NULL,
                `baseMetricV2_cvssV2_baseScore`           INTEGER NOT NULL,
                `baseMetricV2_severity`                   VARCHAR(10) NOT NULL,
                `baseMetricV2_exploitabilityScore`        INTEGER NOT NULL,
                `baseMetricV2_impactScore`                INTEGER NOT NULL,
                `baseMetricV2_acInsufInfo`                BOOL NOT NULL,
                `baseMetricV2_obtainAllPrivilege`         BOOL NOT NULL,
                `baseMetricV2_obtainUserPrivilege`        BOOL NOT NULL,
                `baseMetricV2_obtainOtherPrivilege`       BOOL NOT NULL,
                `baseMetricV2_userInteractionRequired`    BOOL NOT NULL,
                PRIMARY KEY(id),
                FOREIGN KEY (`cveId`) REFERENCES `mariadb` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
            ) CHARSET=utf8;
            '''
            Database.cursor.execute(sql)

        except pymysql.err.InternalError as err:
            code, msg = err.args
            Database.print("create Table error : [" + code + "] " + msg)
