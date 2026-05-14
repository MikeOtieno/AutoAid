package com.autoaid.models;

import com.google.gson.annotations.SerializedName;

public class ServiceRequestPayload {
    public String vehicleType;
    public String problemSummary;
    public double lat;
    public double lng;

    @SerializedName("garage_id")
    public int garageId;
    @SerializedName("service_type")
    public String serviceType = "garage_visit";
    public String notes;
    @SerializedName("user_latitude")
    public double userLatitude;
    @SerializedName("user_longitude")
    public double userLongitude;

    public ServiceRequestPayload(String vehicleType, String problemSummary, double lat, double lng, int garageId) {
        this.vehicleType = vehicleType;
        this.problemSummary = problemSummary;
        this.lat = lat;
        this.lng = lng;
        this.garageId = garageId;
        this.userLatitude = lat;
        this.userLongitude = lng;
        this.notes = vehicleType + ": " + problemSummary;
    }
}
