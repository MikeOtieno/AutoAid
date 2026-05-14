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
import com.autoaid.database.entities.DiagnosisEntity;
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
public final class DiagnosisDao_Impl implements DiagnosisDao {
  private final RoomDatabase __db;

  private final EntityInsertionAdapter<DiagnosisEntity> __insertionAdapterOfDiagnosisEntity;

  public DiagnosisDao_Impl(@NonNull final RoomDatabase __db) {
    this.__db = __db;
    this.__insertionAdapterOfDiagnosisEntity = new EntityInsertionAdapter<DiagnosisEntity>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "INSERT OR REPLACE INTO `diagnoses` (`id`,`description`,`problem`,`confidence`,`urgency`,`recommendedAction`,`createdAt`) VALUES (nullif(?, 0),?,?,?,?,?,?)";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement,
          final DiagnosisEntity entity) {
        statement.bindLong(1, entity.id);
        if (entity.description == null) {
          statement.bindNull(2);
        } else {
          statement.bindString(2, entity.description);
        }
        if (entity.problem == null) {
          statement.bindNull(3);
        } else {
          statement.bindString(3, entity.problem);
        }
        statement.bindLong(4, entity.confidence);
        if (entity.urgency == null) {
          statement.bindNull(5);
        } else {
          statement.bindString(5, entity.urgency);
        }
        if (entity.recommendedAction == null) {
          statement.bindNull(6);
        } else {
          statement.bindString(6, entity.recommendedAction);
        }
        statement.bindLong(7, entity.createdAt);
      }
    };
  }

  @Override
  public long insert(final DiagnosisEntity e) {
    __db.assertNotSuspendingTransaction();
    __db.beginTransaction();
    try {
      final long _result = __insertionAdapterOfDiagnosisEntity.insertAndReturnId(e);
      __db.setTransactionSuccessful();
      return _result;
    } finally {
      __db.endTransaction();
    }
  }

  @Override
  public LiveData<List<DiagnosisEntity>> observeAll() {
    final String _sql = "SELECT * FROM diagnoses ORDER BY createdAt DESC";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    return __db.getInvalidationTracker().createLiveData(new String[] {"diagnoses"}, false, new Callable<List<DiagnosisEntity>>() {
      @Override
      @Nullable
      public List<DiagnosisEntity> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfId = CursorUtil.getColumnIndexOrThrow(_cursor, "id");
          final int _cursorIndexOfDescription = CursorUtil.getColumnIndexOrThrow(_cursor, "description");
          final int _cursorIndexOfProblem = CursorUtil.getColumnIndexOrThrow(_cursor, "problem");
          final int _cursorIndexOfConfidence = CursorUtil.getColumnIndexOrThrow(_cursor, "confidence");
          final int _cursorIndexOfUrgency = CursorUtil.getColumnIndexOrThrow(_cursor, "urgency");
          final int _cursorIndexOfRecommendedAction = CursorUtil.getColumnIndexOrThrow(_cursor, "recommendedAction");
          final int _cursorIndexOfCreatedAt = CursorUtil.getColumnIndexOrThrow(_cursor, "createdAt");
          final List<DiagnosisEntity> _result = new ArrayList<DiagnosisEntity>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final DiagnosisEntity _item;
            _item = new DiagnosisEntity();
            _item.id = _cursor.getLong(_cursorIndexOfId);
            if (_cursor.isNull(_cursorIndexOfDescription)) {
              _item.description = null;
            } else {
              _item.description = _cursor.getString(_cursorIndexOfDescription);
            }
            if (_cursor.isNull(_cursorIndexOfProblem)) {
              _item.problem = null;
            } else {
              _item.problem = _cursor.getString(_cursorIndexOfProblem);
            }
            _item.confidence = _cursor.getInt(_cursorIndexOfConfidence);
            if (_cursor.isNull(_cursorIndexOfUrgency)) {
              _item.urgency = null;
            } else {
              _item.urgency = _cursor.getString(_cursorIndexOfUrgency);
            }
            if (_cursor.isNull(_cursorIndexOfRecommendedAction)) {
              _item.recommendedAction = null;
            } else {
              _item.recommendedAction = _cursor.getString(_cursorIndexOfRecommendedAction);
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
