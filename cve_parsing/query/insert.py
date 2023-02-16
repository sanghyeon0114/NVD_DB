insert_configuration_nodes = '''
            INSERT INTO configuration_nodes (
                cveId,
                operator,
                parentId
            ) VALUES (%s, %s, %s)
            '''

insert_cpe_match = '''
            INSERT INTO cpe_match (
                cveId,
                nodeId,
                vulnerable,
                cpe23Uri,
                versionStartIncluding,
                versionEndIncluding,
                versionStartExcluding,
                versionEndExcluding,
                cpe_name
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''

insert_impact = '''
            INSERT INTO impact (
                cveId,
                baseMetricV3_cvssV3_version,
                baseMetricV3_cvssV3_vectorString,
                baseMetricV3_cvssV3_baseScore,
                baseMetricV3_cvssV3_baseSeverity,
                baseMetricV3_exploitabilityScore,
                baseMetricV3_impactScore,
                baseMetricV2_cvssV2_version,
                baseMetricV2_cvssV2_vectorString,
                baseMetricV2_cvssV2_baseScore,
                baseMetricV2_severity,
                baseMetricV2_exploitabilityScore,
                baseMetricV2_impactScore,
                baseMetricV2_acInsufInfo,
                baseMetricV2_obtainAllPrivilege,
                baseMetricV2_obtainUserPrivilege,
                baseMetricV2_obtainOtherPrivilege,
                baseMetricV2_userInteractionRequired
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''

insert_cpe = '''
            INSERT INTO cpe (
                cpe22,
                cpe23
            ) VALUES (%s, %s)
            '''

insert_cpe_titles = '''
            INSERT INTO cpe_titles (
                cpeId,
                value,
                lang
            ) VALUES (%s, %s, %s)
            '''

insert_cpe_references = '''
            INSERT INTO cpe_references (
                cpeId,
                type,
                uri
            ) VALUES (%s, %s, %s)
            '''

insert_nvd_cpe_match = '''
            INSERT INTO nvd_cpe_match (
                cpe23Uri,
                versionStartIncluding,
                versionEndIncluding,
                versionStartExcluding,
                versionEndExcluding,
                cpe_name
            ) VALUES (%s, %s, %s, %s, %s, %s)
            '''
