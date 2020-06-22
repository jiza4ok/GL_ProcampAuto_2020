//POST base_url/login
//body {"login": "user"
//"password": "password"}
//status code 200
//body {"session_id": "xxxxxxxxxxxx",
//"access_token": "AYjcyMzY3ZDhiNmJNTY",
//"refresh_token": "RjY2NjM5NzA2OWJjuE7c",
//"expires": 3600}

//POST /oauth2/access_token
//body {"session_id": "xxxxxxxxxxxx"
//"refresh_token": "xxxxx"}
//status code 200
//body {"access_token": "AYjcyMzY3ZDhiNmJkNTY",
//"refresh_token": "RjY2NjM5NzA2OWJjuE7c",
//"token_type": "bearer",
//"expires": 3600}


package api.objects;

import io.restassured.response.Response;
import lombok.Data;
import org.json.JSONObject;


import java.util.Date;

@Data
public class UserSession {
    String session_id;
    String access_token;
    String refresh_token;
    private ThreadLocal<Date> accessTokenExpirationTime = new ThreadLocal<Date>();


    public Boolean isExpired() {
        Date date = accessTokenExpirationTime.get();
        return date.after(new Date());
    }

    public static UserSession createSession(Response successResponse) {
        JSONObject jsonObject = new JSONObject(successResponse.toString());
        UserSession session = new UserSession();
        session.setSession_id(jsonObject.getString("session_id"));
        session.setAccess_token(jsonObject.getString("access_token"));
        session.setRefresh_token(jsonObject.getString("refresh_token"));
        session.accessTokenExpirationTime.set(new Date(System.currentTimeMillis() + jsonObject.getInt("expires")));
        return session;
    }

    public void refresh(Response successResponse) {
        JSONObject jsonObject = new JSONObject(successResponse.toString());
        this.setAccess_token(jsonObject.getString("access_token"));
        this.setRefresh_token(jsonObject.getString("refresh_token"));
        this.accessTokenExpirationTime.set(new Date(System.currentTimeMillis() + jsonObject.getInt("expires")));
    }

}
