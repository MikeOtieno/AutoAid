package com.autoaid.adapters;

import android.view.LayoutInflater;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.autoaid.database.entities.ServiceRequestEntity;
import com.autoaid.databinding.ItemRequestBinding;

import java.util.ArrayList;
import java.util.List;

public class RequestAdapter extends RecyclerView.Adapter<RequestAdapter.VH> {
    private final List<ServiceRequestEntity> data = new ArrayList<>();

    public void submit(List<ServiceRequestEntity> list) {
        data.clear();
        if (list != null) data.addAll(list);
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public VH onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        return new VH(ItemRequestBinding.inflate(LayoutInflater.from(parent.getContext()), parent, false));
    }

    @Override
    public void onBindViewHolder(@NonNull VH h, int pos) {
        ServiceRequestEntity r = data.get(pos);
        h.b.tvGarage.setText(r.garageName);
        h.b.tvSummary.setText(r.problemSummary);
        h.b.tvStatus.setText(r.status);
    }

    @Override
    public int getItemCount() { return data.size(); }

    static class VH extends RecyclerView.ViewHolder {
        ItemRequestBinding b;
        VH(ItemRequestBinding b) {
            super(b.getRoot());
            this.b = b;
        }
    }
}
