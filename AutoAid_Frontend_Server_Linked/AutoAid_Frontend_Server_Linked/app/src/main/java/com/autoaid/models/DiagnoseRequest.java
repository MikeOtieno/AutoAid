package com.autoaid.models;

public class DiagnoseRequest {
    public String description;
    public String image;
    public String audio;

    public DiagnoseRequest(String description, String image, String audio) {
        this.description = description;
        this.image = image;
        this.audio = audio;
    }
}
