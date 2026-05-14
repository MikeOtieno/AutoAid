package com.autoaid.adapters;

import android.view.LayoutInflater;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.autoaid.database.entities.GarageEntity;
import com.autoaid.databinding.ItemGarageBinding;

import java.util.ArrayList;
import java.util.List;

public class GarageAdapter extends RecyclerView.Adapter<GarageAdapter.VH> {

    public interface OnGarageClick { void onClick(GarageEntity g); }

    private final OnGarageClick click;
    private final List<GarageEntity> data = new ArrayList<>();

    public GarageAdapter(OnGarageClick click) {
        this.click = click;
    }

    public void submitEntities(List<GarageEntity> list) {
        data.clear();
        if (list != null) data.addAll(list);
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public VH onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        ItemGarageBinding b = ItemGarageBinding.inflate(LayoutInflater.from(parent.getContext()), parent, false);
        return new VH(b);
    }

    @Override
    public void onBindViewHolder(@NonNull VH h, int pos) {
        GarageEntity g = data.get(pos);
        h.b.tvName.setText(g.name);
        h.b.tvRating.setText(String.valueOf(g.rating));
        h.b.tvDistance.setText("Nearby");
        h.b.tvSpec.setText(g.specialization);
        h.b.getRoot().setOnClickListener(v -> click.onClick(g));
    }

    @Override
    public int getItemCount() { return data.size(); }

    static class VH extends RecyclerView.ViewHolder {
        ItemGarageBinding b;
        VH(ItemGarageBinding b) {
            super(b.getRoot());
            this.b = b;
        }
    }
}
