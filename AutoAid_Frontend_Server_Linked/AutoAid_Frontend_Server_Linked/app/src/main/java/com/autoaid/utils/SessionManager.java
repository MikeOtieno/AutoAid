package com.autoaid.utils;

import android.content.Context;
import android.content.SharedPreferences;

public class SessionManager {
    private final SharedPreferences prefs;

    public SessionManager(Context ctx) {
        prefs = ctx.getSharedPreferences(Constants.PREFS, Context.MODE_PRIVATE);
    }

    public void saveAuth(String token, String name, String email, String phone) {
        prefs.edit()
                .putString("token", token)
                .putString("name", name)
                .putString("email", email)
                .putString("phone", phone)
                .apply();
    }

    public boolean isLoggedIn() {
        String t = getToken();
        return t != null && !t.isEmpty();
    }

    public String getToken() { return prefs.getString("token", ""); }
    public String getName() { return prefs.getString("name", ""); }
    public String getEmail(){ return prefs.getString("email",""); }
    public String getPhone(){ return prefs.getString("phone",""); }

    public void clear() { prefs.edit().clear().apply(); }
}
