package com.autoaid.database.entities;

import androidx.room.Entity;
import androidx.room.PrimaryKey;
import androidx.annotation.NonNull;

@Entity(tableName = "garages")
public class GarageEntity {
    @PrimaryKey
    @NonNull
    public String id;

    public String name;
    public double lat;
    public double lng;
    public double rating;
    public String priceRange;
    public String specialization;

    public String phone;
    public String address;
}
