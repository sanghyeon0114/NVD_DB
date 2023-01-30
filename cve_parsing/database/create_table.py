create_cve = '''
            CREATE TABLE IF NOT EXISTS cve (
                id                                  SERIAL PRIMARY KEY,
                data_type                           VARCHAR(255) NOT NULL,
                data_format                         VARCHAR(255) NOT NULL,
                data_version                        VARCHAR(255) NOT NULL,
                CVE_data_meta_ID                    VARCHAR(255) NOT NULL,
                CVE_data_meta_ASSIGNER              VARCHAR(255) NOT NULL,
                configurations_CVE_data_version     VARCHAR(255) NOT NULL,
                publishedDate                       TIMESTAMP NOT NULL,
                lastModifiedDate                    TIMESTAMP NOT NULL
            );
        '''

create_problemtypes = '''
            CREATE TABLE IF NOT EXISTS problemtype_data (
                id      SERIAL PRIMARY KEY,
                cveId   INTEGER,
                lang    VARCHAR(15) NOT NULL,
                value   VARCHAR(255) NOT NULL,
                FOREIGN KEY (cveId) REFERENCES cve (id) ON DELETE CASCADE ON UPDATE CASCADE
            );
            '''

create_references = '''
            CREATE TABLE IF NOT EXISTS reference_data (
                id          SERIAL PRIMARY KEY,
                cveId       INTEGER,
                url         VARCHAR(255) NOT NULL,
                name        VARCHAR(255) NOT NULL,
                refsource   VARCHAR(255) NOT NULL,
                tag         VARCHAR(255)[],
                FOREIGN KEY (cveId) REFERENCES cve (id) ON DELETE CASCADE ON UPDATE CASCADE
            );
            '''

create_descriptions = '''
            CREATE TABLE IF NOT EXISTS description_data (
                id      SERIAL PRIMARY KEY,
                cveId   INTEGER,
                lang    VARCHAR(255) NOT NULL,
                value   VARCHAR(255) NOT NULL,
                FOREIGN KEY (cveId) REFERENCES cve (id) ON DELETE CASCADE ON UPDATE CASCADE
            );
            '''

create_configuration_nodes = '''
            CREATE TABLE IF NOT EXISTS configuration_nodes (
                id          SERIAL PRIMARY KEY,
                cveId       INTEGER,
                operator    VARCHAR(255) NOT NULL,
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
                cpe23Uri                VARCHAR(255) NOT NULL,
                part                    VARCHAR(255),
                vendor                  VARCHAR(255),
                product                 VARCHAR(255),
                version                 VARCHAR(255),
                update                  VARCHAR(255),
                edition                 VARCHAR(255),
                language                VARCHAR(255),
                software_edition        VARCHAR(255),
                target_software         VARCHAR(255),
                target_hardware         VARCHAR(255),
                other                   VARCHAR(255),
                versionStartIncluding   VARCHAR(255),
                versionEndIncluding     VARCHAR(255),
                versionStartExcluding   VARCHAR(255),
                versionEndExcluding     VARCHAR(255),
                cpe_name                VARCHAR(255)[],
                FOREIGN KEY (cveId) REFERENCES cve (id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (nodeId) REFERENCES configuration_nodes (id) ON DELETE CASCADE ON UPDATE CASCADE
            );
            '''

create_impact = '''
            CREATE TABLE IF NOT EXISTS impact (
                id        SERIAL PRIMARY KEY,
                cveId   INTEGER,
                baseMetricV3_cvssV3_version             VARCHAR(255),
                baseMetricV3_cvssV3_vectorString        VARCHAR(255),
                baseMetricV3_cvssV3_baseScore           INTEGER,
                baseMetricV3_cvssV3_baseSeverity        VARCHAR(255),
                baseMetricV3_exploitabilityScore        INTEGER,
                baseMetricV3_impactScore                INTEGER,
                baseMetricV2_cvssV2_version             VARCHAR(255),
                baseMetricV2_cvssV2_vectorString        VARCHAR(255),
                baseMetricV2_cvssV2_baseScore           INTEGER,
                baseMetricV2_severity                   VARCHAR(255),
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
                cpe22                   VARCHAR(255),
                cpe23                   VARCHAR(255),   
                part                    VARCHAR(255),
                vendor                  VARCHAR(255),
                product                 VARCHAR(255),
                version                 VARCHAR(255),
                update                  VARCHAR(255),
                edition                 VARCHAR(255),
                language                VARCHAR(255),
                software_edition        VARCHAR(255),
                target_software         VARCHAR(255),
                target_hardware         VARCHAR(255),
                other                   VARCHAR(255)
            );
            '''

create_cpe_titles = '''
            CREATE TABLE IF NOT EXISTS cpe_titles (
                id                      SERIAL PRIMARY KEY,
                cpeId                   INTEGER,
                value                   VARCHAR(255),
                lang                    VARCHAR(255),
                FOREIGN KEY (cpeId) REFERENCES cpe (id) ON DELETE CASCADE ON UPDATE CASCADE
            );
            '''

create_cpe_references = '''
            CREATE TABLE IF NOT EXISTS cpe_references (
                id          SERIAL PRIMARY KEY,
                cpeId       INTEGER,
                type        VARCHAR(255),
                uri         VARCHAR(255),
                FOREIGN KEY (cpeId) REFERENCES cpe (id) ON DELETE CASCADE ON UPDATE CASCADE
            );
            '''
