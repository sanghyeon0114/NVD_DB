insert_cve = '''
            INSERT INTO cve (
                data_type,
                data_format,
                data_version,
                CVE_data_meta_ID,
                CVE_data_meta_ASSIGNER,
                configurations_CVE_data_version,
                publishedDate,
                lastModifiedDate
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            '''

insert_problemtype_data = '''
            INSERT INTO problemtype_data (
                cveId,
                lang,
                value
            ) VALUES (%s, %s, %s)
            '''

insert_reference_data = '''
            INSERT INTO reference_data (
                cveId,
                url,
                name,
                refsource,
                tag
            ) VALUES (%s, %s, %s, %s, %s)
            '''

insert_description_data = '''
            INSERT INTO description_data (
                cveId,
                lang,
                value
            ) VALUES (%s, %s, %s)
            '''
