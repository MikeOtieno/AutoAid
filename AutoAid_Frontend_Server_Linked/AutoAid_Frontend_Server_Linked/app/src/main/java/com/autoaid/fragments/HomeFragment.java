package com.autoaid.fragments;

import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import com.autoaid.activities.DiagnosisActivity;
import com.autoaid.activities.MechanicsMapActivity;
import com.autoaid.databinding.FragmentHomeBinding;

public class HomeFragment extends Fragment {

    private FragmentHomeBinding binding;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        binding = FragmentHomeBinding.inflate(inflater, container, false);

        binding.btnDiagnose.setOnClickListener(v -> startActivity(new Intent(getContext(), DiagnosisActivity.class)));
        binding.btnFindMechanics.setOnClickListener(v -> startActivity(new Intent(getContext(), MechanicsMapActivity.class)));

        return binding.getRoot();
    }
}
