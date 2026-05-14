package com.autoaid.viewmodel;

import android.app.Application;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;

import com.autoaid.database.entities.ServiceRequestEntity;
import com.autoaid.models.ApiResponse;
import com.autoaid.models.ServiceRequestPayload;
import com.autoaid.network.NetworkResult;
import com.autoaid.repository.RequestRepository;

import java.util.List;

public class RequestViewModel extends AndroidViewModel {
    public final MutableLiveData<Boolean> loading = new MutableLiveData<>(false);
    public final MutableLiveData<String> error = new MutableLiveData<>();
    public final MutableLiveData<ApiResponse> submitted = new MutableLiveData<>();

    private final RequestRepository repo = new RequestRepository();

    public RequestViewModel(@NonNull Application application) { super(application); }

    public LiveData<List<ServiceRequestEntity>> observeRequests() {
        return repo.observeRequests(getApplication());
    }

    public void submit(ServiceRequestPayload payload, String garageName) {
        loading.setValue(true);
        new Thread(() -> {
            NetworkResult<ApiResponse> r = repo.submit(getApplication(), payload, garageName);
            loading.postValue(false);
            if (r.isSuccess()) submitted.postValue(r.data);
            else error.postValue(r.error);
        }).start();
    }
}
