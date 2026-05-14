package com.autoaid.fragments;

import android.os.Bundle;
import android.content.Intent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import com.autoaid.databinding.FragmentProfileBinding;
import com.autoaid.activities.LoginActivity;
import com.autoaid.utils.SessionManager;

public class ProfileFragment extends Fragment {

    private FragmentProfileBinding binding;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        binding = FragmentProfileBinding.inflate(inflater, container, false);

        SessionManager s = new SessionManager(requireContext());
        binding.etName.setText(s.getName());
        binding.etEmail.setText(s.getEmail());
        binding.etPhone.setText(s.getPhone());

        binding.btnSave.setOnClickListener(v -> {
            s.saveAuth(s.getToken(),
                    binding.etName.getText().toString(),
                    binding.etEmail.getText().toString(),
                    binding.etPhone.getText().toString());
            Toast.makeText(getContext(), "Profile updated (local).", Toast.LENGTH_LONG).show();
        });

        binding.btnLogout.setOnClickListener(v -> {
            s.clear();
            Intent i = new Intent(requireContext(), LoginActivity.class);
            i.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
            startActivity(i);
        });

        return binding.getRoot();
    }
}
