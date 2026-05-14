package com.autoaid.activities;

import android.os.Bundle;
import android.content.Intent;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;

import com.autoaid.R;
import com.autoaid.databinding.ActivityMainBinding;
import com.autoaid.fragments.HomeFragment;
import com.autoaid.fragments.MyRequestsFragment;
import com.autoaid.fragments.ProfileFragment;
import com.autoaid.utils.SessionManager;

public class MainActivity extends AppCompatActivity {

    private ActivityMainBinding binding;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        show(new HomeFragment());

        binding.bottomNav.setOnItemSelectedListener(item -> {
            if (item.getItemId() == R.id.nav_home) show(new HomeFragment());
            else if (item.getItemId() == R.id.nav_requests) show(new MyRequestsFragment());
            else if (item.getItemId() == R.id.nav_profile) show(new ProfileFragment());
            return true;
        });
    }

    private void show(Fragment f) {
        getSupportFragmentManager().beginTransaction().replace(R.id.container, f).commit();
    }

    @Override
    public void onBackPressed() {
        new SessionManager(this).clear();
        Intent i = new Intent(this, LoginActivity.class);
        i.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
        startActivity(i);
    }
}

