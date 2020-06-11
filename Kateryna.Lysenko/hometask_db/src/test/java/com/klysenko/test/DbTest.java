package com.klysenko.test;

import com.klysenko.db.DbClient;
import com.klysenko.test.entity.Ebook;
import com.klysenko.test.mapper.EbookRowMapper;
import lombok.SneakyThrows;
import org.junit.*;

import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

public class DbTest {

    static DbClient dbClient;

    @SneakyThrows
    @BeforeClass
    public static void initConnection() {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
        dbClient = new DbClient();
        Properties properties = new Properties();
        InputStream configInputStream = DbTest.class.getClassLoader()
                .getResourceAsStream("config.properties");
        properties.load(configInputStream);
        String url = properties.getProperty("db.url");
        String username = properties.getProperty("db.username");
        String password = properties.getProperty("db.password");
        dbClient.initConnection(url, username, password);
    }


    @Before
    public void createNewTestRow() {
        /*insert into books values (1001, 'Java', 'Tan Ah Teck', 11.11, 11);*/
        String updateQuery = "insert into books values (?, ?, ?, ?, ?)";
        dbClient.update(updateQuery, 10012, "Java", "Tan Ah Teck", 11.11, 11);
    }

    @Test
    public void shouldSelectById() {
        String selectQuery = "Select * from books where id=?";
        List<Ebook> actualList = dbClient.select(selectQuery, new EbookRowMapper(), 10012);
        actualList.forEach(System.out::println);

        List<Ebook> expected = new ArrayList<>();
        expected.add(new Ebook(10012, "Java", "Tan Ah Teck", 11.11f, 11));

        Assert.assertEquals("Actual row in the table is not te same as expected", actualList, expected);
    }

    @Test
    public void shouldUpdateById() {
        String updateQuery = "update books set title = 'Test Java' where id = ?";
        dbClient.update(updateQuery, 10012);

        String selectQuery = "Select * from books where id=?";
        List<Ebook> actualList = dbClient.select(selectQuery, new EbookRowMapper(), 10012);
        List<Ebook> expected = new ArrayList<>();
        expected.add(new Ebook(10012, "Test Java", "Tan Ah Teck", (float) 11.11, 11));

        Assert.assertEquals("Actual row in the table is not the same as expected", actualList, expected);
    }

    @After
    public void deleteTestRow() {
        String updateQuery = "DELETE FROM books WHERE id=?";
        dbClient.update(updateQuery, 10012);
    }

    @AfterClass
    public static void closeConnection() {
        dbClient.closeConnection();
    }

}