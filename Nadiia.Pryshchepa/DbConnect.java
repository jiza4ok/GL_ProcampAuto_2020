package db;

import java.sql.*;

public class DbConnect{

    final static String db_driver = "oracle.jdbc.driver.OracleDriver";
    final static String URI = "jdbc:postgresql://127.0.0.1:5432/test";
    final static String user = "user";
    final static String pwd = "123456";
    private static ThreadLocal<Connection> connectionHolder = new ThreadLocal<Connection>();


    public static Connection getDBConnection() {
        Connection connection = connectionHolder.get();
        if (connection == null) {
            try {
                Class.forName(db_driver);
            } catch (ClassNotFoundException e) {
                System.out.println(e.getMessage());
            }
            try{connection = DriverManager.getConnection(URI, user, pwd);
            connectionHolder.set(connection);}
            catch (SQLException e){
                System.out.println(e.getMessage());
            }
        }
        return connectionHolder.get();
    }

    public static void closeDBConnection(){
        Connection connection = connectionHolder.get();
        if (connection!=null){
            try{connection.close();}
            catch (SQLException e) {
                System.out.println(e.getMessage());
            }
            connectionHolder.remove();
        }
    }

    public static ResultSet executeQuery(String query) throws SQLException
    {
        Connection connection = connectionHolder.get();
        if (connection!=null)
        {
                Statement statement = connection.createStatement();
                ResultSet rs = statement.executeQuery(query);
                return rs;
        }
        return null;
    }
}
