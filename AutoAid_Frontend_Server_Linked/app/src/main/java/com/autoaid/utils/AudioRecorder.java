package com.autoaid.utils;

import android.content.Context;
import android.media.MediaRecorder;
import android.util.Base64;

import java.io.File;
import java.io.FileInputStream;
import java.util.UUID;

public class AudioRecorder {
    private MediaRecorder recorder;
    private File outFile;

    public File start(Context ctx) throws Exception {
        stop();
        File dir = ctx.getExternalFilesDir("Music");
        if (dir != null && !dir.exists()) dir.mkdirs();
        outFile = new File(dir, "audio_" + UUID.randomUUID() + ".m4a");

        recorder = new MediaRecorder();
        recorder.setAudioSource(MediaRecorder.AudioSource.MIC);
        recorder.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4);
        recorder.setAudioEncoder(MediaRecorder.AudioEncoder.AAC);
        recorder.setAudioSamplingRate(44100);
        recorder.setAudioEncodingBitRate(96000);
        recorder.setOutputFile(outFile.getAbsolutePath());
        recorder.prepare();
        recorder.start();
        return outFile;
    }

    public File stop() {
        try {
            if (recorder != null) {
                recorder.stop();
                recorder.release();
            }
        } catch (Exception ignored) {}
        recorder = null;
        return outFile;
    }

    public boolean isRecording() {
        return recorder != null;
    }

    public static String fileToBase64(File f) throws Exception {
        if (f == null || !f.exists()) return null;
        FileInputStream fis = new FileInputStream(f);
        byte[] buf = new byte[(int) f.length()];
        int read = fis.read(buf);
        fis.close();
        if (read <= 0) return null;
        return Base64.encodeToString(buf, Base64.NO_WRAP);
    }
}
