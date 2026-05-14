package com.autoaid.database.dao;

import android.database.Cursor;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.lifecycle.LiveData;
import androidx.room.EntityInsertionAdapter;
import androidx.room.RoomDatabase;
import androidx.room.RoomSQLiteQuery;
import androidx.room.SharedSQLiteStatement;
import androidx.room.util.CursorUtil;
import androidx.room.util.DBUtil;
import androidx.sqlite.db.SupportSQLiteStatement;
import com.autoaid.database.entities.GarageEntity;
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
public final class GarageDao_Impl implements GarageDao {
  private final RoomDatabase __db;

  private final EntityInsertionAdapter<GarageEntity> __insertionAdapterOfGarageEntity;

  private final SharedSQLiteStatement __preparedStmtOfClear;

  public GarageDao_Impl(@NonNull final RoomDatabase __db) {
    this.__db = __db;
    this.__insertionAdapterOfGarageEntity = new EntityInsertionAdapter<GarageEntity>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "INSERT OR REPLACE INTO `garages` (`id`,`name`,`lat`,`lng`,`rating`,`priceRange`,`specialization`,`phone`,`address`) VALUES (?,?,?,?,?,?,?,?,?)";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement,
          final GarageEntity entity) {
        if (entity.id == null) {
          statement.bindNull(1);
        } else {
          statement.bindString(1, entity.id);
        }
        if (entity.name == null) {
          statement.bindNull(2);
        } else {
          statement.bindString(2, entity.name);
        }
        statement.bindDouble(3, entity.lat);
        statement.bindDouble(4, entity.lng);
        statement.bindDouble(5, entity.rating);
        if (entity.priceRange == null) {
          statement.bindNull(6);
        } else {
          statement.bindString(6, entity.priceRange);
        }
        if (entity.specialization == null) {
          statement.bindNull(7);
        } else {
          statement.bindString(7, entity.specialization);
        }
        if (entity.phone == null) {
          statement.bindNull(8);
        } else {
          statement.bindString(8, entity.phone);
        }
        if (entity.address == null) {
          statement.bindNull(9);
        } else {
          statement.bindString(9, entity.address);
        }
      }
    };
    this.__preparedStmtOfClear = new SharedSQLiteStatement(__db) {
      @Override
      @NonNull
      public String createQuery() {
        final String _query = "DELETE FROM garages";
        return _query;
      }
    };
  }

  @Override
  public void upsertAll(final List<GarageEntity> garages) {
    __db.assertNotSuspendingTransaction();
    __db.beginTransaction();
    try {
      __insertionAdapterOfGarageEntity.insert(garages);
      __db.setTransactionSuccessful();
    } finally {
      __db.endTransaction();
    }
  }

  @Override
  public void clear() {
    __db.assertNotSuspendingTransaction();
    final SupportSQLiteStatement _stmt = __preparedStmtOfClear.acquire();
    try {
      __db.beginTransaction();
      try {
        _stmt.executeUpdateDelete();
        __db.setTransactionSuccessful();
      } finally {
        __db.endTransaction();
      }
    } finally {
      __preparedStmtOfClear.release(_stmt);
    }
  }

  @Override
  public LiveData<List<GarageEntity>> observeAll() {
    final String _sql = "SELECT * FROM garages";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    return __db.getInvalidationTracker().createLiveData(new String[] {"garages"}, false, new Callable<List<GarageEntity>>() {
      @Override
      @Nullable
      public List<GarageEntity> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfId = CursorUtil.getColumnIndexOrThrow(_cursor, "id");
          final int _cursorIndexOfName = CursorUtil.getColumnIndexOrThrow(_cursor, "name");
          final int _cursorIndexOfLat = CursorUtil.getColumnIndexOrThrow(_cursor, "lat");
          final int _cursorIndexOfLng = CursorUtil.getColumnIndexOrThrow(_cursor, "lng");
          final int _cursorIndexOfRating = CursorUtil.getColumnIndexOrThrow(_cursor, "rating");
          final int _cursorIndexOfPriceRange = CursorUtil.getColumnIndexOrThrow(_cursor, "priceRange");
          final int _cursorIndexOfSpecialization = CursorUtil.getColumnIndexOrThrow(_cursor, "specialization");
          final int _cursorIndexOfPhone = CursorUtil.getColumnIndexOrThrow(_cursor, "phone");
          final int _cursorIndexOfAddress = CursorUtil.getColumnIndexOrThrow(_cursor, "address");
          final List<GarageEntity> _result = new ArrayList<GarageEntity>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final GarageEntity _item;
            _item = new GarageEntity();
            if (_cursor.isNull(_cursorIndexOfId)) {
              _item.id = null;
            } else {
              _item.id = _cursor.getString(_cursorIndexOfId);
            }
            if (_cursor.isNull(_cursorIndexOfName)) {
              _item.name = null;
            } else {
              _item.name = _cursor.getString(_cursorIndexOfName);
            }
            _item.lat = _cursor.getDouble(_cursorIndexOfLat);
            _item.lng = _cursor.getDouble(_cursorIndexOfLng);
            _item.rating = _cursor.getDouble(_cursorIndexOfRating);
            if (_cursor.isNull(_cursorIndexOfPriceRange)) {
              _item.priceRange = null;
            } else {
              _item.priceRange = _cursor.getString(_cursorIndexOfPriceRange);
            }
            if (_cursor.isNull(_cursorIndexOfSpecialization)) {
              _item.specialization = null;
            } else {
              _item.specialization = _cursor.getString(_cursorIndexOfSpecialization);
            }
            if (_cursor.isNull(_cursorIndexOfPhone)) {
              _item.phone = null;
            } else {
              _item.phone = _cursor.getString(_cursorIndexOfPhone);
            }
            if (_cursor.isNull(_cursorIndexOfAddress)) {
              _item.address = null;
            } else {
              _item.address = _cursor.getString(_cursorIndexOfAddress);
            }
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
