<<<<<<< HEAD
# %%
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Dropout, Flatten, Dense
from tensorflow.keras import backend as K

from tensorflow.keras.layers import Input

import tensorflow as tf

img_width, img_height = 299, 299

# %%
train_data_dir = r"C:\TABLES_SANDBOX\model_data_v2\Train"
epochs = 200
batch_size = 8 # can be reduced to 16 to save memory

# %%
# check format of image
if K.image_data_format() == 'channels_first':
	input_shape = (3, img_width, img_height)
else:
	input_shape = (img_width, img_height, 3)

# This part is to check the data format i.e the RGB channel is coming first or last so, whatever it may be, the model will check first and then input shape will be fed accordingly.

# %%
model = Sequential([
    Input(shape=input_shape), 
    
    # First Convolutional Block
    Conv2D(32, (3, 3), padding='same', activation='relu'), 
    MaxPooling2D(pool_size=(2, 2)),
    
    # Second Convolutional Block
    Conv2D(32, (3, 3), padding='same', activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    
    # Third Convolutional Block
    Conv2D(64, (3, 3), padding='same', activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    
    # Flatten and Dense Layers
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(4, activation='softmax') # number of classes
])

# %%
# Define optimizer with customized parameters
optimizer = tf.keras.optimizers.Adam(
    learning_rate=0.0002, # for this run of the model, learning rate was reduced to 0.0002
    beta_1=0.9,
    beta_2=0.999,
    epsilon=1e-07
)

# Compile model with additional metrics
model.compile(
    optimizer=optimizer,
    loss='categorical_crossentropy',
    metrics=[
        'accuracy',
        tf.keras.metrics.Precision(name='precision'),
        tf.keras.metrics.Recall(name='recall'),
        tf.keras.metrics.AUC(name='auc'),
        tf.keras.metrics.F1Score(name='f1_score', threshold=0.5)
    ]
)

# %%
# Normalize the data (similar to rescale=1./255 in ImageDataGenerator)
normalization_layer = tf.keras.layers.Rescaling(1./255)

# Create training dataset
train_ds = tf.keras.utils.image_dataset_from_directory(
    train_data_dir,
    validation_split=0.2,
    subset='training',
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size,
    label_mode='categorical'  # this handles the one-hot encoding
)

# Create validation dataset
val_ds = tf.keras.utils.image_dataset_from_directory(
    train_data_dir,
    validation_split=0.2,
    subset='validation',
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size,
    label_mode='categorical'
)

# Apply normalization to the datasets
train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))

# Optimize the datasets for performance
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# %%
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

callbacks = [
    ModelCheckpoint('best_model_v2.keras', save_best_only=True, monitor='val_accuracy'),
    EarlyStopping(monitor='val_accuracy', patience=20)
]

model.fit(
    train_ds,
    epochs=epochs,
    validation_data=val_ds,
    callbacks=callbacks
)

# %%
model.save('model_saved.keras')
=======
# %%
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Dropout, Flatten, Dense
from tensorflow.keras import backend as K

from tensorflow.keras.layers import Input

import tensorflow as tf

img_width, img_height = 299, 299

# %%
train_data_dir = r"C:\TABLES_SANDBOX\model_data_v2\Train"
epochs = 200
batch_size = 8 # can be reduced to 16 to save memory

# %%
# check format of image
if K.image_data_format() == 'channels_first':
	input_shape = (3, img_width, img_height)
else:
	input_shape = (img_width, img_height, 3)

# This part is to check the data format i.e the RGB channel is coming first or last so, whatever it may be, the model will check first and then input shape will be fed accordingly.

# %%
model = Sequential([
    Input(shape=input_shape), 
    
    # First Convolutional Block
    Conv2D(32, (3, 3), padding='same', activation='relu'), 
    MaxPooling2D(pool_size=(2, 2)),
    
    # Second Convolutional Block
    Conv2D(32, (3, 3), padding='same', activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    
    # Third Convolutional Block
    Conv2D(64, (3, 3), padding='same', activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    
    # Flatten and Dense Layers
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(4, activation='softmax') # number of classes
])

# %%
# Define optimizer with customized parameters
optimizer = tf.keras.optimizers.Adam(
    learning_rate=0.0002, # for this run of the model, learning rate was reduced to 0.0002
    beta_1=0.9,
    beta_2=0.999,
    epsilon=1e-07
)

# Compile model with additional metrics
model.compile(
    optimizer=optimizer,
    loss='categorical_crossentropy',
    metrics=[
        'accuracy',
        tf.keras.metrics.Precision(name='precision'),
        tf.keras.metrics.Recall(name='recall'),
        tf.keras.metrics.AUC(name='auc'),
        tf.keras.metrics.F1Score(name='f1_score', threshold=0.5)
    ]
)

# %%
# Normalize the data (similar to rescale=1./255 in ImageDataGenerator)
normalization_layer = tf.keras.layers.Rescaling(1./255)

# Create training dataset
train_ds = tf.keras.utils.image_dataset_from_directory(
    train_data_dir,
    validation_split=0.2,
    subset='training',
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size,
    label_mode='categorical'  # this handles the one-hot encoding
)

# Create validation dataset
val_ds = tf.keras.utils.image_dataset_from_directory(
    train_data_dir,
    validation_split=0.2,
    subset='validation',
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size,
    label_mode='categorical'
)

# Apply normalization to the datasets
train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))

# Optimize the datasets for performance
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# %%
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

callbacks = [
    ModelCheckpoint('best_model_v2.keras', save_best_only=True, monitor='val_accuracy'),
    EarlyStopping(monitor='val_accuracy', patience=20)
]

model.fit(
    train_ds,
    epochs=epochs,
    validation_data=val_ds,
    callbacks=callbacks
)

# %%
model.save('model_saved.keras')
>>>>>>> 7f66c7c04acfc988496105081eacaa7d72433e18
