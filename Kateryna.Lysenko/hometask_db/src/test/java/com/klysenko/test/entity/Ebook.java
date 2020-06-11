package com.klysenko.test.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@AllArgsConstructor
@NoArgsConstructor
@Data
public class Ebook {

    private int id;

    private String title;

    private String author;

    private float price;

    private int qty;
}
