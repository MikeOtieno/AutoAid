package com.autoaid.activities;

import android.Manifest;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.widget.Toast;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;
import androidx.core.content.FileProvider;
import androidx.lifecycle.ViewModelProvider;

import com.autoaid.R;
import com.autoaid.databinding.ActivityDiagnosisBinding;
import com.autoaid.models.DiagnoseRequest;
import com.autoaid.utils.AudioRecorder;
import com.autoaid.utils.Constants;
import com.autoaid.utils.ImageUtils;
//import com.autoaid.utils.NetworkUtils;
import com.autoaid.viewmodel.DiagnoseViewModel;
import com.google.android.material.dialog.MaterialAlertDialogBuilder;
import com.google.android.material.snackbar.Snackbar;
import com.google.gson.Gson;

import java.io.File;
import java.io.IOException;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class DiagnosisActivity extends AppCompatActivity {

    private ActivityDiagnosisBinding binding;
    private DiagnoseViewModel vm;
    private final ExecutorService executorService = Executors.newSingleThreadExecutor();
    private final Handler mainHandler = new Handler(Looper.getMainLooper());

    private Uri imageUri;
    private File audioFile;
    private final AudioRecorder recorder = new AudioRecorder();
    private boolean isRecording = false;

    // Permission request codes
    private static final int PERMISSION_REQUEST_CODE = 100;

    // Activity result launchers
    private ActivityResultLauncher<String[]> permissionLauncher;
    private ActivityResultLauncher<String> pickImageLauncher;
    private ActivityResultLauncher<Uri> takePictureLauncher;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityDiagnosisBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        initializeViewModel();
        initializePermissionLauncher();
        initializeImageLaunchers();
        setupClickListeners();
        observeViewModel();
    }

    private void initializeViewModel() {
        vm = new ViewModelProvider(this).get(DiagnoseViewModel.class);
    }

    private void initializePermissionLauncher() {
        permissionLauncher = registerForActivityResult(
                new ActivityResultContracts.RequestMultiplePermissions(),
                this::handlePermissionResult
        );
    }

    private void handlePermissionResult(Map<String, Boolean> result) {
        boolean allGranted = true;
        StringBuilder deniedPermissions = new StringBuilder();

        for (Map.Entry<String, Boolean> entry : result.entrySet()) {
            if (!entry.getValue()) {
                allGranted = false;
                deniedPermissions.append(getPermissionName(entry.getKey())).append("\n");
            }
        }

        if (!allGranted) {
            showPermissionDeniedDialog(deniedPermissions.toString());
        }
    }

    private String getPermissionName(String permission) {
        switch (permission) {
            case Manifest.permission.CAMERA:
                return "Camera";
            case Manifest.permission.RECORD_AUDIO:
                return "Microphone";
            default:
                return permission;
        }
    }

    private void showPermissionDeniedDialog(String deniedPermissions) {
        new MaterialAlertDialogBuilder(this)
                .setTitle("Permissions Required")
                .setMessage("The following permissions are required:\n\n" + deniedPermissions +
                        "\n\nPlease grant them in settings to use this feature.")
                .setPositiveButton("Open Settings", (dialog, which) -> {
                    // Navigate to app settings
                    android.content.Intent intent = new android.content.Intent(
                            android.provider.Settings.ACTION_APPLICATION_DETAILS_SETTINGS);
                    intent.setData(Uri.parse("package:" + getPackageName()));
                    startActivity(intent);
                })
                .setNegativeButton("Cancel", null)
                .show();
    }

    private void initializeImageLaunchers() {
        pickImageLauncher = registerForActivityResult(
                new ActivityResultContracts.GetContent(),
                uri -> {
                    if (uri != null) {
                        imageUri = uri;
                        showImagePreview();
                    }
                }
        );

        takePictureLauncher = registerForActivityResult(
                new ActivityResultContracts.TakePicture(),
                success -> {
                    if (success && imageUri != null) {
                        showImagePreview();
                    } else {
                        // Clean up failed capture
                        deleteImageFile();
                    }
                }
        );
    }

    private void showImagePreview() {
        if (imageUri != null) {
            binding.cardPreview.setVisibility(View.VISIBLE);
            binding.ivPreview.setImageURI(imageUri);
        }
    }

    private void hideImagePreview() {
        binding.cardPreview.setVisibility(View.GONE);
        binding.ivPreview.setImageDrawable(null);
    }

    private void setupClickListeners() {
        binding.btnGallery.setOnClickListener(v -> pickImageLauncher.launch("image/*"));

        binding.btnCamera.setOnClickListener(v -> {
            if (checkPermission(Manifest.permission.CAMERA)) {
                launchCamera();
            } else {
                permissionLauncher.launch(new String[]{Manifest.permission.CAMERA});
            }
        });

        binding.btnRemoveImage.setOnClickListener(v -> {
            deleteImageFile();
            hideImagePreview();
            imageUri = null;
        });

        binding.btnRecord.setOnClickListener(v -> {
            if (checkPermission(Manifest.permission.RECORD_AUDIO)) {
                toggleAudioRecording();
            } else {
                permissionLauncher.launch(new String[]{Manifest.permission.RECORD_AUDIO});
            }
        });

        binding.btnSubmit.setOnClickListener(v -> submitDiagnosis());
    }

    private boolean checkPermission(String permission) {
        return ContextCompat.checkSelfPermission(this, permission) == PackageManager.PERMISSION_GRANTED;
    }

    private void launchCamera() {
        imageUri = createImageUri();
        if (imageUri != null) {
            takePictureLauncher.launch(imageUri);
        }
    }

    private void toggleAudioRecording() {
        try {
            if (!isRecording) {
                // Start recording
                audioFile = recorder.start(this);
                if (audioFile != null) {
                    isRecording = true;
                    updateRecordingUI(true);
                    showRecordingStartedMessage();
                }
            } else {
                // Stop recording
                recorder.stop();
                isRecording = false;
                updateRecordingUI(false);
                showRecordingCompleteMessage();
            }
        } catch (Exception e) {
            showError("Audio recording error: " + e.getMessage());
            isRecording = false;
            updateRecordingUI(false);
        }
    }

    private void updateRecordingUI(boolean recording) {
        if (recording) {
            binding.btnRecord.setText("Stop Recording");
            binding.btnRecord.setIcon(ContextCompat.getDrawable(this, R.drawable.ic_close));
        } else {
            binding.btnRecord.setText("Record Audio (Optional)");
            binding.btnRecord.setIcon(ContextCompat.getDrawable(this, R.drawable.ic_mic));
        }
    }

    private void showRecordingStartedMessage() {
        Snackbar.make(binding.getRoot(), "Recording started...", Snackbar.LENGTH_SHORT).show();
    }

    private void showRecordingCompleteMessage() {
        Snackbar.make(binding.getRoot(), "Audio recorded successfully", Snackbar.LENGTH_SHORT).show();
    }

    private void submitDiagnosis() {
        String description = binding.etDescription.getText().toString().trim();

        if (description.isEmpty()) {
            binding.etDescription.setError("Please describe the problem");
            binding.etDescription.requestFocus();
            return;
        }

//        if (!NetworkUtils.isNetworkAvailable(this)) {
//            showNoInternetDialog();
//            return;
//        }

        // Disable submit button to prevent double submission
        binding.btnSubmit.setEnabled(false);
        binding.progress.setVisibility(View.VISIBLE);

        // Process in background to avoid UI thread blocking
        executorService.execute(() -> {
            try {
                DiagnoseRequest request = prepareDiagnosisRequest(description);
                mainHandler.post(() -> vm.diagnose(request));
            } catch (Exception e) {
                mainHandler.post(() -> {
                    binding.btnSubmit.setEnabled(true);
                    binding.progress.setVisibility(View.GONE);
                    showError("Failed to prepare request: " + e.getMessage());
                });
            }
        });
    }

    @NonNull
    private DiagnoseRequest prepareDiagnosisRequest(String description) throws IOException {
        String imageBase64 = null;
        if (imageUri != null) {
//            imageBase64 = ImageUtils.toCompressedBase64(this, imageUri, 1280);
        }

        String audioBase64 = null;
        if (audioFile != null && audioFile.exists()) {
//            audioBase64 = AudioRecorder.fileToBase64(audioFile);
        }

        return new DiagnoseRequest(description, imageBase64, audioBase64);
    }

    private void showNoInternetDialog() {
        new MaterialAlertDialogBuilder(this)
                .setTitle("No Internet Connection")
                .setMessage("Please check your internet connection and try again.")
                .setPositiveButton("OK", null)
                .show();
    }

    private void observeViewModel() {
        vm.loading.observe(this, isLoading -> {
            binding.progress.setVisibility(isLoading ? View.VISIBLE : View.GONE);
            binding.btnSubmit.setEnabled(!isLoading);
        });

        vm.error.observe(this, error -> {
            if (error != null && !error.isEmpty()) {
                showError(error);
            }
        });

        vm.result.observe(this, result -> {
            if (result != null) {
                navigateToResult(result);
            }
        });
    }

    private void navigateToResult(Object result) {
        android.content.Intent intent = new android.content.Intent(this, DiagnosisResultActivity.class);
        intent.putExtra(Constants.EXTRA_DIAGNOSIS, new Gson().toJson(result));
        startActivity(intent);
        finish(); // Optional: close this activity
    }

    private Uri createImageUri() {
        try {
            File dir = getExternalFilesDir("Pictures");
            if (dir != null && !dir.exists()) {
                dir.mkdirs();
            }
            File file = new File(dir, "capture_" + System.currentTimeMillis() + ".jpg");
            return FileProvider.getUriForFile(this, getPackageName() + ".fileprovider", file);
        } catch (Exception e) {
            showError("Failed to create image file: " + e.getMessage());
            return null;
        }
    }

    private void deleteImageFile() {
        if (imageUri != null) {
            try {
                getContentResolver().delete(imageUri, null, null);
            } catch (Exception e) {
                // Ignore deletion errors
            }
        }
    }

    private void showError(String message) {
        Snackbar.make(binding.getRoot(), message, Snackbar.LENGTH_LONG)
                .setAction("Dismiss", v -> {})
                .show();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        cleanup();
    }

    private void cleanup() {
        // Stop recording if in progress
        if (isRecording) {
            recorder.stop();
            isRecording = false;
        }

        // Clean up temporary files
        deleteImageFile();
        if (audioFile != null && audioFile.exists()) {
            audioFile.delete();
        }

        // Shutdown executor service
        executorService.shutdown();
    }

    @Override
    public void onBackPressed() {
        if (hasUnsavedData()) {
            showUnsavedChangesDialog();
        } else {
            super.onBackPressed();
        }
    }

    private boolean hasUnsavedData() {
        return !binding.etDescription.getText().toString().trim().isEmpty() ||
                imageUri != null ||
                (audioFile != null && audioFile.exists());
    }

    private void showUnsavedChangesDialog() {
        new MaterialAlertDialogBuilder(this)
                .setTitle("Unsaved Changes")
                .setMessage("You have unsaved data. Are you sure you want to exit?")
                .setPositiveButton("Exit", (dialog, which) -> finish())
                .setNegativeButton("Stay", null)
                .show();
    }
}