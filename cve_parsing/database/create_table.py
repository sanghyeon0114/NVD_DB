# [TODO] all TEXT -> VARCHAR ( dynamic -> static )

create_cve = '''
            CREATE TABLE IF NOT EXISTS cve (
                id                                  SERIAL PRIMARY KEY,
                data_type                           VARCHAR(10) NOT NULL,
                data_format                         VARCHAR(15) NOT NULL,
                data_version                        VARCHAR(10) NOT NULL,
                CVE_data_meta_ID                    VARCHAR(30) NOT NULL,
                CVE_data_meta_ASSIGNER              VARCHAR(50) NOT NULL,
                configurations_CVE_data_version     VARCHAR(10) NOT NULL,
                publishedDate                       TIMESTAMP NOT NULL,
                lastModifiedDate                    TIMESTAMP NOT NULL
            );
        '''

create_problemtypes = '''
            CREATE TABLE IF NOT EXISTS problemtype_data (
                id      SERIAL PRIMARY KEY,
                cveId   INTEGER,
                lang    VARCHAR(15) NOT NULL,
                value   TEXT NOT NULL,
                FOREIGN KEY (cveId) REFERENCES cve (id) ON DELETE CASCADE ON UPDATE CASCADE
            );
            '''

create_references = '''
            CREATE TABLE IF NOT EXISTS reference_data (
                id          SERIAL PRIMARY KEY,
                cveId       INTEGER,
                url         TEXT NOT NULL,
                name        TEXT NOT NULL,
                refsource   VARCHAR(20) NOT NULL,
                tag         TEXT[],
                FOREIGN KEY (cveId) REFERENCES cve (id) ON DELETE CASCADE ON UPDATE CASCADE
            );
            '''

create_descriptions = '''
            CREATE TABLE IF NOT EXISTS description_data (
                id      SERIAL PRIMARY KEY,
                cveId   INTEGER,
                lang    VARCHAR(15) NOT NULL,
                value   TEXT NOT NULL,
                FOREIGN KEY (cveId) REFERENCES cve (id) ON DELETE CASCADE ON UPDATE CASCADE
            );
            '''

create_configuration_nodes = '''
            CREATE TABLE IF NOT EXISTS configuration_nodes (
                id          SERIAL PRIMARY KEY,
                cveId       INTEGER,
                operator    VARCHAR(10) NOT NULL,
                parentId      INTEGER,
                FOREIGN KEY (cveId) REFERENCES cve (id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (parentId) REFERENCES configuration_nodes (id) ON DELETE CASCADE ON UPDATE CASCADE
            );
            '''

create_cpe_match = '''
            CREATE TABLE IF NOT EXISTS cpe_match (
                id                      SERIAL PRIMARY KEY,
                cveId                   INTEGER,
                nodeId                  INTEGER,
                vulnerable              BOOL NOT NULL,
                cpe23Uri                TEXT NOT NULL,
                part                    VARCHAR(64),
                vendor                  VARCHAR(64),
                product                 VARCHAR(64),
                version                 VARCHAR(64),
                update                  VARCHAR(64),
                edition                 VARCHAR(64),
                language                VARCHAR(64),
                software_edition        VARCHAR(64),
                target_software         VARCHAR(64),
                target_hardware         VARCHAR(64),
                other                   VARCHAR(64),
                versionStartIncluding   VARCHAR(25),
                versionEndIncluding     VARCHAR(25),
                versionStartExcluding   VARCHAR(25),
                versionEndExcluding     VARCHAR(25),
                cpe_name                TEXT[],
                FOREIGN KEY (cveId) REFERENCES cve (id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (nodeId) REFERENCES configuration_nodes (id) ON DELETE CASCADE ON UPDATE CASCADE
            );
            '''

create_impact = '''
            CREATE TABLE IF NOT EXISTS impact (
                id        SERIAL PRIMARY KEY,
                cveId   INTEGER,
                baseMetricV3_cvssV3_version             VARCHAR(10),
                baseMetricV3_cvssV3_vectorString        TEXT,
                baseMetricV3_cvssV3_baseScore           INTEGER,
                baseMetricV3_cvssV3_baseSeverity        VARCHAR(10),
                baseMetricV3_exploitabilityScore        INTEGER,
                baseMetricV3_impactScore                INTEGER,
                baseMetricV2_cvssV2_version             VARCHAR(10),
                baseMetricV2_cvssV2_vectorString        TEXT,
                baseMetricV2_cvssV2_baseScore           INTEGER,
                baseMetricV2_severity                   VARCHAR(10),
                baseMetricV2_exploitabilityScore        INTEGER,
                baseMetricV2_impactScore                INTEGER,
                baseMetricV2_acInsufInfo                BOOL,
                baseMetricV2_obtainAllPrivilege         BOOL,
                baseMetricV2_obtainUserPrivilege        BOOL,
                baseMetricV2_obtainOtherPrivilege       BOOL,
                baseMetricV2_userInteractionRequired    BOOL,
                FOREIGN KEY (cveId) REFERENCES cve (id) ON DELETE CASCADE ON UPDATE CASCADE
            );
            '''

####################################### cpe information #######################################

create_cpe = '''
            CREATE TABLE IF NOT EXISTS cpe (
                id                      SERIAL PRIMARY KEY,
                cpe22                   TEXT,
                title_value             TEXT,
                title_lang              VARCHAR(16),
                cpe23                   TEXT,   
                part                    VARCHAR(64),
                vendor                  VARCHAR(64),
                product                 VARCHAR(64),
                version                 VARCHAR(64),
                update                  VARCHAR(64),
                edition                 VARCHAR(64),
                language                VARCHAR(64),
                software_edition        VARCHAR(64),
                target_software         VARCHAR(64),
                target_hardware         VARCHAR(64),
                other                   VARCHAR(64)
            );
            '''

create_cpe_references = '''
            CREATE TABLE IF NOT EXISTS cpe_references (
                id      SERIAL PRIMARY KEY,
                cpeId   INTEGER,
                type    TEXT,
                uri   TEXT,
                FOREIGN KEY (cpeId) REFERENCES cpe (id) ON DELETE CASCADE ON UPDATE CASCADE
            );
            '''