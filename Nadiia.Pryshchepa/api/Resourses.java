package api;

import lombok.Getter;

import java.sql.Driver;

public class Resourses {
    @Getter
    private static final String base_url = "base_url";
    @Getter
    private static final String login_endpoint = "/login";
    @Getter
    private static final String access_token_endpoint = "/oauth2/access_token";
}
