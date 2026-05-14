package com.autoaid.repository;

import android.content.Context;

import com.autoaid.database.AutoAidDatabase;
import com.autoaid.database.entities.DiagnosisEntity;
import com.autoaid.models.DiagnoseRequest;
import com.autoaid.models.DiagnoseResponse;
import com.autoaid.network.ApiClient;
import com.autoaid.network.NetworkResult;

import okhttp3.MediaType;
import okhttp3.RequestBody;
import retrofit2.Response;

public class DiagnoseRepository {

    public NetworkResult<DiagnoseResponse> diagnose(Context ctx, DiagnoseRequest req) {
        try {
            RequestBody desc = RequestBody.create(req.description, MediaType.parse("text/plain"));
            Response<DiagnoseResponse> r = ApiClient.api(ctx).diagnose(desc).execute();
            if (r.isSuccessful() && r.body() != null) {
                r.body().normalize();
                cache(ctx, req.description, r.body());
                return NetworkResult.ok(r.body());
            }
            return NetworkResult.fail("Diagnosis failed");
        } catch (Exception e) {
            return NetworkResult.fail("Diagnosis error: " + e.getMessage());
        }
    }

    private void cache(Context ctx, String description, DiagnoseResponse res) {
        new Thread(() -> {
            DiagnosisEntity e = new DiagnosisEntity();
            e.description = description;
            e.problem = res.problem;
            e.confidence = res.confidence;
            e.urgency = res.urgency;
            e.recommendedAction = res.recommendedAction;
            e.createdAt = System.currentTimeMillis();
            AutoAidDatabase.get(ctx).diagnosisDao().insert(e);
        }).start();
    }
}
