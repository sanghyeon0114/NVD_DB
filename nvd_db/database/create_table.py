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
                cpe                     VARCHAR(1024) NOT NULL,
                versionStartIncluding   VARCHAR(128) NOT NULL,
                versionEndIncluding     VARCHAR(128) NOT NULL,
                versionStartExcluding   VARCHAR(128) NOT NULL,
                versionEndExcluding     VARCHAR(128) NOT NULL,
                vulnerable              BOOL,
                FOREIGN KEY (cveId) REFERENCES cve (id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (nodeId) REFERENCES configuration_nodes (id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (cpe, versionStartIncluding, versionEndIncluding, versionStartExcluding, versionEndExcluding) REFERENCES nvd_cpe_match (cpe, versionStartIncluding, versionEndIncluding, versionStartExcluding, versionEndExcluding)
            );
            '''

create_impact = '''
            CREATE TABLE IF NOT EXISTS impact (
                id                                      SERIAL PRIMARY KEY,
                cveId                                   INTEGER,
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
                cpe23                   VARCHAR(1024) PRIMARY KEY,
                cpe23_tsv               tsvector,
                cpe22                   VARCHAR(1024),
                titles                  JSONB,
                titles_tsv              tsvector,
                references_data         JSONB,
                references_tsv          tsvector
            );
            '''

####################################### cpe match information #######################################

create_nvd_cpe_match = '''
            CREATE TABLE IF NOT EXISTS nvd_cpe_match (
                id                      SERIAL,
                cpe                     VARCHAR(1024) NOT NULL,
                versionStartIncluding   VARCHAR(128) NOT NULL,
                versionEndIncluding     VARCHAR(128) NOT NULL,
                versionStartExcluding   VARCHAR(128) NOT NULL,
                versionEndExcluding     VARCHAR(128) NOT NULL,
                PRIMARY KEY(cpe, versionStartIncluding, versionEndIncluding, versionStartExcluding, versionEndExcluding)
            );
            '''

create_nvd_cpe23 = '''
            CREATE TABLE IF NOT EXISTS nvd_cpe23 (
                cpe                     VARCHAR(1024) NOT NULL,
                versionStartIncluding   VARCHAR(128) NOT NULL,
                versionEndIncluding     VARCHAR(128) NOT NULL,
                versionStartExcluding   VARCHAR(128) NOT NULL,
                versionEndExcluding     VARCHAR(128) NOT NULL,
                cpe23                   VARCHAR(1024),
                FOREIGN KEY (cpe23) REFERENCES cpe (cpe23) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (cpe, versionStartIncluding, versionEndIncluding, versionStartExcluding, versionEndExcluding) REFERENCES nvd_cpe_match (cpe, versionStartIncluding, versionEndIncluding, versionStartExcluding, versionEndExcluding) ON DELETE CASCADE ON UPDATE CASCADE
            );
            '''
