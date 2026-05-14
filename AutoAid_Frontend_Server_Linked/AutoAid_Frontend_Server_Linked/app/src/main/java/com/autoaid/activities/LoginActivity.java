package com.autoaid.activities;

import android.content.Intent;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.lifecycle.ViewModelProvider;

import com.autoaid.databinding.ActivityLoginBinding;
import com.autoaid.utils.SessionManager;
import com.autoaid.viewmodel.AuthViewModel;

public class LoginActivity extends AppCompatActivity {

    private ActivityLoginBinding binding;
    private AuthViewModel vm;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        binding = ActivityLoginBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        vm = new ViewModelProvider(this).get(AuthViewModel.class);

        setupListeners();
        observeViewModel();
    }

    private void setupListeners() {

        binding.btnLogin.setOnClickListener(v -> performLogin());

        binding.tvRegister.setOnClickListener(v ->
                startActivity(new Intent(this, RegisterActivity.class))
        );

        binding.tvForgot.setOnClickListener(v ->
                startActivity(new Intent(this, ForgotPasswordActivity.class))
        );
    }

    private void performLogin() {

        String email = binding.etEmail.getText().toString().trim();
        String password = binding.etPassword.getText().toString().trim();

        if (TextUtils.isEmpty(email)) {
            binding.etEmail.setError("Email is required");
            return;
        }

        if (TextUtils.isEmpty(password)) {
            binding.etPassword.setError("Password is required");
            return;
        }

        vm.login(email, password);
    }

    private void observeViewModel() {

        vm.loading.observe(this, isLoading -> {
            binding.progress.setVisibility(isLoading ? View.VISIBLE : View.GONE);
            binding.btnLogin.setEnabled(!isLoading);
        });

        vm.error.observe(this, error -> {
            if (error != null && !error.isEmpty()) {
                Toast.makeText(this, error, Toast.LENGTH_LONG).show();
            }
        });

        vm.auth.observe(this, auth -> {

            if (auth == null || !auth.success) {
                Toast.makeText(this,
                        auth != null ? auth.message : "Login failed",
                        Toast.LENGTH_LONG).show();
                return;
            }

            SessionManager session = new SessionManager(this);
            session.saveAuth(auth.token, auth.getName(), auth.getEmail(), auth.getPhone());

            startActivity(new Intent(this, MainActivity.class));
            finish();
        });
    }
}