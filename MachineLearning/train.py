if __name__ == '__main__': from __init__ import *
else: from . import *
from datetime import date

from tensorflow.python.keras import activations

def make_model(input_shape, classes, chckpnt=False, load=False):

    inputs = keras.Input(shape=(*input_shape, 3))
    x = data_augmentation(inputs)
    x = layers.experimental.preprocessing.Rescaling(1./255)(x)
    
    if isinstance(load, str): 
        model = keras.models.load_model(MODELS / f'{load}.hdf5')(x)
    
    else:
        if load == 0:
            x = layers.Conv2D(32, 3, activation='relu')(x)
            x = layers.MaxPooling2D()(x)
            x = layers.Conv2D(32, 3, activation='relu')(x)
            x = layers.MaxPooling2D()(x)
            x = layers.Conv2D(32, 3, activation='relu')(x)
            x = layers.MaxPooling2D()(x)
            x = layers.Flatten()(x)
            x = layers.Dense(128, activation='relu')(x)
        
        elif load == 1:
            # Entry block
            x = layers.Conv2D(32, 3, strides=2, padding='same')(x)
            x = layers.BatchNormalization()(x)
            x = layers.Activation('relu')(x)

            x = layers.Conv2D(64, 3, padding='same')(x)
            x = layers.BatchNormalization()(x)
            x = layers.Activation('relu')(x)

            previous_block_activation = x  # Set aside residual
            
            for size in [128, 256, 512, 728]:

                x = layers.Activation('relu')(x)
                x = layers.SeparableConv2D(size, 3, padding='same')(x)
                x = layers.BatchNormalization()(x)

                x = layers.Activation('relu')(x)
                x = layers.SeparableConv2D(size, 3, padding='same')(x)
                x = layers.BatchNormalization()(x)

                x = layers.MaxPooling2D(3, strides=2, padding='same')(x)
                
                # Project residual
                residual = layers.Conv2D(
                    size, 1, strides=2, padding='same')(previous_block_activation
                    )
                x = layers.add([x, residual])  # Add back residual
                previous_block_activation = x  # Set aside next residual

            x = layers.SeparableConv2D(1024, 3, padding='same')(x)
            x = layers.BatchNormalization()(x)
            x = layers.Activation('relu')(x)
            
            x = layers.GlobalAveragePooling2D()(x)
        
        elif load == 2:
            x = layers.Conv2D(32, (3, 3), padding='same')(x)
            x = layers.Activation('relu')(x)
            x = layers.BatchNormalization()(x)
            x = layers.MaxPooling2D(pool_size=(3, 3))(x)
            x = layers.Dropout(0.25)(x)
            x = layers.Conv2D(64, (3, 3), padding='same')(x)
            x = layers.Activation('relu')(x)
            x = layers.BatchNormalization()(x)
            x = layers.Conv2D(64, (3, 3), padding='same')(x)
            x = layers.Activation('relu')(x)
            x = layers.BatchNormalization()(x)
            x = layers.MaxPooling2D(pool_size=(2, 2))(x)
        
        # if classes == 2: activation, units = 'sigmoid', classes
        # else: activation, units = 'softmax', classes
        
        x = layers.Dropout(0.5)(x)
        outputs = layers.Dense(classes, activation='relu')(x)
        model = keras.Model(inputs, outputs)
        
    if chckpnt:
        
        checkpoints = list(CHCKPNT.glob(f'{NAME}*'))
        model.load_weights(checkpoints[-1])
    
    return model

def cleanup(num_skipped=0):

    import PIL
    
    for folder in DATA.iterdir():

        for path in folder.iterdir():
            
            try: 
                jfif = tf.compat.as_bytes('JFIF') in path.read_bytes()
                size = PIL.Image.open(path).size == (512, 512)
            except PIL.UnidentifiedImageError: jfif = size = False
            
            if not jfif or not size:
                path.unlink()
                num_skipped += 1
                                
    print(f'Deleted {num_skipped} images\n')

def decompose(epoch):

    factors = [i for i in range(2, epoch) if epoch%i == 0]
    total = len(factors)

    if total % 2: return factors[total // 2], factors[total // 2]
    else: return factors[(total // 2) - 1:(total // 2) + 1]

NAME, VERSION = 'Medium', 1
DATA = Path(r'E:\Users\Emc11\Training') / NAME
IMAGE_SIZE = 180, 180
BATCH = 32
saves, epochs = decompose(16)
# cleanup()

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    str(DATA), validation_split=0.2, subset='training', 
    seed=1337, image_size=IMAGE_SIZE, batch_size=BATCH
    )
val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    str(DATA), validation_split=0.2, subset='validation', 
    seed=1337, image_size=IMAGE_SIZE, batch_size=BATCH
    )

data_augmentation = keras.Sequential([
    layers.experimental.preprocessing.RandomFlip(),
    layers.experimental.preprocessing.RandomRotation(0.33),
    layers.experimental.preprocessing.RandomZoom(
        height_factor=(-0.3, -0.1),
         width_factor=(-0.3, -0.1)
        ),
    ])
augmented_train_ds = train_ds.map(
    lambda x, y: (data_augmentation(x, training=True), y)
    )

train_ds = train_ds.prefetch(buffer_size=32)
val_ds = val_ds.prefetch(buffer_size=32)

checkpoint = keras.callbacks.ModelCheckpoint(
    CHCKPNT / f'{NAME}_{{epoch:02}}.hdf5', save_frequency=saves
    )
tensorboard = tf.keras.callbacks.TensorBoard(
    log_dir=LOGS / f'{date.today()}', histogram_freq=1
    )

model = make_model(IMAGE_SIZE, classes=2, chckpnt=True, load=0)
model.compile(
    optimizer=keras.optimizers.Adam(1e-3),
    loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
    )

for save in range(saves):
        
    model.fit(
        train_ds, epochs=epochs + save*epochs, 
        callbacks=[checkpoint, tensorboard], 
        validation_data=val_ds,
        initial_epoch=save*epochs
        )
    model.save(MODELS / f'{NAME}-{VERSION:02}.hdf5', save_format='h5')
