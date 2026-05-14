"""
AutoAid Car Damage Severity Classifier — Retrain Script
========================================================
Dataset: Roboflow car-damages-v1 (COCO segmentation format)
Classes: Minor Damage -Dent-, Minor Damage -Scratch-, Severe Damage, No Damage
Model:   MobileNetV2 transfer learning (single-label classification)

Usage:
    1. Extract car_damages_v1i_coco-segmentation.zip to a folder
    2. Set DATASET_DIR below to that folder path
    3. pip install tensorflow opencv-python scikit-learn matplotlib
    4. python retrain_damage_classifier.py

Output:
    models/damage_classifier.h5        ← drop-in replacement for your existing model
    models/damage_severity_classes.json ← class names for image_infer.py
    models/training_curves.png
"""

import os
import json
import numpy as np
import cv2
import matplotlib.pyplot as plt
from collections import Counter
from pathlib import Path

# ─── CONFIG ───────────────────────────────────────────────────────────────────
DATASET_DIR = r"C:\Users\mikeo\Desktop\car_damage_detection"        # folder where you extracted the zip
                         # should contain: train/, valid/, test/
IMG_SIZE    = 224
BATCH_SIZE  = 16
EPOCHS      = 40
MODEL_SAVE  = "models/damage_classifier.h5"
CLASSES_SAVE = "models/damage_classifier_classes.json"

# Classes to keep — map Roboflow names → clean AutoAid names
CLASS_MAP = {
    'Minor Damage -Dent-':    'Minor Damage - Dent',
    'Minor Damage -Scratch-': 'Minor Damage - Scratch',
    'Severe Damage':          'Severe Damage',
    'No Damage':              'No Damage',
}

# Ignore these Roboflow noise labels
IGNORE_CLASSES = {'car-damagesv2', '-'}


# ─── STEP 1: LOAD COCO ANNOTATIONS ───────────────────────────────────────────
def load_dataset(json_path, img_dir, class_to_idx):
    with open(json_path) as f:
        coco = json.load(f)

    cats = {c['id']: c['name'] for c in coco['categories']}
    id_to_file = {img['id']: img['file_name'] for img in coco['images']}

    # Each image → dominant class (highest annotation area wins)
    id_to_class = {}
    id_to_area  = {}
    for ann in coco['annotations']:
        cat_name = cats.get(ann['category_id'], '')
        if cat_name in IGNORE_CLASSES:
            continue
        clean_name = CLASS_MAP.get(cat_name)
        if clean_name is None:
            continue
        iid  = ann['image_id']
        area = ann.get('area', 1.0)
        if iid not in id_to_area or area > id_to_area[iid]:
            id_to_area[iid]  = area
            id_to_class[iid] = clean_name

    samples = []
    for img in coco['images']:
        iid      = img['id']
        cls_name = id_to_class.get(iid)
        if cls_name is None:
            continue
        if cls_name not in class_to_idx:
            continue
        img_path = os.path.join(img_dir, id_to_file[iid])
        if not os.path.exists(img_path):
            continue
        samples.append((img_path, class_to_idx[cls_name]))

    return samples


# ─── STEP 2: PREPROCESS ───────────────────────────────────────────────────────
def load_image(path):
    img = cv2.imread(path)
    if img is None:
        return None
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    return img.astype(np.float32) / 255.0


def build_arrays(samples):
    X, y = [], []
    for path, label in samples:
        img = load_image(path)
        if img is None:
            continue
        X.append(img)
        y.append(label)
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.int32)


