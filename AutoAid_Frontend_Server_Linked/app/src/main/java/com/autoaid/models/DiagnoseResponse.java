package com.autoaid.models;

import com.google.gson.annotations.SerializedName;
import java.util.List;

public class DiagnoseResponse {
    public int id;
    @SerializedName("top_fault")
    public String problem;
    @SerializedName("top_confidence")
    public Double confidenceRaw;
    public String urgency;
    public List<Object> predictions;

    public int confidence;
    public String recommendedAction;

    public void normalize() {
        if (confidenceRaw != null) {
            confidence = confidenceRaw <= 1.0 ? (int)Math.round(confidenceRaw * 100) : (int)Math.round(confidenceRaw);
        }
        if (recommendedAction == null) {
            recommendedAction = "Recommended action: visit a nearby garage for inspection.";
        }
    }
}
