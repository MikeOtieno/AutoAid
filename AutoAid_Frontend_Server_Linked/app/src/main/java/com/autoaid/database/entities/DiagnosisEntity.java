package com.autoaid.database.entities;

import androidx.room.Entity;
import androidx.room.PrimaryKey;

@Entity(tableName = "diagnoses")
public class DiagnosisEntity {
    @PrimaryKey(autoGenerate = true)
    public long id;

    public String description;
    public String problem;
    public int confidence;
    public String urgency;
    public String recommendedAction;
    public long createdAt;
}
