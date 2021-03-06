import json
import requests
import socket

from nautilus.conventions.services import api_gateway_name
from nautilus.network.registry import service_location_by_name

def query_graphql_service(url, name, fields, filters=None):
    """ A graphql query wrapper factory"""

    # by default there are no args to add to the query
    args = None
    # if there are filters defined for the query
    if filters:
        # construct the argument string out of the given dictionary
        arg_string = ', '.join(['{}: {}'.format(key, json.dumps(value)) \
                                            for key, value in filters.items()])
        args = "(%s)" % arg_string if len(arg_string) > 0  else ''

    # construct the field string
    field_list = ', '.join(fields)

    # build the query out of the given paramters
    query = """
        query {
            %s %s {
                %s
            }
        }
    """ % (name, args or '', field_list)

    # query the service to retrieve the data
    data_request = requests.get(url + '?query='   + query).json()
    # if there is an error
    if 'errors' in data_request:
        raise RuntimeError(data_request['errors'])
    # otherwise there is no error
    else:
        # return the data
        return data_request['data'][name]


def query_service(service, fields, filters = {}):
    '''
        Apply the given filters to a query of a model service given its name
        and the desired fields.
    '''
    # necessary imports
    from nautilus.conventions import root_query

    # query the target using model service conventions
    return query_graphql_service(
        url = 'http://{}'.format(service_location_by_name(service)),
        name = root_query(service),
        fields = fields,
        filters = filters
    )

def query_api(query, mutation = None):
    '''
        Perform the given query on the api gateway and turn the results.
        Use this function to avoid hard coding the name of the api gateway.
    '''
    # grab the location of the api service from the registry
    api_location = service_location_by_name(api_gateway_name())
    # construct the url out of the location
    url = 'http://{}'.format(api_location)
    print(url + '?query='   + query)
    # query the service to retrieve the data
    dataRequest = requests.get(url + '?query='   + query).json()


    return query_service(api_gateway_name(), query)


def combine_action_handlers(*args):
    """
        This function combines the given action handlers into a single function
        which will call all of them.
    """
    # the combined action handler
    def combinedActionHandler(action_type, payload):
        # goes over every given handler
        for handler in args:
            # call the handler
            handler(action_type, payload)

    # return the combined action handler
    return combinedActionHandler

