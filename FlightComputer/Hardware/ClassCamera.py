from ClassAbstractHardware import ClassAbstractHardware
from picamera import PiCamera
from picamera.array import PiRGBArray
import time


class ClassCamera(ClassAbstractHardware):

    def __init__(self):
        super().__init__()
        self.image = None

    def _connect(self, device):
        self.camera = PiCamera()
        # allow the camera to warmup
        time.sleep(0.1)
        return True

    def _disconnect(self):
        self.camera.stop_preview()
        self.camera.close()
        return False

    def _getData(self):
        try:
            rawCapture = PiRGBArray(self.camera)
            self.camera.capture(rawCapture, format="bgr", use_video_port=True)
            self.image = rawCapture.array
            success = True
        except:
            success = False
        return success

    def _setData(self):
        print('Cannot write anything to camera!')
        return False
