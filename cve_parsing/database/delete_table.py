delete_cve = '''
            DROP TABLE IF EXISTS cve;
        '''

delete_problemtypes = '''
            DROP TABLE IF EXISTS problemtype_data;
            '''

delete_references = '''
            DROP TABLE IF EXISTS reference_data;
            '''

delete_descriptions = '''
            DROP TABLE IF EXISTS description_data;
            '''

delete_configuration_nodes = '''
            DROP TABLE IF EXISTS configuration_nodes;
            '''

delete_cpe_match = '''
            DROP TABLE IF EXISTS cpe_match;
            '''

delete_impact = '''
            DROP TABLE IF EXISTS impact;
            '''

####################################### cpe information #######################################

delete_cpe = '''
            DROP TABLE IF EXISTS cpe;
            '''

delete_cpe_titles = '''
            DROP TABLE IF EXISTS cpe_titles;
            '''

delete_cpe_references = '''
            DROP TABLE IF EXISTS cpe_references;
            '''