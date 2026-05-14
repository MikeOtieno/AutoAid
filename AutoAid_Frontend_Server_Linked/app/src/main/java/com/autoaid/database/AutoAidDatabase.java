package com.autoaid.database;

import android.content.Context;

import androidx.room.Database;
import androidx.room.Room;
import androidx.room.RoomDatabase;

import com.autoaid.database.dao.DiagnosisDao;
import com.autoaid.database.dao.GarageDao;
import com.autoaid.database.dao.RequestDao;
import com.autoaid.database.entities.DiagnosisEntity;
import com.autoaid.database.entities.GarageEntity;
import com.autoaid.database.entities.ServiceRequestEntity;
import com.autoaid.utils.Constants;

@Database(entities = {DiagnosisEntity.class, GarageEntity.class, ServiceRequestEntity.class}, version = 1, exportSchema = false)
public abstract class AutoAidDatabase extends RoomDatabase {
    private static volatile AutoAidDatabase INSTANCE;

    public abstract DiagnosisDao diagnosisDao();
    public abstract GarageDao garageDao();
    public abstract RequestDao requestDao();

    public static AutoAidDatabase get(Context ctx) {
        if (INSTANCE == null) {
            synchronized (AutoAidDatabase.class) {
                if (INSTANCE == null) {
                    INSTANCE = Room.databaseBuilder(ctx.getApplicationContext(), AutoAidDatabase.class, Constants.DB_NAME)
                            .fallbackToDestructiveMigration()
                            .build();
                }
            }
        }
        return INSTANCE;
    }
}
