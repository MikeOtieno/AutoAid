package com.autoaid.viewmodel;

import android.app.Application;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;

import com.autoaid.database.entities.GarageEntity;
import com.autoaid.models.Garage;
import com.autoaid.network.NetworkResult;
import com.autoaid.repository.GarageRepository;

import java.util.List;

public class GarageViewModel extends AndroidViewModel {
    public final MutableLiveData<Boolean> loading = new MutableLiveData<>(false);
    public final MutableLiveData<String> error = new MutableLiveData<>();

    private final GarageRepository repo = new GarageRepository();
    private LiveData<List<GarageEntity>> cached;

    public GarageViewModel(@NonNull Application application) { super(application); }

    public LiveData<List<GarageEntity>> cachedGarages() {
        if (cached == null) cached = repo.observeCached(getApplication());
        return cached;
    }

    public void fetch(double lat, double lng) {
        loading.setValue(true);
        new Thread(() -> {
            NetworkResult<List<Garage>> r = repo.fetchNearby(getApplication(), lat, lng);
            loading.postValue(false);
            if (!r.isSuccess()) error.postValue(r.error);
        }).start();
    }
}
