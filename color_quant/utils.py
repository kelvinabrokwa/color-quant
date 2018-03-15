import sys
from sys import platform
from time import sleep

if platform == "linux2":
    from picamera import PiCamera
    from picamera.array import PiRGBArray
elif platform == "darwin":
    print("MacOS support to come")
    sys.exit(0)
else:
    print("Unsupported platform: {}".format(platform))
    sys.exit(1)


def get_image():
    """Returns an image as a numpy 3d BGR array
    """
    with PiCamera() as camera:
        with PiRGBArray(camera) as frame:
            # let camera warm up
            sleep(1)
            # capture photo
            camera.capture(frame, format="bgr")
            return frame.array
