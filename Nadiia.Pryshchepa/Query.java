package db;
import org.springframework.jdbc.core.RowMapper;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

public class Query<T>{

    public List<T> select(String query, RowMapper<T> rowMapper) throws SQLException {
        ResultSet rs = DbConnect.executeQuery(query);
        List<T> result = new ArrayList<>();
        while(rs.next()){
            result.add(rowMapper.mapRow(rs, rs.getRow()));
        }
        return result;
    }

    public void update(String query) throws SQLException {
        Connection connection = DbConnect.getDBConnection();
        connection.createStatement().executeQuery(query);
    }
}
