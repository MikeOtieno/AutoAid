package com.autoaid.activities;

import android.os.Bundle;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.autoaid.databinding.ActivityForgotPasswordBinding;

public class ForgotPasswordActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        ActivityForgotPasswordBinding b = ActivityForgotPasswordBinding.inflate(getLayoutInflater());
        setContentView(b.getRoot());

        b.btnSend.setOnClickListener(v -> Toast.makeText(this, "Mock reset link sent to email (demo).", Toast.LENGTH_LONG).show());
    }
}
