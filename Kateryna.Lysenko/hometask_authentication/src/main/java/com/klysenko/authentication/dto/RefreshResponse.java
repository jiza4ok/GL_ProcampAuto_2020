package com.klysenko.authentication.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class RefreshResponse {

    @JsonProperty("access_token")
    String accessToken;
}
