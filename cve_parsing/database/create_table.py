create_cve = '''
            CREATE TABLE IF NOT EXISTS cve (
                id                                  SERIAL PRIMARY KEY,
                data_type                           VARCHAR(1024) NOT NULL,
                data_format                         VARCHAR(1024) NOT NULL,
                data_version                        VARCHAR(1024) NOT NULL,
                CVE_data_meta                       JSONB NOT NULL,
                problemtype_data                    JSONB,
                references_data                     JSONB,
                references_tsv                      tsvector,
                description_data                    JSONB,
                description_tsv                     tsvector,
                configurations_CVE_data_version     VARCHAR(1024) NOT NULL,
                publishedDate                       TIMESTAMP NOT NULL,
                lastModifiedDate                    TIMESTAMP NOT NULL
            );
        '''

create_configuration_nodes = '''
            CREATE TABLE IF NOT EXISTS configuration_nodes (
                id              SERIAL PRIMARY KEY,
                cveId           INTEGER,
                operator        VARCHAR(1024) NOT NULL,
                parentId        INTEGER,
                FOREIGN KEY (cveId) REFERENCES cve (id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (parentId) REFERENCES configuration_nodes (id) ON DELETE CASCADE ON UPDATE CASCADE
            );
            '''

create_cpe_match = '''
            CREATE TABLE IF NOT EXISTS cpe_match (
                id                      SERIAL PRIMARY KEY,
                cveId                   INTEGER,
                nodeId                  INTEGER,
                cpe_info                JSONB,
                FOREIGN KEY (cveId) REFERENCES cve (id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (nodeId) REFERENCES configuration_nodes (id) ON DELETE CASCADE ON UPDATE CASCADE
            );
            '''

create_impact = '''
            CREATE TABLE IF NOT EXISTS impact (
                id        SERIAL PRIMARY KEY,
                cveId   INTEGER,
                baseMetricV3_cvssV3_version             VARCHAR(1024),
                baseMetricV3_cvssV3_vectorString        VARCHAR(1024),
                baseMetricV3_cvssV3_baseScore           INTEGER,
                baseMetricV3_cvssV3_baseSeverity        VARCHAR(1024),
                baseMetricV3_exploitabilityScore        INTEGER,
                baseMetricV3_impactScore                INTEGER,
                baseMetricV2_cvssV2_version             VARCHAR(1024),
                baseMetricV2_cvssV2_vectorString        VARCHAR(1024),
                baseMetricV2_cvssV2_baseScore           INTEGER,
                baseMetricV2_severity                   VARCHAR(1024),
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
                cpe22                   VARCHAR(1024),
                cpe23                   VARCHAR(1024),
                titles                  JSONB,
                titles_tsv              tsvector,
                references_data         JSONB,
                references_tsv          tsvector
            );
            '''

####################################### cpe match information #######################################

create_nvd_cpe_match = '''
            CREATE TABLE IF NOT EXISTS nvd_cpe_match (
                id                      SERIAL PRIMARY KEY,
                cpe_info                JSONB,
                cpe_name                TEXT[],
                cpe_name_tsv            tsvector
            );
            '''
