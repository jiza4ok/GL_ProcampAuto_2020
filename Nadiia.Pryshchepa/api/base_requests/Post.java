package api.base_requests;

import api.Resourses;
import api.waiters.ApiWaiter;
import api.waiters.ValidateResponseWaiter;
import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import io.restassured.response.Response;
import io.restassured.response.ValidatableResponse;
import lombok.extern.slf4j.Slf4j;

import static io.restassured.RestAssured.given;
import static org.assertj.core.api.Assertions.assertThat;

@Slf4j
public class Post {

    public Response withoutAuth(int responseCode, String endpoint, String body) {
        RestAssured.baseURI = Resourses.getBase_url();
        ValidateResponseWaiter responseWaiter = () -> {
            return given()
                    .relaxedHTTPSValidation()
                    .header("Content-Type", "application/json")
                    .header("Accept", "application/json")
                    .body(body)
                    .when()
                    .post(endpoint)
                    .then()
                    .statusCode(responseCode);
        };
        return WaitResponse.validate(responseWaiter, responseCode);
    }

    public Response withToken(String token, int responseCode, String endpoint, String body) {
        ValidateResponseWaiter responseWaiter = () -> {
            RestAssured.baseURI = Resourses.getBase_url();
            return given()
                    .relaxedHTTPSValidation()
                    .auth().oauth2(token)
                    .header("Content-Type", "application/json")
                    .header("Accept", "application/json")
                    .body(body)
                    .when()
                    .get(endpoint)
                    .then()
                    .statusCode(responseCode);
        };
        return WaitResponse.validate(responseWaiter, responseCode);
    }
}
