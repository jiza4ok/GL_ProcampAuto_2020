package com.klysenko.db;

import lombok.SneakyThrows;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class DbClient<T> {

    private Connection connection;

    @SneakyThrows
    public void initConnection(String url, String username, String password) {

        if (connection == null) {
            connection = DriverManager.getConnection(url, username, password);
        }
    }

    @SneakyThrows
    public void closeConnection() {
        connection.close();
    }

    @SneakyThrows
    public List<T> select(String query, RowMapper<T> rowMapper, Object... params) {

        List<T> result = new ArrayList<>();
        try (PreparedStatement stmt = connection.prepareStatement(query)) {

            populateParameters(stmt, params);
            ResultSet resultSet = stmt.executeQuery();

            while (resultSet.next()) {
                result.add(rowMapper.mapRow(resultSet));
            }
        }
        return result;
    }

    @SneakyThrows
    public void update(String query, Object... params) {
        try (PreparedStatement stmt = connection.prepareStatement(query)) {

            populateParameters(stmt, params);
            stmt.execute();
        }

    }

    private void populateParameters(PreparedStatement stmt, Object[] params) throws SQLException {
        for (int i = 0; i < params.length; i++) {
            stmt.setObject(i + 1, params[i]);
        }
    }
}