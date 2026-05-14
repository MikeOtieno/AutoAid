package com.autoaid.models;

import com.google.gson.annotations.SerializedName;
import java.util.List;

public class Garage {
    public String id;
    public String name;
    @SerializedName("latitude")
    public double lat;
    @SerializedName("longitude")
    public double lng;
    public double rating;
    @SerializedName("price_range")
    public String priceRange;
    @SerializedName("specializations")
    public List<String> services;
    public String specialization;
    public String phone;
    public String address;

    public String getIdString() { return id; }
    public String getSpecializationText() {
        return services == null ? "" : String.join(", ", services);
    }
}