# ─── STEP 3: AUGMENTATION ─────────────────────────────────────────────────────
def augment(X, y, target_per_class=400):
    """Augment minority classes to balance the dataset."""
    import tensorflow as tf
    counts = Counter(y.tolist())
    print("\nClass distribution before augmentation:")
    for i, name in enumerate(CLASSES):
        print(f"  {name}: {counts.get(i, 0)}")

    X_aug, y_aug = list(X), list(y)

    for cls_idx in range(len(CLASSES)):
        cls_count = counts.get(cls_idx, 0)
        if cls_count >= target_per_class:
            continue
        needed = target_per_class - cls_count
        cls_images = X[y == cls_idx]
        if len(cls_images) == 0:
            continue

        for _ in range(needed):
            img = cls_images[np.random.randint(len(cls_images))].copy()
            # Random augmentations
            if np.random.random() > 0.5:
                img = np.fliplr(img)
            if np.random.random() > 0.5:
                img = np.flipud(img)
            # Random brightness
            img = np.clip(img * np.random.uniform(0.7, 1.3), 0, 1)
            # Random rotation
            angle = np.random.uniform(-20, 20)
            M = cv2.getRotationMatrix2D((IMG_SIZE//2, IMG_SIZE//2), angle, 1.0)
            img = cv2.warpAffine(img, M, (IMG_SIZE, IMG_SIZE))
            X_aug.append(img)
            y_aug.append(cls_idx)

    X_aug = np.array(X_aug, dtype=np.float32)
    y_aug = np.array(y_aug, dtype=np.int32)

    # Shuffle
    idx = np.random.permutation(len(X_aug))
    print("\nClass distribution after augmentation:")
    counts2 = Counter(y_aug.tolist())
    for i, name in enumerate(CLASSES):
        print(f"  {name}: {counts2.get(i, 0)}")

    return X_aug[idx], y_aug[idx]


# ─── STEP 4: BUILD MODEL ──────────────────────────────────────────────────────
def build_model(num_classes):
    import tensorflow as tf
    from tensorflow.keras import layers, models

    base = tf.keras.applications.MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    base.trainable = False

    inputs = tf.keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
    x = base(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dropout(0.4)(x)
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)

    model = tf.keras.Model(inputs, outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-3),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model, base


# ─── STEP 5: TRAIN ────────────────────────────────────────────────────────────
def train():
    import tensorflow as tf

    print("=" * 55)
    print("AutoAid Damage Severity Classifier — Retraining")
    print("=" * 55)

    # Build class index
    global CLASSES
    CLASSES = list(CLASS_MAP.values())
    # Deduplicate while preserving order
    seen = set()
    CLASSES = [c for c in CLASSES if not (c in seen or seen.add(c))]
    class_to_idx = {c: i for i, c in enumerate(CLASSES)}
    num_classes  = len(CLASSES)
    print(f"\nClasses ({num_classes}): {CLASSES}")

    # Load splits
    print("\n[1/5] Loading dataset...")
    train_samples = load_dataset(
        os.path.join(DATASET_DIR, 'train', '_annotations.coco.json'),
        os.path.join(DATASET_DIR, 'train'),
        class_to_idx
    )
    val_samples = load_dataset(
        os.path.join(DATASET_DIR, 'valid', '_annotations.coco.json'),
        os.path.join(DATASET_DIR, 'valid'),
        class_to_idx
    )
    print(f"  Train: {len(train_samples)} images")
    print(f"  Val:   {len(val_samples)} images")

    print("\n[2/5] Preprocessing images...")
    X_train, y_train = build_arrays(train_samples)
    X_val,   y_val   = build_arrays(val_samples)
    print(f"  X_train: {X_train.shape}")
    print(f"  X_val:   {X_val.shape}")

    print("\n[3/5] Augmenting minority classes...")
    X_train, y_train = augment(X_train, y_train, target_per_class=400)

    print("\n[4/5] Building MobileNetV2 model...")
    model, base_model = build_model(num_classes)
    model.summary()

    os.makedirs('models', exist_ok=True)

    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            MODEL_SAVE, save_best_only=True,
            monitor='val_accuracy', mode='max', verbose=1
        ),
        tf.keras.callbacks.EarlyStopping(
            patience=10, restore_best_weights=True, verbose=1
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            factor=0.3, patience=4, min_lr=1e-6, verbose=1
        ),
    ]

    print(f"\n[5/5] Phase 1 — Training classifier head ({EPOCHS} epochs max)...")
    h1 = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=callbacks,
        verbose=1
    )

    # Fine-tune top layers
    print("\nPhase 2 — Fine-tuning top 30 base layers...")
    base_model.trainable = True
    for layer in base_model.layers[:-30]:
        layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-5),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    h2 = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=20,
        batch_size=BATCH_SIZE,
        callbacks=callbacks,
        verbose=1
    )

    # Save classes JSON
    with open(CLASSES_SAVE, 'w') as f:
        json.dump(CLASSES, f, indent=2)
    print(f"\nClasses saved to: {CLASSES_SAVE}")
    print(f"Model saved to:   {MODEL_SAVE}")

    # Plot
    plot_training(h1, h2)

    # Evaluate
    print("\nFinal evaluation on validation set:")
    loss, acc = model.evaluate(X_val, y_val, verbose=0)
    print(f"  Val accuracy: {acc:.1%}")
    print(f"  Val loss:     {loss:.4f}")

    return model


# ─── PLOT ─────────────────────────────────────────────────────────────────────
def plot_training(h1, h2=None):
    acc  = h1.history['accuracy']
    vacc = h1.history['val_accuracy']
    loss = h1.history['loss']
    vloss = h1.history['val_loss']

    if h2:
        acc   += h2.history['accuracy']
        vacc  += h2.history['val_accuracy']
        loss  += h2.history['loss']
        vloss += h2.history['val_loss']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    ax1.plot(loss,  label='Train'); ax1.plot(vloss, label='Val')
    ax1.set_title('Loss'); ax1.legend()
    ax2.plot(acc,   label='Train'); ax2.plot(vacc,  label='Val')
    ax2.set_title('Accuracy'); ax2.legend()
    plt.tight_layout()
    plt.savefig('models/training_curves.png')
    print("Training curves saved to models/training_curves.png")


# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    train()
    print("\n✅ Done!")
    print("Next steps:")
    print("  1. Copy models/damage_classifier.h5 to your Django ml_engine/models/ folder")
    print("  2. Copy models/damage_classifier_classes.json to the same folder")
    print("  3. Restart Django — image_infer.py will pick it up automatically")
