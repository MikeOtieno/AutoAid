package com.autoaid.network;

public class NetworkResult<T> {
    public final T data;
    public final String error;

    private NetworkResult(T data, String error) {
        this.data = data;
        this.error = error;
    }

    public static <T> NetworkResult<T> ok(T data) { return new NetworkResult<>(data, null); }
    public static <T> NetworkResult<T> fail(String err) { return new NetworkResult<>(null, err); }

    public boolean isSuccess() { return error == null; }
}
