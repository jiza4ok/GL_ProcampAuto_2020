package api.requests;

import api.Resourses;
import api.base_requests.Post;
import api.objects.UserSession;
import io.restassured.response.Response;

public class Requests {
    public Response login(String login, String password) {
        String endpoint = Resourses.getLogin_endpoint();
        String body = "{\"login\":\"" + login + "\", \"password\":" + password + "\"";
        return new Post().withoutAuth(200, endpoint, body);
    }

    public Response refreshAccess(UserSession session) {
        String endpoint = Resourses.getAccess_token_endpoint();
        String body = "{\"session_id\":\""
                + session.getSession_id()
                + "\", \"grant_type\": \"refresh_token\", \"refresh_token\":"
                + session.getRefresh_token() + "\"";
        return new Post().withToken(session.getAccess_token(), 200, endpoint, body);
    }
}
