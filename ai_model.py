import numpy as np

from sklearn import preprocessing
from cv2 import CascadeClassifier
from tensorflow.keras.models import load_model
# from openvino.inference_engine import IECore

class AIModel():

    detector = None
    classifier = None
    # modelLocation = 'files/vromeo_ai_model.h5'
    classes = 'files/vromeo_ai_model_classes.npy'
    ieModelProperties = []
    label = ''
    
    def __init__(self, recognition = True, ie = False, model_location = 'files/vromeo_ai_model.h5'):
        # Face detector
        self.detector = CascadeClassifier("haarcascade_frontalface_default.xml")
        self.modelLocation = model_location
        self.classes = np.load(self.classes)
        if recognition:
            self.label = preprocessing.LabelEncoder()
            self.label.classes_ = self.classes
            if model_location != '':
                if ie:
                    # Use intel inference engine
                    self.classifier = self.create_inference_engine(self.modelLocation)
                else:
                    print('t')
                    # Use regular tf / keras model
                    self.classifier = load_model(self.modelLocation)
                    print(f'classifier : {self.classifier}')
            else:
                print ('Model location is not set')
        else:
            print("recognition tida aktif")
    
    def create_inference_engine(self, model_location):
        ie = IECore()
        net  = ie.read_network(model = model_location)
        input_name = next(iter(net.input_info))
        output_name = next(iter(net.outputs))
        self.ieModelProperties = input_name, output_name
        try:
            model = ie.load_network(network = self.ieModelLocation, device_name = "MYRIAD")
            print ("USE NCS2 VPU")
        except:
            model = ie.load_network(network = self.ieModelLocation, device_name = "CPU")
            print ("NCS2 not found, use CPU...")
        
        return model