import os

from .create import *
from .insert import *
from .select import *


class Query:

    # static field
    create_cve: str = None
    create_problemtypes: str = None
    create_references: str = None
    create_descriptions: str = None
    create_configuration_nodes: str = None
    create_cpe_match: str = None
    create_cpe_metadata: str = None
    create_cpe_name: str = None
    create_impact: str = None

    insert_cve: str = None
    insert_problemtypes: str = None

    get_last_cve_id: str = None

    @staticmethod
    def loadQuery():
        Query.create_cve = create_cve
        Query.create_problemtypes = create_problemtypes
        Query.create_references = create_references
        Query.create_descriptions = create_descriptions
        Query.create_configuration_nodes = create_configuration_nodes
        Query.create_cpe_match = create_cpe_match
        Query.create_cpe_metadata = create_cpe_metadata
        Query.create_cpe_name = create_cpe_name
        Query.create_impact = create_impact

        Query.insert_cve = insert_cve
        Query.insert_problemtypes = insert_problemtypes

        Query.get_last_cve_id = get_last_cve_id
