get_last_cve_id = '''
            SELECT MAX(id) as maxId FROM cve;
            '''

get_last_node_id = '''
            SELECT MAX(id) as maxId FROM configuration_nodes;
            '''
