package com.klysenko.test.mapper;

import com.klysenko.db.RowMapper;
import com.klysenko.test.entity.Ebook;

import java.sql.ResultSet;
import java.sql.SQLException;

public class EbookRowMapper implements RowMapper <Ebook>{


    @Override
    public Ebook mapRow(ResultSet resultSet) throws SQLException {
        Ebook ebook = new Ebook();
        ebook.setId(resultSet.getInt("id"));
        ebook.setAuthor(resultSet.getString("author"));
        ebook.setTitle(resultSet.getString("title"));
        ebook.setPrice(resultSet.getFloat("price"));
        ebook.setQty(resultSet.getInt("qty"));
        return ebook;
    }
}
