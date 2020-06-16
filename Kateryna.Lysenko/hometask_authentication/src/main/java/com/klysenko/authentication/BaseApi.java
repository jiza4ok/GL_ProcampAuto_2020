package com.klysenko.authentication;

import com.klysenko.authentication.dto.ItemsResponse;

public interface BaseApi {
    void login();
    void refresh();
    ItemsResponse getItems();
}
