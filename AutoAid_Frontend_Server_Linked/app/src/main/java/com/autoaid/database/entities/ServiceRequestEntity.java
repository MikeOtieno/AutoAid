package com.autoaid.database.entities;

import androidx.room.Entity;
import androidx.room.PrimaryKey;

@Entity(tableName = "service_requests")
public class ServiceRequestEntity {
    @PrimaryKey(autoGenerate = true)
    public long id;

    public String garageId;
    public String garageName;
    public String vehicleType;
    public String problemSummary;
    public double lat;
    public double lng;

    public String status;
    public long createdAt;
}
