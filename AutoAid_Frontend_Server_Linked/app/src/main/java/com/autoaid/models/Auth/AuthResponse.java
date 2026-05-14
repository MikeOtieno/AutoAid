package com.autoaid.models.Auth;

import com.google.gson.annotations.SerializedName;

public class AuthResponse {
    @SerializedName(value="access_token", alternate={"accessToken"})
    public String token;
    @SerializedName("token_type")
    public String tokenType;
    public User user;

    public boolean success = true;
    public String message = "OK";

    public String name;
    public String email;
    public String phone;

    public static class User {
        public int id;
        @SerializedName(value="full_name", alternate={"name"})
        public String fullName;
        public String email;
        public String phone;
        public String role;
    }

    public String getName() { return user != null ? user.fullName : name; }
    public String getEmail() { return user != null ? user.email : email; }
    public String getPhone() { return user != null ? user.phone : phone; }
}
