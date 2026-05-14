package com.autoaid.fragments;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import com.autoaid.adapters.RequestAdapter;
import com.autoaid.databinding.FragmentRequestsBinding;
import com.autoaid.viewmodel.RequestViewModel;

public class MyRequestsFragment extends Fragment {

    private FragmentRequestsBinding binding;
    private RequestAdapter adapter;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        binding = FragmentRequestsBinding.inflate(inflater, container, false);

        adapter = new RequestAdapter();
        binding.recycler.setAdapter(adapter);

        RequestViewModel vm = new ViewModelProvider(this).get(RequestViewModel.class);
        vm.observeRequests().observe(getViewLifecycleOwner(), adapter::submit);

        return binding.getRoot();
    }
}
