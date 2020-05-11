from requests import Response


def status_code_is_2xx(response: Response) -> bool:
    """ Returns True, if the response status code is in range from 200 to 299, and False otherwise
        :param response: request.Response object
        :return :bool
    """
    return 200 <= response.status_code < 300


def status_code_is_3xx(response: Response) -> bool:
    """ Returns True, if the response status code is in range from 300 to 399, and False otherwise
        :param response: request.Response object
        :return :bool
    """
    return 300 <= response.status_code < 400


def extract_access_token(response: Response) -> str:
    """ Returns the access token taken from the response json container
        :param response: request.Response object
        :return :str
    """
    return response.json()['access_token']
