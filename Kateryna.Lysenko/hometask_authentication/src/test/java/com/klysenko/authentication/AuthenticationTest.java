package com.klysenko.authentication;

import com.klysenko.authentication.dto.ItemsResponse;
import org.junit.Test;
import org.springframework.web.client.RestTemplate;

import static java.lang.Thread.sleep;
import static org.junit.Assert.assertNotNull;

public class AuthenticationTest {

    RestTemplate restTemplate = new RestTemplate();
    private BaseApi baseApi = new BaseApiImpl("test", "test");

    @Test
    public void shouldGetItemsWithValidAccessToken() {
        baseApi.login();

        ItemsResponse items = baseApi.getItems();

        assertNotNull(items);
    }

    @Test
    public void shouldRefreshTokenAndGetItems() throws InterruptedException {
        baseApi.login();
        sleep(2 * 60 * 1000);

        ItemsResponse items = baseApi.getItems();

        assertNotNull(items);
    }
}
