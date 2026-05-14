package com.autoaid.utils;

import android.annotation.SuppressLint;
import android.content.Context;

import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationServices;

public class LocationUtils {

    public static FusedLocationProviderClient fusedClient(Context ctx) {
        return LocationServices.getFusedLocationProviderClient(ctx);
    }

    @SuppressLint("MissingPermission")
    public static void getLastLocation(Context ctx, LocationCallback cb) {
        fusedClient(ctx).getLastLocation()
                .addOnSuccessListener(cb::onLocation)
                .addOnFailureListener(cb::onError);
    }

    public interface LocationCallback {
        void onLocation(android.location.Location loc);
        void onError(Exception e);
    }
}
