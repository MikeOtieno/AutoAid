package com.autoaid.database.dao;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.OnConflictStrategy;
import androidx.room.Query;

import com.autoaid.database.entities.GarageEntity;

import java.util.List;

@Dao
public interface GarageDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    void upsertAll(List<GarageEntity> garages);

    @Query("DELETE FROM garages")
    void clear();

    @Query("SELECT * FROM garages")
    LiveData<List<GarageEntity>> observeAll();
}
