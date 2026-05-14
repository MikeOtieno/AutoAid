package com.autoaid.activities;

import android.Manifest;
import android.content.Intent;
import android.location.Location;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AppCompatActivity;
import androidx.lifecycle.ViewModelProvider;

import com.autoaid.R;
import com.autoaid.adapters.GarageAdapter;
import com.autoaid.database.entities.GarageEntity;
import com.autoaid.databinding.ActivityMechanicsMapBinding;
import com.autoaid.models.Garage;
import com.autoaid.utils.Constants;
import com.autoaid.utils.LocationUtils;
import com.autoaid.viewmodel.GarageViewModel;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.gson.Gson;

import java.util.List;

public class MechanicsMapActivity extends AppCompatActivity implements OnMapReadyCallback {

    private ActivityMechanicsMapBinding binding;
    private GoogleMap map;
    private GarageViewModel vm;
    private GarageAdapter adapter;

    private double lastLat = -1.0, lastLng = 37.0;

    private final ActivityResultLauncher<String[]> locPermLauncher =
            registerForActivityResult(new ActivityResultContracts.RequestMultiplePermissions(), r -> loadLocation());

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityMechanicsMapBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        adapter = new GarageAdapter(this::openDetails);
        binding.recyclerGarages.setAdapter(adapter);

        vm = new ViewModelProvider(this).get(GarageViewModel.class);

        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager().findFragmentById(R.id.map);
        if (mapFragment != null) mapFragment.getMapAsync(this);

        binding.fabLocate.setOnClickListener(v ->
                locPermLauncher.launch(new String[]{Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION}));

        vm.cachedGarages().observe(this, garages -> {
            adapter.submitEntities(garages);
            renderMarkers(garages);
        });

        vm.loading.observe(this, l -> binding.progress.setVisibility(l ? View.VISIBLE : View.GONE));
        vm.error.observe(this, e -> { if (e != null) Toast.makeText(this, e, Toast.LENGTH_LONG).show(); });

        locPermLauncher.launch(new String[]{Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION});
    }

    @Override
    public void onMapReady(GoogleMap googleMap) {
        map = googleMap;
        moveCamera(lastLat, lastLng);
    }

    private void loadLocation() {
        try {
            LocationUtils.getLastLocation(this, new LocationUtils.LocationCallback() {
                @Override public void onLocation(Location loc) {
                    if (loc != null) { lastLat = loc.getLatitude(); lastLng = loc.getLongitude(); }
                    moveCamera(lastLat, lastLng);
                    vm.fetch(lastLat, lastLng);
                }

                @Override public void onError(Exception e) {
                    moveCamera(lastLat, lastLng);
                    vm.fetch(lastLat, lastLng);
                }
            });
        } catch (Exception e) {
            moveCamera(lastLat, lastLng);
            vm.fetch(lastLat, lastLng);
        }
    }

    private void moveCamera(double lat, double lng) {
        if (map == null) return;
        LatLng pos = new LatLng(lat, lng);
        map.moveCamera(CameraUpdateFactory.newLatLngZoom(pos, 13f));
    }

    private void renderMarkers(List<GarageEntity> garages) {
        if (map == null) return;
        map.clear();
        for (GarageEntity g : garages) {
            map.addMarker(new MarkerOptions().position(new LatLng(g.lat, g.lng)).title(g.name).snippet(g.specialization));
        }
    }

    private void openDetails(GarageEntity g) {
        Garage model = new Garage();
        model.id = g.id;
        model.name = g.name;
        model.lat = g.lat;
        model.lng = g.lng;
        model.rating = g.rating;
        model.priceRange = g.priceRange;
        model.specialization = g.specialization;
        model.phone = g.phone;
        model.address = g.address;

        Intent i = new Intent(this, MechanicDetailsActivity.class);
        i.putExtra(Constants.EXTRA_GARAGE, new Gson().toJson(model));
        startActivity(i);
    }
}
