package com.autoaid.activities;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.lifecycle.ViewModelProvider;

import com.autoaid.databinding.ActivityRegisterBinding;
import com.autoaid.utils.SessionManager;
import com.autoaid.viewmodel.AuthViewModel;

public class RegisterActivity extends AppCompatActivity {

    private ActivityRegisterBinding binding;
    private AuthViewModel vm;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityRegisterBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        vm = new ViewModelProvider(this).get(AuthViewModel.class);

        binding.btnRegister.setOnClickListener(v -> vm.register(
                binding.etName.getText().toString().trim(),
                binding.etEmail.getText().toString().trim(),
                binding.etPhone.getText().toString().trim(),
                binding.etPassword.getText().toString().trim()
        ));

        vm.loading.observe(this, l -> binding.progress.setVisibility(l ? View.VISIBLE : View.GONE));
        vm.error.observe(this, e -> { if (e != null) Toast.makeText(this, e, Toast.LENGTH_LONG).show(); });

        vm.auth.observe(this, a -> {
            if (a == null || !a.success) {
                Toast.makeText(this, a != null ? a.message : "Register failed", Toast.LENGTH_LONG).show();
                return;
            }
            new SessionManager(this).saveAuth(a.token, a.getName(), a.getEmail(), a.getPhone());
            startActivity(new Intent(this, MainActivity.class));
            finish();
        });
    }
}
