package com.autoaid.database.dao;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.OnConflictStrategy;
import androidx.room.Query;

import com.autoaid.database.entities.DiagnosisEntity;

import java.util.List;

@Dao
public interface DiagnosisDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    long insert(DiagnosisEntity e);

    @Query("SELECT * FROM diagnoses ORDER BY createdAt DESC")
    LiveData<List<DiagnosisEntity>> observeAll();
}
