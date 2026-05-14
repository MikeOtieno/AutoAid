package com.autoaid.database;

import androidx.annotation.NonNull;
import androidx.room.DatabaseConfiguration;
import androidx.room.InvalidationTracker;
import androidx.room.RoomDatabase;
import androidx.room.RoomOpenHelper;
import androidx.room.migration.AutoMigrationSpec;
import androidx.room.migration.Migration;
import androidx.room.util.DBUtil;
import androidx.room.util.TableInfo;
import androidx.sqlite.db.SupportSQLiteDatabase;
import androidx.sqlite.db.SupportSQLiteOpenHelper;
import com.autoaid.database.dao.DiagnosisDao;
import com.autoaid.database.dao.DiagnosisDao_Impl;
import com.autoaid.database.dao.GarageDao;
import com.autoaid.database.dao.GarageDao_Impl;
import com.autoaid.database.dao.RequestDao;
import com.autoaid.database.dao.RequestDao_Impl;
import java.lang.Class;
import java.lang.Override;
import java.lang.String;
import java.lang.SuppressWarnings;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import javax.annotation.processing.Generated;

@Generated("androidx.room.RoomProcessor")
@SuppressWarnings({"unchecked", "deprecation"})
public final class AutoAidDatabase_Impl extends AutoAidDatabase {
  private volatile DiagnosisDao _diagnosisDao;

  private volatile GarageDao _garageDao;

  private volatile RequestDao _requestDao;

