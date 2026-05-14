package com.autoaid.repository;

import android.content.Context;

import androidx.lifecycle.LiveData;

import com.autoaid.database.AutoAidDatabase;
import com.autoaid.database.entities.ServiceRequestEntity;
import com.autoaid.models.ApiResponse;
import com.autoaid.models.ServiceRequestPayload;
import com.autoaid.network.ApiClient;
import com.autoaid.network.NetworkResult;

import retrofit2.Response;

public class RequestRepository {

    public LiveData<java.util.List<ServiceRequestEntity>> observeRequests(Context ctx) {
        return AutoAidDatabase.get(ctx).requestDao().observeAll();
    }

    public NetworkResult<ApiResponse> submit(Context ctx, ServiceRequestPayload payload, String garageName) {
        try {
            Response<ApiResponse> r = ApiClient.api(ctx).requestMechanic(payload).execute();
            if (r.isSuccessful()) {
                cache(ctx, payload, garageName);
                ApiResponse ok = new ApiResponse();
                ok.success = true;
                ok.message = "Booking submitted successfully";
                return NetworkResult.ok(ok);
            }
            return NetworkResult.fail("Request failed");
        } catch (Exception e) {
            return NetworkResult.fail("Request error: " + e.getMessage());
        }
    }

    private void cache(Context ctx, ServiceRequestPayload payload, String garageName) {
        new Thread(() -> {
            ServiceRequestEntity e = new ServiceRequestEntity();
            e.garageId = String.valueOf(payload.garageId);
            e.garageName = garageName;
            e.vehicleType = payload.vehicleType;
            e.problemSummary = payload.problemSummary;
            e.lat = payload.lat;
            e.lng = payload.lng;
            e.status = "Submitted";
            e.createdAt = System.currentTimeMillis();
            AutoAidDatabase.get(ctx).requestDao().insert(e);
        }).start();
    }
}
