package api.base_requests;

import api.waiters.ApiWaiter;
import api.waiters.ValidateResponseWaiter;
import io.restassured.http.ContentType;
import io.restassured.response.Response;
import io.restassured.response.ValidatableResponse;
import lombok.extern.slf4j.Slf4j;

import static org.assertj.core.api.Assertions.assertThat;

@Slf4j
public class WaitResponse {

    static Response validate(ValidateResponseWaiter responseWaiter, int responseCode) {
        ApiWaiter apiWaiter = new ApiWaiter();
        ValidatableResponse validatableResponse = apiWaiter.waitForResponse(responseWaiter, responseCode);
        Response resp = validatableResponse.contentType(ContentType.JSON).extract().response();
        log.info("Response returned - {}", resp.asString());
        assertThat(resp.getStatusCode()).as("Response error occurred - {}", resp.getStatusLine()).isEqualTo(responseCode);
        log.info("{} return successfully ", resp.getStatusCode());
        return resp;
    }
}
