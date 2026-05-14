package com.autoaid.viewmodel;

import android.app.Application;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.MutableLiveData;

import com.autoaid.models.DiagnoseRequest;
import com.autoaid.models.DiagnoseResponse;
import com.autoaid.network.NetworkResult;
import com.autoaid.repository.DiagnoseRepository;

public class DiagnoseViewModel extends AndroidViewModel {
    public final MutableLiveData<Boolean> loading = new MutableLiveData<>(false);
    public final MutableLiveData<String> error = new MutableLiveData<>();
    public final MutableLiveData<DiagnoseResponse> result = new MutableLiveData<>();

    private final DiagnoseRepository repo = new DiagnoseRepository();

    public DiagnoseViewModel(@NonNull Application application) { super(application); }

    public void diagnose(DiagnoseRequest req) {
        loading.setValue(true);
        new Thread(() -> {
            NetworkResult<DiagnoseResponse> r = repo.diagnose(getApplication(), req);
            loading.postValue(false);
            if (r.isSuccess()) result.postValue(r.data);
            else error.postValue(r.error);
        }).start();
    }
}
