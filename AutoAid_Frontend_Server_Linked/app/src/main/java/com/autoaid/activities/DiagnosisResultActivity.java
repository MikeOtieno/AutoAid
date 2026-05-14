package com.autoaid.activities;

import android.content.Intent;
import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;

import com.autoaid.databinding.ActivityDiagnosisResultBinding;
import com.autoaid.database.AutoAidDatabase;
import com.autoaid.database.entities.ServiceRequestEntity;
import com.autoaid.models.DiagnoseResponse;
import com.autoaid.utils.Constants;
import com.google.gson.Gson;

public class DiagnosisResultActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        ActivityDiagnosisResultBinding b = ActivityDiagnosisResultBinding.inflate(getLayoutInflater());
        setContentView(b.getRoot());

        String json = getIntent().getStringExtra(Constants.EXTRA_DIAGNOSIS);
        DiagnoseResponse r = new Gson().fromJson(json, DiagnoseResponse.class);

        b.tvProblem.setText(r.problem);
        b.tvConfidence.setText(r.confidence + "%");
        b.tvUrgency.setText(r.urgency);
        b.tvAction.setText(r.recommendedAction);

        // Save the diagnosis locally so the My Requests tab is not empty after a test diagnosis.
        new Thread(() -> {
            ServiceRequestEntity e = new ServiceRequestEntity();
            e.garageId = "";
            e.garageName = "Diagnosis result";
            e.vehicleType = "Vehicle";
            e.problemSummary = r.problem + " - " + r.urgency + " urgency";
            e.status = "Diagnosed";
            e.createdAt = System.currentTimeMillis();
            AutoAidDatabase.get(this).requestDao().insert(e);
        }).start();

        b.btnFindMechanics.setOnClickListener(v -> {
            Intent i = new Intent(this, MechanicsMapActivity.class);
            i.putExtra(Constants.EXTRA_PROBLEM_SUMMARY, r.problem);
            startActivity(i);
        });
    }
}
