import pytest
import allure
from requests import HTTPError
from ..utils import api, helpers, launchers
from ..testdata import testdata
from ..config import local_link_to_server

# NB! Run Pytest from the "Lecture_Pytest" folder


@pytest.fixture(scope='session')
def session_fixture():
    """ SETUP: runs the test server at the start of the session
        TEARDOWN: stops it as the session concludes
    """
    server = launchers.start_server(local_link_to_server)
    yield
    api.delete_all_resources()
    launchers.stop_server(server)


@pytest.fixture(params=testdata.correct_credentials)
def authorization_fixture(request):
    """
        SETUP for tests requiring preliminary authorization with an access token.
        Authorizes at a server, yields access token to the tests or fixtures related
    """
    access_token, server_response = api.jwt_authorize(request.param['user_name'], request.param['password'])
    assert helpers.status_code_is_2xx(server_response)
    yield access_token


@pytest.fixture
def resource_creation_fixture(authorization_fixture):
    """
        SETUP for tests requiring preliminary creation of a resource.
        Uses authorization_fixture for getting an access token.
        Yields resource ID, the resource created as a json, and the access token to the tests related
    """
    access_token, resource = authorization_fixture, testdata.resource
    resource_id, server_response = api.create_resource(access_token, resource)
    assert helpers.status_code_is_2xx(server_response)
    yield resource_id, resource, access_token


@allure.title('Authorization with correct credentials')
@pytest.mark.smoke
@pytest.mark.parametrize('credentials', testdata.correct_credentials)
def test_authorization(session_fixture, credentials):
    """ Verifies authorization with correct credentials """
    access_token, server_response = api.jwt_authorize(credentials['user_name'], credentials['password'])
    assert helpers.status_code_is_2xx(server_response)


@allure.title('Creation of the resource')
def test_resource_creation(session_fixture, authorization_fixture):
    """ Verifies that a resource can be created given a proper token obtained after authorization """
    access_token = authorization_fixture
    resource_id, server_response = api.create_resource(access_token, testdata.resource)
    assert helpers.status_code_is_2xx(server_response)


@allure.title('Reading of the resource by ID')
def test_resource_reading(session_fixture, resource_creation_fixture):
    """ Verifies that a resource can be read by its ID given a proper token obtained after authorization """
    resource_id, created_resource, access_token = resource_creation_fixture
    resource_content, server_response = api.read_resource(access_token, resource_id)
    assert helpers.status_code_is_2xx(server_response)
    assert resource_content == created_resource


@allure.title('Deletion of the resource ID')
def test_resource_deletion(session_fixture, resource_creation_fixture):
    """ Verifies a resource can be deleted by its ID given a proper token obtained after authorization """
    resource_id, created_resource, access_token = resource_creation_fixture
    server_response = api.delete_resource(access_token, resource_id)
    assert helpers.status_code_is_2xx(server_response)
    with pytest.raises(HTTPError):
        server_response = api.delete_resource(access_token, resource_id)
        server_response.raise_for_status()


@allure.title('Authorization with wrong credentials')
@pytest.mark.parametrize('credentials', testdata.incorrect_credentials)
def test_authorization_with_wrong_credentials(session_fixture, credentials):
    """ Verifies impossibility to receive an access token and authorize with incorrect credentials """
    access_token, server_response = api.jwt_authorize(credentials['user_name'], credentials['password'])
    assert access_token is None
    with pytest.raises(HTTPError):
        server_response.raise_for_status()


@allure.title('Creation of the resource with no token')
@pytest.mark.parametrize('token', testdata.empty_tokens)
def test_resource_creation_with_bad_token(session_fixture, token):
    """ Verifies impossibility to create a resource with no or an empty access token """
    resource_id, server_response = api.create_resource(token, testdata.resource)
    with pytest.raises(HTTPError):
        server_response.raise_for_status()