  @Override
  @NonNull
  protected SupportSQLiteOpenHelper createOpenHelper(@NonNull final DatabaseConfiguration config) {
    final SupportSQLiteOpenHelper.Callback _openCallback = new RoomOpenHelper(config, new RoomOpenHelper.Delegate(1) {
      @Override
      public void createAllTables(@NonNull final SupportSQLiteDatabase db) {
        db.execSQL("CREATE TABLE IF NOT EXISTS `diagnoses` (`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, `description` TEXT, `problem` TEXT, `confidence` INTEGER NOT NULL, `urgency` TEXT, `recommendedAction` TEXT, `createdAt` INTEGER NOT NULL)");
        db.execSQL("CREATE TABLE IF NOT EXISTS `garages` (`id` TEXT NOT NULL, `name` TEXT, `lat` REAL NOT NULL, `lng` REAL NOT NULL, `rating` REAL NOT NULL, `priceRange` TEXT, `specialization` TEXT, `phone` TEXT, `address` TEXT, PRIMARY KEY(`id`))");
        db.execSQL("CREATE TABLE IF NOT EXISTS `service_requests` (`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, `garageId` TEXT, `garageName` TEXT, `vehicleType` TEXT, `problemSummary` TEXT, `lat` REAL NOT NULL, `lng` REAL NOT NULL, `status` TEXT, `createdAt` INTEGER NOT NULL)");
        db.execSQL("CREATE TABLE IF NOT EXISTS room_master_table (id INTEGER PRIMARY KEY,identity_hash TEXT)");
        db.execSQL("INSERT OR REPLACE INTO room_master_table (id,identity_hash) VALUES(42, '016c0c595f908b7a142a8ceed5a132a1')");
      }

      @Override
      public void dropAllTables(@NonNull final SupportSQLiteDatabase db) {
        db.execSQL("DROP TABLE IF EXISTS `diagnoses`");
        db.execSQL("DROP TABLE IF EXISTS `garages`");
        db.execSQL("DROP TABLE IF EXISTS `service_requests`");
        final List<? extends RoomDatabase.Callback> _callbacks = mCallbacks;
        if (_callbacks != null) {
          for (RoomDatabase.Callback _callback : _callbacks) {
            _callback.onDestructiveMigration(db);
          }
        }
      }

      @Override
      public void onCreate(@NonNull final SupportSQLiteDatabase db) {
        final List<? extends RoomDatabase.Callback> _callbacks = mCallbacks;
        if (_callbacks != null) {
          for (RoomDatabase.Callback _callback : _callbacks) {
            _callback.onCreate(db);
          }
        }
      }

      @Override
      public void onOpen(@NonNull final SupportSQLiteDatabase db) {
        mDatabase = db;
        internalInitInvalidationTracker(db);
        final List<? extends RoomDatabase.Callback> _callbacks = mCallbacks;
        if (_callbacks != null) {
          for (RoomDatabase.Callback _callback : _callbacks) {
            _callback.onOpen(db);
          }
        }
      }

      @Override
      public void onPreMigrate(@NonNull final SupportSQLiteDatabase db) {
        DBUtil.dropFtsSyncTriggers(db);
      }

      @Override
      public void onPostMigrate(@NonNull final SupportSQLiteDatabase db) {
      }

      @Override
      @NonNull
      public RoomOpenHelper.ValidationResult onValidateSchema(
          @NonNull final SupportSQLiteDatabase db) {
        final HashMap<String, TableInfo.Column> _columnsDiagnoses = new HashMap<String, TableInfo.Column>(7);
        _columnsDiagnoses.put("id", new TableInfo.Column("id", "INTEGER", true, 1, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsDiagnoses.put("description", new TableInfo.Column("description", "TEXT", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsDiagnoses.put("problem", new TableInfo.Column("problem", "TEXT", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsDiagnoses.put("confidence", new TableInfo.Column("confidence", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsDiagnoses.put("urgency", new TableInfo.Column("urgency", "TEXT", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsDiagnoses.put("recommendedAction", new TableInfo.Column("recommendedAction", "TEXT", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsDiagnoses.put("createdAt", new TableInfo.Column("createdAt", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        final HashSet<TableInfo.ForeignKey> _foreignKeysDiagnoses = new HashSet<TableInfo.ForeignKey>(0);
        final HashSet<TableInfo.Index> _indicesDiagnoses = new HashSet<TableInfo.Index>(0);
        final TableInfo _infoDiagnoses = new TableInfo("diagnoses", _columnsDiagnoses, _foreignKeysDiagnoses, _indicesDiagnoses);
        final TableInfo _existingDiagnoses = TableInfo.read(db, "diagnoses");
        if (!_infoDiagnoses.equals(_existingDiagnoses)) {
          return new RoomOpenHelper.ValidationResult(false, "diagnoses(com.autoaid.database.entities.DiagnosisEntity).\n"
                  + " Expected:\n" + _infoDiagnoses + "\n"
                  + " Found:\n" + _existingDiagnoses);
        }
        final HashMap<String, TableInfo.Column> _columnsGarages = new HashMap<String, TableInfo.Column>(9);
        _columnsGarages.put("id", new TableInfo.Column("id", "TEXT", true, 1, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsGarages.put("name", new TableInfo.Column("name", "TEXT", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsGarages.put("lat", new TableInfo.Column("lat", "REAL", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsGarages.put("lng", new TableInfo.Column("lng", "REAL", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsGarages.put("rating", new TableInfo.Column("rating", "REAL", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsGarages.put("priceRange", new TableInfo.Column("priceRange", "TEXT", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsGarages.put("specialization", new TableInfo.Column("specialization", "TEXT", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsGarages.put("phone", new TableInfo.Column("phone", "TEXT", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsGarages.put("address", new TableInfo.Column("address", "TEXT", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        final HashSet<TableInfo.ForeignKey> _foreignKeysGarages = new HashSet<TableInfo.ForeignKey>(0);
        final HashSet<TableInfo.Index> _indicesGarages = new HashSet<TableInfo.Index>(0);
        final TableInfo _infoGarages = new TableInfo("garages", _columnsGarages, _foreignKeysGarages, _indicesGarages);
        final TableInfo _existingGarages = TableInfo.read(db, "garages");
        if (!_infoGarages.equals(_existingGarages)) {
          return new RoomOpenHelper.ValidationResult(false, "garages(com.autoaid.database.entities.GarageEntity).\n"
                  + " Expected:\n" + _infoGarages + "\n"
                  + " Found:\n" + _existingGarages);
        }
        final HashMap<String, TableInfo.Column> _columnsServiceRequests = new HashMap<String, TableInfo.Column>(9);
        _columnsServiceRequests.put("id", new TableInfo.Column("id", "INTEGER", true, 1, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsServiceRequests.put("garageId", new TableInfo.Column("garageId", "TEXT", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsServiceRequests.put("garageName", new TableInfo.Column("garageName", "TEXT", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsServiceRequests.put("vehicleType", new TableInfo.Column("vehicleType", "TEXT", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsServiceRequests.put("problemSummary", new TableInfo.Column("problemSummary", "TEXT", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsServiceRequests.put("lat", new TableInfo.Column("lat", "REAL", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsServiceRequests.put("lng", new TableInfo.Column("lng", "REAL", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsServiceRequests.put("status", new TableInfo.Column("status", "TEXT", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsServiceRequests.put("createdAt", new TableInfo.Column("createdAt", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        final HashSet<TableInfo.ForeignKey> _foreignKeysServiceRequests = new HashSet<TableInfo.ForeignKey>(0);
        final HashSet<TableInfo.Index> _indicesServiceRequests = new HashSet<TableInfo.Index>(0);
        final TableInfo _infoServiceRequests = new TableInfo("service_requests", _columnsServiceRequests, _foreignKeysServiceRequests, _indicesServiceRequests);
        final TableInfo _existingServiceRequests = TableInfo.read(db, "service_requests");
        if (!_infoServiceRequests.equals(_existingServiceRequests)) {
          return new RoomOpenHelper.ValidationResult(false, "service_requests(com.autoaid.database.entities.ServiceRequestEntity).\n"
                  + " Expected:\n" + _infoServiceRequests + "\n"
                  + " Found:\n" + _existingServiceRequests);
        }
        return new RoomOpenHelper.ValidationResult(true, null);
      }
    }, "016c0c595f908b7a142a8ceed5a132a1", "d476f9771232d6dd61e44a3fcff46a3c");
    final SupportSQLiteOpenHelper.Configuration _sqliteConfig = SupportSQLiteOpenHelper.Configuration.builder(config.context).name(config.name).callback(_openCallback).build();
    final SupportSQLiteOpenHelper _helper = config.sqliteOpenHelperFactory.create(_sqliteConfig);
    return _helper;
  }

  @Override
  @NonNull
  protected InvalidationTracker createInvalidationTracker() {
    final HashMap<String, String> _shadowTablesMap = new HashMap<String, String>(0);
    final HashMap<String, Set<String>> _viewTables = new HashMap<String, Set<String>>(0);
    return new InvalidationTracker(this, _shadowTablesMap, _viewTables, "diagnoses","garages","service_requests");
  }

  @Override
  public void clearAllTables() {
    super.assertNotMainThread();
    final SupportSQLiteDatabase _db = super.getOpenHelper().getWritableDatabase();
    try {
      super.beginTransaction();
      _db.execSQL("DELETE FROM `diagnoses`");
      _db.execSQL("DELETE FROM `garages`");
      _db.execSQL("DELETE FROM `service_requests`");
      super.setTransactionSuccessful();
    } finally {
      super.endTransaction();
      _db.query("PRAGMA wal_checkpoint(FULL)").close();
      if (!_db.inTransaction()) {
        _db.execSQL("VACUUM");
      }
    }
  }

  @Override
  @NonNull
  protected Map<Class<?>, List<Class<?>>> getRequiredTypeConverters() {
    final HashMap<Class<?>, List<Class<?>>> _typeConvertersMap = new HashMap<Class<?>, List<Class<?>>>();
    _typeConvertersMap.put(DiagnosisDao.class, DiagnosisDao_Impl.getRequiredConverters());
    _typeConvertersMap.put(GarageDao.class, GarageDao_Impl.getRequiredConverters());
    _typeConvertersMap.put(RequestDao.class, RequestDao_Impl.getRequiredConverters());
    return _typeConvertersMap;
  }

  @Override
  @NonNull
  public Set<Class<? extends AutoMigrationSpec>> getRequiredAutoMigrationSpecs() {
    final HashSet<Class<? extends AutoMigrationSpec>> _autoMigrationSpecsSet = new HashSet<Class<? extends AutoMigrationSpec>>();
    return _autoMigrationSpecsSet;
  }

  @Override
  @NonNull
  public List<Migration> getAutoMigrations(
      @NonNull final Map<Class<? extends AutoMigrationSpec>, AutoMigrationSpec> autoMigrationSpecs) {
    final List<Migration> _autoMigrations = new ArrayList<Migration>();
    return _autoMigrations;
  }

  @Override
  public DiagnosisDao diagnosisDao() {
    if (_diagnosisDao != null) {
      return _diagnosisDao;
    } else {
      synchronized(this) {
        if(_diagnosisDao == null) {
          _diagnosisDao = new DiagnosisDao_Impl(this);
        }
        return _diagnosisDao;
      }
    }
  }

  @Override
  public GarageDao garageDao() {
    if (_garageDao != null) {
      return _garageDao;
    } else {
      synchronized(this) {
        if(_garageDao == null) {
          _garageDao = new GarageDao_Impl(this);
        }
        return _garageDao;
      }
    }
  }

  @Override
  public RequestDao requestDao() {
    if (_requestDao != null) {
      return _requestDao;
    } else {
      synchronized(this) {
        if(_requestDao == null) {
          _requestDao = new RequestDao_Impl(this);
        }
        return _requestDao;
      }
    }
  }
}
