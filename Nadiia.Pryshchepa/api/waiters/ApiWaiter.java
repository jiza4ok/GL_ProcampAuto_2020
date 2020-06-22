package api.waiters;

import io.restassured.response.ValidatableResponse;
import lombok.extern.slf4j.Slf4j;
import org.awaitility.Awaitility;
import org.awaitility.core.ConditionTimeoutException;

import java.util.concurrent.TimeUnit;

@Slf4j
public class ApiWaiter {
    public ValidatableResponse waitForResponse(ValidateResponseWaiter validateResponseWaiter, int responseCode) {
        final ValidatableResponse[] validatableResponse = new ValidatableResponse[1];
        try {
            Awaitility.await().atMost(100, TimeUnit.SECONDS)
                    .with()
                    .until(() -> {
                        validatableResponse[0] = validateResponseWaiter.validatableResponse();
                        return validatableResponse[0].extract().statusCode() == responseCode;
                    });
            return validatableResponse[0];
        } catch (ConditionTimeoutException e) {
            ValidatableResponse assertResponse = validateResponseWaiter.validatableResponse();
            throw new AssertionError("[ERROR::] Timeout exception with status code :  "
                    .concat(String.valueOf(assertResponse.extract().statusCode()))
                    .concat(" but expected ")
                    .concat(String.valueOf(responseCode))
                    .concat("\n[ERROR::] With error response : \n")
                    .concat(assertResponse.extract().response().asString()));
        }
    }
}