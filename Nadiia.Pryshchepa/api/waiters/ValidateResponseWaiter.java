package api.waiters;

import io.restassured.response.ValidatableResponse;

public interface ValidateResponseWaiter {
    ValidatableResponse validatableResponse();
}
