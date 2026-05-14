package com.autoaid.activities;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;

import com.autoaid.databinding.ActivityMechanicDetailsBinding;
import com.autoaid.models.Garage;
import com.autoaid.utils.Constants;
import com.google.gson.Gson;

public class MechanicDetailsActivity extends AppCompatActivity {

    private Garage garage;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        ActivityMechanicDetailsBinding b = ActivityMechanicDetailsBinding.inflate(getLayoutInflater());
        setContentView(b.getRoot());

        garage = new Gson().fromJson(getIntent().getStringExtra(Constants.EXTRA_GARAGE), Garage.class);

        b.tvName.setText(garage.name);
        b.tvAddress.setText(garage.address);
        b.tvPhone.setText(garage.phone);
        b.tvRating.setText(String.valueOf(garage.rating));
        b.tvPrice.setText(garage.priceRange);
        b.tvSpec.setText(garage.specialization);

        b.btnCall.setOnClickListener(v -> startActivity(new Intent(Intent.ACTION_DIAL, Uri.parse("tel:" + garage.phone))));

        b.btnRequestMechanic.setOnClickListener(v -> {
            Intent i = new Intent(this, ServiceRequestActivity.class);
            i.putExtra(Constants.EXTRA_GARAGE, new Gson().toJson(garage));
            startActivity(i);
        });

        b.btnRequestTowing.setOnClickListener(v -> {
            Intent i = new Intent(this, ServiceRequestActivity.class);
            i.putExtra(Constants.EXTRA_GARAGE, new Gson().toJson(garage));
            i.putExtra(Constants.EXTRA_PROBLEM_SUMMARY, "Need towing assistance");
            startActivity(i);
        });
    }
}
