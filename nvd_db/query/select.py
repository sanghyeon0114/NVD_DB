get_cve_id = '''
            SELECT id FROM cve WHERE CVE_data_meta_ID = %s;
            '''

get_cpe_id = '''
            SELECT id FROM cpe WHERE cpe23 = %s;
            '''

get_last_cve_id = '''
            SELECT MAX(id) as maxId FROM cve;
            '''

get_last_node_id = '''
            SELECT MAX(id) as maxId FROM configuration_nodes;
            '''

get_last_cpe_id = '''
            SELECT MAX(id) as maxId FROM cpe;
            '''

get_last_nvd_cpe_match_id = '''
            SELECT MAX(id) as maxId FROM nvd_cpe_match;
            '''

get_cve_count = '''
            SELECT COUNT(*) as cnt FROM cve;
            '''

get_cpe_count = '''
            SELECT COUNT(*) as cnt FROM cpe;
            '''

get_nvd_cpe_match_count = '''
            SELECT COUNT(*) as cnt FROM nvd_cpe_match;
            '''

get_nvd_cpe_match = '''
            SELECT id FROM nvd_cpe_match WHERE cpe23Uri = %s AND versionStartIncluding {} AND versionEndIncluding {} AND versionStartExcluding {} AND versionEndExcluding {};
            '''
