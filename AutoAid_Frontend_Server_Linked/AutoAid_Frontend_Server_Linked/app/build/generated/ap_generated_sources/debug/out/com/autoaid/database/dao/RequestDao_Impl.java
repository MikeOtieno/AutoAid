package com.autoaid.database.dao;

import android.database.Cursor;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.lifecycle.LiveData;
import androidx.room.EntityInsertionAdapter;
import androidx.room.RoomDatabase;
import androidx.room.RoomSQLiteQuery;
import androidx.room.util.CursorUtil;
import androidx.room.util.DBUtil;
import androidx.sqlite.db.SupportSQLiteStatement;
import com.autoaid.database.entities.ServiceRequestEntity;
import java.lang.Class;
import java.lang.Exception;
import java.lang.Override;
import java.lang.String;
import java.lang.SuppressWarnings;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.Callable;
import javax.annotation.processing.Generated;

@Generated("androidx.room.RoomProcessor")
@SuppressWarnings({"unchecked", "deprecation"})
public final class RequestDao_Impl implements RequestDao {
  private final RoomDatabase __db;

  private final EntityInsertionAdapter<ServiceRequestEntity> __insertionAdapterOfServiceRequestEntity;

  public RequestDao_Impl(@NonNull final RoomDatabase __db) {
    this.__db = __db;
    this.__insertionAdapterOfServiceRequestEntity = new EntityInsertionAdapter<ServiceRequestEntity>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "INSERT OR REPLACE INTO `service_requests` (`id`,`garageId`,`garageName`,`vehicleType`,`problemSummary`,`lat`,`lng`,`status`,`createdAt`) VALUES (nullif(?, 0),?,?,?,?,?,?,?,?)";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement,
          final ServiceRequestEntity entity) {
        statement.bindLong(1, entity.id);
        if (entity.garageId == null) {
          statement.bindNull(2);
        } else {
          statement.bindString(2, entity.garageId);
        }
        if (entity.garageName == null) {
          statement.bindNull(3);
        } else {
          statement.bindString(3, entity.garageName);
        }
        if (entity.vehicleType == null) {
          statement.bindNull(4);
        } else {
          statement.bindString(4, entity.vehicleType);
        }
        if (entity.problemSummary == null) {
          statement.bindNull(5);
        } else {
          statement.bindString(5, entity.problemSummary);
        }
        statement.bindDouble(6, entity.lat);
        statement.bindDouble(7, entity.lng);
        if (entity.status == null) {
          statement.bindNull(8);
        } else {
          statement.bindString(8, entity.status);
        }
        statement.bindLong(9, entity.createdAt);
      }
    };
  }

  @Override
  public long insert(final ServiceRequestEntity e) {
    __db.assertNotSuspendingTransaction();
    __db.beginTransaction();
    try {
      final long _result = __insertionAdapterOfServiceRequestEntity.insertAndReturnId(e);
      __db.setTransactionSuccessful();
      return _result;
    } finally {
      __db.endTransaction();
    }
  }

  @Override
  public LiveData<List<ServiceRequestEntity>> observeAll() {
    final String _sql = "SELECT * FROM service_requests ORDER BY createdAt DESC";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    return __db.getInvalidationTracker().createLiveData(new String[] {"service_requests"}, false, new Callable<List<ServiceRequestEntity>>() {
      @Override
      @Nullable
      public List<ServiceRequestEntity> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfId = CursorUtil.getColumnIndexOrThrow(_cursor, "id");
          final int _cursorIndexOfGarageId = CursorUtil.getColumnIndexOrThrow(_cursor, "garageId");
          final int _cursorIndexOfGarageName = CursorUtil.getColumnIndexOrThrow(_cursor, "garageName");
          final int _cursorIndexOfVehicleType = CursorUtil.getColumnIndexOrThrow(_cursor, "vehicleType");
          final int _cursorIndexOfProblemSummary = CursorUtil.getColumnIndexOrThrow(_cursor, "problemSummary");
          final int _cursorIndexOfLat = CursorUtil.getColumnIndexOrThrow(_cursor, "lat");
          final int _cursorIndexOfLng = CursorUtil.getColumnIndexOrThrow(_cursor, "lng");
          final int _cursorIndexOfStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "status");
          final int _cursorIndexOfCreatedAt = CursorUtil.getColumnIndexOrThrow(_cursor, "createdAt");
          final List<ServiceRequestEntity> _result = new ArrayList<ServiceRequestEntity>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final ServiceRequestEntity _item;
            _item = new ServiceRequestEntity();
            _item.id = _cursor.getLong(_cursorIndexOfId);
            if (_cursor.isNull(_cursorIndexOfGarageId)) {
              _item.garageId = null;
            } else {
              _item.garageId = _cursor.getString(_cursorIndexOfGarageId);
            }
            if (_cursor.isNull(_cursorIndexOfGarageName)) {
              _item.garageName = null;
            } else {
              _item.garageName = _cursor.getString(_cursorIndexOfGarageName);
            }
            if (_cursor.isNull(_cursorIndexOfVehicleType)) {
              _item.vehicleType = null;
            } else {
              _item.vehicleType = _cursor.getString(_cursorIndexOfVehicleType);
            }
            if (_cursor.isNull(_cursorIndexOfProblemSummary)) {
              _item.problemSummary = null;
            } else {
              _item.problemSummary = _cursor.getString(_cursorIndexOfProblemSummary);
            }
            _item.lat = _cursor.getDouble(_cursorIndexOfLat);
            _item.lng = _cursor.getDouble(_cursorIndexOfLng);
            if (_cursor.isNull(_cursorIndexOfStatus)) {
              _item.status = null;
            } else {
              _item.status = _cursor.getString(_cursorIndexOfStatus);
            }
            _item.createdAt = _cursor.getLong(_cursorIndexOfCreatedAt);
            _result.add(_item);
          }
          return _result;
        } finally {
          _cursor.close();
        }
      }

      @Override
      protected void finalize() {
        _statement.release();
      }
    });
  }

  @NonNull
  public static List<Class<?>> getRequiredConverters() {
    return Collections.emptyList();
  }
}
