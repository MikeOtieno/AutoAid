package com.autoaid.utils;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.util.Base64;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;

public class ImageUtils {

    public static String toCompressedBase64(Context ctx, Uri imageUri, int maxDim) throws Exception {
        Bitmap bitmap = decodeScaledBitmap(ctx, imageUri, maxDim);
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.JPEG, 80, baos);
        byte[] bytes = baos.toByteArray();
        return Base64.encodeToString(bytes, Base64.NO_WRAP);
    }

    private static Bitmap decodeScaledBitmap(Context ctx, Uri uri, int maxDim) throws Exception {
        InputStream is1 = ctx.getContentResolver().openInputStream(uri);
        BitmapFactory.Options opts = new BitmapFactory.Options();
        opts.inJustDecodeBounds = true;
        BitmapFactory.decodeStream(is1, null, opts);
        if (is1 != null) is1.close();

        int inSampleSize = 1;
        int w = opts.outWidth, h = opts.outHeight;
        while (Math.max(w / inSampleSize, h / inSampleSize) > maxDim) {
            inSampleSize *= 2;
        }

        BitmapFactory.Options opts2 = new BitmapFactory.Options();
        opts2.inSampleSize = inSampleSize;

        InputStream is2 = ctx.getContentResolver().openInputStream(uri);
        Bitmap bm = BitmapFactory.decodeStream(is2, null, opts2);
        if (is2 != null) is2.close();
        return bm;
    }
}
