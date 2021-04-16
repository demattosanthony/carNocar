import cv2
from datetime import datetime
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--img', help='Image Path')
args = parser.parse_args()

def tuplify(listything):
    if isinstance(listything, list): return tuple(map(tuplify, listything))
    if isinstance(listything, dict): return {k:tuplify(v) for k,v in listything.items()}
    return listything

parking_spots = json.loads(open('coords.txt', 'r').read())
parking_spots = tuplify(parking_spots)

image_path = args.img
img = cv2.imread(image_path)

points = []
color = (255,0,0)
thickness = 2
font = cv2.FONT_HERSHEY_SIMPLEX

def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x,y))
        print('x = %d, y = %d'%(x, y))

cv2.namedWindow("image", cv2.WINDOW_NORMAL)   
cv2.resizeWindow("image", 1000,800)
cv2.setMouseCallback("image", onMouse)

while True:
    cv2.imshow('image', img)
    for key, spot in parking_spots.items():
        # cv2.circle(img, (spot['center'][0], spot['center'][1]), 20, color, thickness)
        # cv2.line(img, spot['tl'], spot['tr'], color, thickness)
        # cv2.line(img, spot['tr'], spot['br'], color, thickness)
        # cv2.line(img, spot['br'], spot['bl'], color, thickness)
        # cv2.line(img, spot['bl'], spot['tl'], color, thickness)
        # cv2.putText(img, str(key[4:]), spot['tl'], font, 1.5, color, thickness, cv2.LINE_AA)

        top_left_x = min([spot['tl'][0], spot['tr'][0], spot['br'][0], spot['bl'][0]])
        bot_right_x = max([spot['tl'][0], spot['tr'][0], spot['br'][0], spot['bl'][0]])
        top_left_y = min([spot['tl'][1], spot['tr'][1], spot['br'][1], spot['bl'][1]])
        bot_right_y = max([spot['tl'][1], spot['tr'][1], spot['br'][1], spot['bl'][1]])
        cropped_img = img[top_left_y:bot_right_y+1, top_left_x:bot_right_x+1]
        cropped_img = cv2.resize(cropped_img, (150,150))
        cv2.namedWindow('croppedImage', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('croppedImage', 150, 150)

        while True:
            cv2.imshow('croppedImage', cropped_img)

            k = cv2.waitKey(1)

            if k == ord('q'):
                cv2.destroyWindow('croppedImage')
                print('QUIT')
                break
            elif k == ord('o'):
                now = datetime.now().time()
                cv2.imwrite('data/open/'+str(now)+'.png', cropped_img)
                cv2.destroyWindow('croppedImage')
                print('Saved open spot')
                break
            elif k == ord('c'):
                now = datetime.now().time()
                cv2.imwrite('data/cars/'+str(now)+'.png', cropped_img)
                cv2.destroyWindow('croppedImage')
                print('Saved car ')
                break
    break
    if cv2.waitKey(10) == ord('q'):
        break
