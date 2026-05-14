package com.autoaid.viewmodel;

import android.app.Application;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.MutableLiveData;

import com.autoaid.models.Auth.AuthResponse;
import com.autoaid.network.NetworkResult;
import com.autoaid.repository.AuthRepository;

public class AuthViewModel extends AndroidViewModel {

    public final MutableLiveData<Boolean> loading = new MutableLiveData<>(false);
    public final MutableLiveData<String> error = new MutableLiveData<>();
    public final MutableLiveData<AuthResponse> auth = new MutableLiveData<>();

    private final AuthRepository repo = new AuthRepository();

    public AuthViewModel(@NonNull Application application) {
        super(application);
    }

    public void login(String email, String password) {
        loading.setValue(true);
        new Thread(() -> {
            NetworkResult<AuthResponse> r = repo.login(getApplication(), email, password);
            loading.postValue(false);
            if (r.isSuccess()) auth.postValue(r.data);
            else error.postValue(r.error);
        }).start();
    }

    public void register(String name, String email, String phone, String password) {
        loading.setValue(true);
        new Thread(() -> {
            NetworkResult<AuthResponse> r = repo.register(getApplication(), name, email, phone, password);
            loading.postValue(false);
            if (r.isSuccess()) auth.postValue(r.data);
            else error.postValue(r.error);
        }).start();
    }
}
