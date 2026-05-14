package com.autoaid.activities;

import android.content.Intent;
import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;

import com.autoaid.utils.SessionManager;

public class SplashActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle b) {
        super.onCreate(b);
        SessionManager s = new SessionManager(this);
        startActivity(new Intent(this, s.isLoggedIn() ? MainActivity.class : LoginActivity.class));
        finish();
    }
}
