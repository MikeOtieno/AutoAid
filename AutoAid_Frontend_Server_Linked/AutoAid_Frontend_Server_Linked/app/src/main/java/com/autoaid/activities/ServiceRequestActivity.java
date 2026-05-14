package com.autoaid.activities;

import android.Manifest;
import android.location.Location;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AppCompatActivity;
import androidx.lifecycle.ViewModelProvider;

import com.autoaid.databinding.ActivityServiceRequestBinding;
import com.autoaid.models.Garage;
import com.autoaid.models.ServiceRequestPayload;
import com.autoaid.utils.Constants;
import com.autoaid.utils.LocationUtils;
import com.autoaid.viewmodel.RequestViewModel;
import com.google.gson.Gson;

public class ServiceRequestActivity extends AppCompatActivity {

    private ActivityServiceRequestBinding b;
    private RequestViewModel vm;
    private Garage garage;
    private double lat = -1.0, lng = 37.0;

    private final ActivityResultLauncher<String[]> locPermLauncher =
            registerForActivityResult(new ActivityResultContracts.RequestMultiplePermissions(), r -> loadLocation());

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        b = ActivityServiceRequestBinding.inflate(getLayoutInflater());
        setContentView(b.getRoot());

        vm = new ViewModelProvider(this).get(RequestViewModel.class);

        garage = new Gson().fromJson(getIntent().getStringExtra(Constants.EXTRA_GARAGE), Garage.class);
        b.tvGarageName.setText(garage.name);

        String maybeSummary = getIntent().getStringExtra(Constants.EXTRA_PROBLEM_SUMMARY);
        if (maybeSummary != null) b.etProblemSummary.setText(maybeSummary);

        b.btnSubmit.setOnClickListener(v -> submit());

        vm.loading.observe(this, l -> b.progress.setVisibility(l ? View.VISIBLE : View.GONE));
        vm.error.observe(this, e -> { if (e != null) Toast.makeText(this, e, Toast.LENGTH_LONG).show(); });
        vm.submitted.observe(this, r -> {
            if (r != null && r.success) {
                Toast.makeText(this, "Request submitted successfully.", Toast.LENGTH_LONG).show();
                finish();
            } else {
                Toast.makeText(this, r != null ? r.message : "Request failed", Toast.LENGTH_LONG).show();
            }
        });

        locPermLauncher.launch(new String[]{Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION});
    }

    private void loadLocation() {
        LocationUtils.getLastLocation(this, new LocationUtils.LocationCallback() {
            @Override public void onLocation(Location loc) {
                if (loc != null) { lat = loc.getLatitude(); lng = loc.getLongitude(); }
                b.tvLocation.setText(lat + ", " + lng);
            }

            @Override public void onError(Exception e) {
                b.tvLocation.setText(lat + ", " + lng);
            }
        });
    }

    private void submit() {
        String vehicleType = b.etVehicleType.getText().toString().trim();
        String summary = b.etProblemSummary.getText().toString().trim();
        if (vehicleType.isEmpty()) { b.etVehicleType.setError("Required"); return; }
        if (summary.isEmpty()) { b.etProblemSummary.setError("Required"); return; }

        ServiceRequestPayload payload = new ServiceRequestPayload(vehicleType, summary, lat, lng, Integer.parseInt(garage.id));
        vm.submit(payload, garage.name);
    }
}
