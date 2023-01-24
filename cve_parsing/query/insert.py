insert_cve = '''
            INSERT INTO `cve` (
                `data_type`,
                `data_format`,
                `data_version`,
                `CVE_data_meta_ID`,
                `CVE_data_meta_ASSIGNER`,
                `configurations_CVE_data_version`,
                `publishedDate`,
                `lastModifiedDate`
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            '''

insert_problemtypes = '''
            INSERT INTO `problemtypes` (
                `cveId`,
                `lang`,
                `value`
            ) VALUES (%s, %s, %s)
            '''

insert_references = '''
            INSERT INTO `references` (
                `cveId`,
                `url`,
                `name`,
                `refsource`
            ) VALUES (%s, %s, %s)
            '''