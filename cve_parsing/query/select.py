get_last_cve_id = '''
            SELECT MAX(id) as maxId FROM `cve`;
            '''