package com.autoaid.network;

import com.autoaid.models.ApiResponse;
import com.autoaid.models.DiagnoseRequest;
import com.autoaid.models.DiagnoseResponse;
import com.autoaid.models.Garage;
import com.autoaid.models.ServiceRequestPayload;
import com.autoaid.models.Auth.AuthResponse;
import com.autoaid.models.Auth.LoginRequest;
import com.autoaid.models.Auth.RegisterRequest;

import java.util.List;

import retrofit2.Call;
import okhttp3.RequestBody;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.Multipart;
import retrofit2.http.POST;
import retrofit2.http.Part;
import retrofit2.http.Query;

public interface ApiService {

    @POST("auth/login")
    Call<AuthResponse> login(@Body LoginRequest req);

    @POST("auth/register")
    Call<AuthResponse> register(@Body RegisterRequest req);

    @Multipart
    @POST("diagnostics/")
    Call<DiagnoseResponse> diagnose(@Part("text_description") RequestBody textDescription);

    @GET("garages/nearby")
    Call<List<Garage>> garagesNearby(@Query("lat") double lat, @Query("lon") double lng, @Query("radius_km") double radiusKm);

    @POST("bookings/")
    Call<ApiResponse> requestMechanic(@Body ServiceRequestPayload req);
}
