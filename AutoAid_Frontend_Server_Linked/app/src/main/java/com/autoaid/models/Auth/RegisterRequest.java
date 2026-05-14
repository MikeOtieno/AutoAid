package com.autoaid.models.Auth;

import com.google.gson.annotations.SerializedName;

public class RegisterRequest {
    @SerializedName("full_name")
    public String fullName;
    public String email;
    public String phone;
    public String password;

    public RegisterRequest(String name, String email, String phone, String password) {
        this.fullName = name;
        this.email = email;
        this.phone = phone;
        this.password = password;
    }
}
