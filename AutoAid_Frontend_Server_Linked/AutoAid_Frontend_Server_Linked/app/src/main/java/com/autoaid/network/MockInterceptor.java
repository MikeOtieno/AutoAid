package com.autoaid.network;

import androidx.annotation.NonNull;

import com.google.gson.Gson;

import java.io.IOException;
import java.util.*;

import okhttp3.Interceptor;
import okhttp3.MediaType;
import okhttp3.Protocol;
import okhttp3.Response;
import okhttp3.ResponseBody;
import okhttp3.Request;

public class MockInterceptor implements Interceptor {

    private static final MediaType JSON = MediaType.get("application/json; charset=utf-8");
    private final Gson gson = new Gson();

    @NonNull
    @Override
    public Response intercept(@NonNull Chain chain) throws IOException {
        Request req = chain.request();
        String path = req.url().encodedPath();

        if (path.endsWith("/auth/login") || path.endsWith("/auth/register")) {
            Map<String, Object> r = new HashMap<>();
            r.put("success", true);
            r.put("token", "mock_token_123");
            r.put("name", "AutoAid User");
            r.put("email", "user@example.com");
            r.put("phone", "+254700000000");
            return ok(chain, gson.toJson(r));
        }

        if (path.endsWith("/diagnose")) {
            Map<String, Object> r = new HashMap<>();
            r.put("problem", "Possible Brake Pad Wear");
            r.put("confidence", 82);
            r.put("urgency", "High");
            r.put("recommendedAction", "Brake pads may be worn and should be inspected immediately.");
            return ok(chain, gson.toJson(r));
        }

        if (path.endsWith("/garages/nearby")) {
            List<Map<String, Object>> garages = new ArrayList<>();
            garages.add(garage("Juja AutoCare", -1.102, 37.010, 4.5, "KES 3,000 - 8,000", "Brake specialist"));
            garages.add(garage("Thika Road Mechanics", -1.096, 37.020, 4.2, "KES 2,000 - 6,000", "General repairs"));
            return ok(chain, gson.toJson(garages));
        }

        return chain.proceed(req);
    }

    private Map<String, Object> garage(String name, double lat, double lng, double rating, String price, String spec) {
        Map<String, Object> g = new HashMap<>();
        g.put("id", UUID.randomUUID().toString());
        g.put("name", name);
        g.put("lat", lat);
        g.put("lng", lng);
        g.put("rating", rating);
        g.put("priceRange", price);
        g.put("specialization", spec);
        g.put("phone", "+254712345678");
        g.put("address", "Near main road");
        g.put("services", Arrays.asList("Brakes", "Oil change", "Diagnostics"));
        return g;
    }

    private Response ok(Chain chain, String body) {
        return new Response.Builder()
                .code(200)
                .message(body)
                .request(chain.request())
                .protocol(Protocol.HTTP_1_1)
                .body(ResponseBody.create(body, JSON))
                .addHeader("content-type", "application/json")
                .build();
    }
}
