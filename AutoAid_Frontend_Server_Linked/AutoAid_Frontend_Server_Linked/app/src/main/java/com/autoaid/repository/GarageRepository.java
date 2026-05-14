package com.autoaid.repository;

import android.content.Context;

import androidx.lifecycle.LiveData;

import com.autoaid.database.AutoAidDatabase;
import com.autoaid.database.entities.GarageEntity;
import com.autoaid.models.Garage;
import com.autoaid.network.ApiClient;
import com.autoaid.network.NetworkResult;

import java.util.ArrayList;
import java.util.List;

import retrofit2.Response;

public class GarageRepository {

    public LiveData<List<GarageEntity>> observeCached(Context ctx) {
        return AutoAidDatabase.get(ctx).garageDao().observeAll();
    }

    public NetworkResult<List<Garage>> fetchNearby(Context ctx, double lat, double lng) {
        try {
            Response<List<Garage>> r = ApiClient.api(ctx).garagesNearby(lat, lng, 50.0).execute();
            if (r.isSuccessful() && r.body() != null) {
                cache(ctx, r.body());
                return NetworkResult.ok(r.body());
            }
            return NetworkResult.fail("Garages fetch failed");
        } catch (Exception e) {
            return NetworkResult.fail("Garages error: " + e.getMessage());
        }
    }

    private void cache(Context ctx, List<Garage> garages) {
        new Thread(() -> {
            List<GarageEntity> entities = new ArrayList<>();
            for (Garage g : garages) {
                GarageEntity e = new GarageEntity();
                e.id = g.getIdString();
                e.name = g.name;
                e.lat = g.lat;
                e.lng = g.lng;
                e.rating = g.rating;
                e.priceRange = g.priceRange;
                e.specialization = g.getSpecializationText();
                e.phone = g.phone;
                e.address = g.address;
                entities.add(e);
            }
            AutoAidDatabase.get(ctx).garageDao().upsertAll(entities);
        }).start();
    }
}
