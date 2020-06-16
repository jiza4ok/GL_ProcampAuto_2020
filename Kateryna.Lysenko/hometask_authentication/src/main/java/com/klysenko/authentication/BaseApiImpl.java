package com.klysenko.authentication;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.klysenko.authentication.dto.*;
import lombok.SneakyThrows;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.util.Base64Utils;
import org.springframework.web.client.RestTemplate;

public class BaseApiImpl implements BaseApi {

    private final String username;
    private final String password;

    private AuthResponse authResponse;

    private RestTemplate restTemplate = new RestTemplate();

    public BaseApiImpl(String username, String password) {
        this.username = username;
        this.password = password;
    }

    public void login() {
        ResponseEntity<AuthResponse> authResponseEntity = restTemplate.postForEntity(
                EndPoints.login,
                new AuthForm(username, password),
                AuthResponse.class);
        this.authResponse = authResponseEntity.getBody();
    }

    public void refresh() {
        HttpHeaders headers = new HttpHeaders();
        headers.add("Authorization", "Bearer " + authResponse.getRefreshToken());
        HttpEntity httpEntity = new HttpEntity(headers);
        ResponseEntity<RefreshResponse> refreshResponseEntity = restTemplate.exchange(EndPoints.refresh,
                HttpMethod.POST,
                httpEntity,
                RefreshResponse.class);
        authResponse.setAccessToken(refreshResponseEntity.getBody().getAccessToken());
    }

    public ItemsResponse getItems() {
        refreshTokenIfExpired();

        HttpHeaders headers = new HttpHeaders();
        headers.add("Authorization", "Bearer " + authResponse.getAccessToken());
        HttpEntity httpEntity = new HttpEntity(headers);
        ResponseEntity<ItemsResponse> itemsResponseResponseEntity = restTemplate.exchange(
                EndPoints.items,
                HttpMethod.GET,
                httpEntity,
                ItemsResponse.class);
        return itemsResponseResponseEntity.getBody();
    }

    protected void refreshTokenIfExpired() {
        JwtPayload jwtPayload = getJwtPayload();
        if (jwtPayload.getExp() < System.currentTimeMillis() / 1000) {
            refresh();
        }
    }

    @SneakyThrows
    private JwtPayload getJwtPayload() {
        String jwtPayload = authResponse.getAccessToken().split("\\.")[1];
        return new ObjectMapper().readValue(
                Base64Utils.decodeFromString(jwtPayload),
                JwtPayload.class
        );
    }
}
