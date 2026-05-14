package com.autoaid.activities;

import android.content.Intent;
import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;

import com.autoaid.databinding.ActivityDiagnosisResultBinding;
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

        b.btnFindMechanics.setOnClickListener(v -> startActivity(new Intent(this, MechanicsMapActivity.class)));
    }
}
