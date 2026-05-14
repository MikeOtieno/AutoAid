package com.autoaid.repository;

import android.content.Context;

import com.autoaid.models.Auth.AuthResponse;
import com.autoaid.models.Auth.LoginRequest;
import com.autoaid.models.Auth.RegisterRequest;
import com.autoaid.network.ApiClient;
import com.autoaid.network.NetworkResult;

import retrofit2.Response;

public class AuthRepository {

    public NetworkResult<AuthResponse> login(Context ctx, String email, String password) {
        try {
            Response<AuthResponse> r = ApiClient.api(ctx).login(new LoginRequest(email, password)).execute();
            if (r.isSuccessful() && r.body() != null) return NetworkResult.ok(r.body());
            return NetworkResult.fail("Login failed");
        } catch (Exception e) {
            return NetworkResult.fail("Login error: " + e.getMessage());
        }
    }

    public NetworkResult<AuthResponse> register(Context ctx, String name, String email, String phone, String password) {
        try {
            Response<AuthResponse> r = ApiClient.api(ctx).register(new RegisterRequest(name, email, phone, password)).execute();
            if (r.isSuccessful() && r.body() != null) return NetworkResult.ok(r.body());
            return NetworkResult.fail("Register failed");
        } catch (Exception e) {
            return NetworkResult.fail("Register error: " + e.getMessage());
        }
    }
}
