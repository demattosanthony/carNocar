import torch
import json
import torchvision
import cv2
import torch.nn as nn
import torchvision.models as models
from PIL import Image
import argparse
import threading
from threading import Thread
from database import *

parser = argparse.ArgumentParser()
parser.add_argument('--live', help='Live video if true / img if false', default='True')
parser.add_argument('--img', help='image path', default=False)
parser.add_argument('--showOutput', help='Show opencv output window', default=True)
args = parser.parse_args()

#consts
empty_color = (0,255,0)
taken_color = (0,0,255)
thickness = 2.5
font = cv2.FONT_HERSHEY_SIMPLEX

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

SOURCE = 'rtsp://admin:HPUcarcam1@10.33.99.30:554/h264Preview_01_main'

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

def tuplify(listything):
    if isinstance(listything, list): return tuple(map(tuplify, listything))
    if isinstance(listything, dict): return {k:tuplify(v) for k,v in listything.items()}
    return listything

def run_through_model(image_tns, image, spot, model, spots_ref):
    spotId = 'spot'+str(spot['id'])
    model.eval()
    with torch.no_grad():
        output = model(image_tns)
    if(torch.argmax(output) == 1):
        cv2.line(image, spot['tl'], spot['tr'], taken_color, 2)
        cv2.line(image, spot['tr'], spot['br'], taken_color, 2)
        cv2.line(image, spot['br'], spot['bl'], taken_color, 2)
        cv2.line(image, spot['bl'], spot['tl'], taken_color, 2)
        if spots_ref[spotId] == 'open':
            set_spot_status('taken', spotId)
            print('update')
    else:
        cv2.line(image, spot['tl'], spot['tr'], empty_color, 2)
        cv2.line(image, spot['tr'], spot['br'], empty_color, 2)
        cv2.line(image, spot['br'], spot['bl'], empty_color, 2)
        cv2.line(image, spot['bl'], spot['tl'], empty_color, 2)
        if spots_ref[spotId] == 'taken':
            set_spot_status('open', spotId)
            print('update')
    
    if args.showOutput == True:
        cv2.namedWindow('img', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('img', 1200, 800)
        cv2.imshow('img', image)

def zoom_on_spots(image, parking_spots, model, spots_ref):
    for key, spot in parking_spots.items():
        top_left_x = min([spot['tl'][0], spot['tr'][0], spot['br'][0], spot['bl'][0]])
        bot_right_x = max([spot['tl'][0], spot['tr'][0], spot['br'][0], spot['bl'][0]])
        top_left_y = min([spot['tl'][1], spot['tr'][1], spot['br'][1], spot['bl'][1]])
        bot_right_y = max([spot['tl'][1], spot['tr'][1], spot['br'][1], spot['bl'][1]])
        cropped_img = image[top_left_y:bot_right_y+1, top_left_x:bot_right_x+1]
        cropped_img = Image.fromarray(cropped_img)
        # cropped_img = img2.crop()

        cropped_img_tns = torchvision.transforms.functional.resize(cropped_img, (150,150))
        cropped_img_tns = torchvision.transforms.functional.to_tensor(cropped_img_tns)
        cropped_img_tns = cropped_img_tns.unsqueeze(0).to(device)

        run_through_model(cropped_img_tns, image, spot, model, spots_ref)

def main():
    #load model
    model = models.resnet18(pretrained=True)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, 2)
    model.to(device)
    model.load_state_dict(torch.load('models/my_data2.pt', map_location=device))

    #load all parking spot locations
    parking_spots = json.loads(open('coords.txt', 'r').read())
    parking_spots = tuplify(parking_spots)

    # live video feed
    if(args.live == 'True'):
        print('live')
        video_getter = VideoGet(SOURCE).start()
        while True:
            frame = video_getter.frame
            zoom_on_spots(frame, parking_spots, model, spots_ref)

            if cv2.waitKey(1) == ord('q'):
                break
    # image 
    else:
        image_path = args.img
        img = cv2.imread(image_path)
        img2 = Image.open(image_path).convert("RGB")
        while True:
            zoom_on_spots(img, parking_spots, model, spots_ref)
            
            if cv2.waitKey(0) == ord('q'):
                break

if __name__ == '__main__':
    main()
