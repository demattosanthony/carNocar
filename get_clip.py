import cv2
import threading
from threading import Thread
import os
from datetime import datetime
import schedule
import time

SOURCE = 'rtsp://admin:HPUcarcam1@10.33.99.30:554/h264Preview_01_main'

# datetime object containing current date and time

class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src,cv2.CAP_FFMPEG)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):   
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def stop(self):
        self.stopped = True
        self.stream.release()


def getImage():
    now = datetime.now()
    video_getter = VideoGet(SOURCE).start()
    frame_width = int(video_getter.stream.get(3))
    frame_height = int(video_getter.stream.get(4))

    #out = cv2.VideoWriter('data/videos/{}.avi'.format(now),cv2.VideoWriter_fourcc(*'MJPG'), 10, (frame_width,frame_height))

    frame = video_getter.frame
    if not cv2.imwrite('couch_pklot_images/{}.png'.format(now), frame):
        raise Exception("Could not write image")

    print('Getting image')

    '''
    while (True):
        frame = video_getter.frame

        out.write(frame)
        
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        #cv2.startWindowThread()
        cv2.resizeWindow('frame', 1200, 600)
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    '''
    video_getter.stopped=True
    #out.release()
    cv2.destroyAllWindows()

getImage()
schedule.every(45).minutes.do(getImage)

while True:
    
    schedule.run_pending()
    time.sleep(1)

