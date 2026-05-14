package com.autoaid.database.dao;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.OnConflictStrategy;
import androidx.room.Query;

import com.autoaid.database.entities.ServiceRequestEntity;

import java.util.List;

@Dao
public interface RequestDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    long insert(ServiceRequestEntity e);

    @Query("SELECT * FROM service_requests ORDER BY createdAt DESC")
    LiveData<List<ServiceRequestEntity>> observeAll();
}
