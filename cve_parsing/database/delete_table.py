delete_cve = '''
            DROP TABLE IF EXISTS cve;
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

delete_nvd_cpe_match = '''
            DROP TABLE IF EXISTS nvd_cpe_match;
            '''

delete_nvd_cpe23 = '''
            DROP TABLE IF EXISTS nvd_cpe23;
            '''
