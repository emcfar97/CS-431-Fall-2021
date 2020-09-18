from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QFormLayout, QLabel, QLineEdit, QComboBox, QMessageBox, QDesktopWidget, QStatusBar

layers = {
    'AbstractRNNCell': {},
    'Activation': {},
    'ActivityRegularization': {},
    'Add': {},
    'add': {},
    'AdditiveAttention': {},
    'AlphaDropout': {},
    'Attention': {},
    'Average': {},
    'average': {},
    'AveragePooling1D': {},
    'AveragePooling2D': {},
    'AveragePooling3D': {},
    'BatchNormalization': {},
    'Bidirectional': {},
    'Concatenate': {},
    'concatenate': {},
    'Conv1D': {},
    'Conv1DTranspose': {},
    'Conv2D': {},
    'Conv2DTranspose': {},
    'Conv3D': {},
    'Conv3DTranspose': {},
    'ConvLSTM2D': {},
    'Cropping1D': {},
    'Cropping2D': {},
    'Cropping3D': {},
    'Dense': {},
    'DenseFeatures': {},
    'DepthwiseConv2D': {},
    'deserialize': {},
    'Dot': {},
    'dot': {},
    'Dropout': {},
    'ELU': {},
    'Embedding': {},
    'Flatten': {},
    'GaussianDropout': {},
    'GaussianNoise': {},
    'GlobalAveragePooling1D': {},
    'GlobalAveragePooling2D': {},
    'GlobalAveragePooling3D': {},
    'GlobalMaxPool1D': {},
    'GlobalMaxPool2D': {},
    'GlobalMaxPool3D': {},
    'GRU': {},
    'GRUCell': {},
    'InputLayer': {},
    'InputSpec': {},
    'Lambda': {},
    'Layer': {},
    'LayerNormalization': {},
    'LeakyReLU': {},
    'LocallyConnected1D': {},
    'LocallyConnected2D': {},
    'LSTM': {},
    'LSTMCell': {},
    'Masking': {},
    'Maximum': {},
    'maximum': {},
    'MaxPool1D': {},
    'MaxPool2D': {},
    'MaxPool3D': {},
    'Minimum': {},
    'minimum': {},
    'MultiHeadAttention': {},
    'Multiply': {},
    'multiply': {},
    'Permute': {},
    'PReLU': {},
    'ReLU': {},
    'RepeatVector': {},
    'Reshape': {},
    'RNN': {},
    'SeparableConv1D': {},
    'SeparableConv2D': {},
    'serialize': {},
    'SimpleRNN': {},
    'SimpleRNNCell': {},
    'Softmax': {},
    'SpatialDropout1D': {},
    'SpatialDropout2D': {},
    'SpatialDropout3D': {},
    'StackedRNNCells': {},
    'Subtract': {},
    'subtract': {},
    'ThresholdedReLU': {},
    'TimeDistributed': {},
    'UpSampling1D': {},
    'UpSampling2D': {},
    'UpSampling3D': {},
    'Wrapper': {},
    'ZeroPadding1D': {},
    'ZeroPadding2D': {},
    'ZeroPadding3D': {},
    'experimental': {
        'EinsumDense': {},
        'RandomFourierFeatures': {},
        'SyncBatchNormalization': {},
        'preprocessing': {
            'CategoryCrossing': {},
            'CategoryEncoding': {},
            'CenterCrop': {},
            'Discretization': {},
            'Hashing': {},
            'IntegerLookup': {},
            'Normalization': {},
            'PreprocessingLayer': {},
            'RandomContrast': {},
            'RandomCrop': {},
            'RandomFlip': {},
            'RandomHeight': {},
            'RandomRotation': {},
            'RandomTranslation': {},
            'RandomWidth': {},
            'RandomZoom': {},
            'Rescaling': {},
            'Resizing': {},
            'StringLookup': {},
            'TextVectorization': {},
            }
        }
    }

class Inspector(QWidget):

    def __init__(self): pass

class Palette(QWidget):

    def __init__(self): pass

class Layer(QWidget): 
    
    def __init__(self): pass


Qapp = QApplication([])

layer = Layer()
layer.show()

Qapp.exec_()