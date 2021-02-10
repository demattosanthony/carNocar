import cv2
from datetime import datetime
import json

def tuplify(listything):
    if isinstance(listything, list): return tuple(map(tuplify, listything))
    if isinstance(listything, dict): return {k:tuplify(v) for k,v in listything.items()}
    return listything

parking_spots = json.loads(open('coords.txt', 'r').read())
parking_spots = tuplify(parking_spots)

image_path = '2020-09-07 13:36:05.466150.png'
img = cv2.imread(image_path)

points = []
color = (255,0,0)
thickness = 5

def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x,y))
        print('x = %d, y = %d'%(x, y))

cv2.namedWindow("image", cv2.WINDOW_NORMAL)   
cv2.resizeWindow("image", 1000,800)
cv2.setMouseCallback("image", onMouse)

font = cv2.FONT_HERSHEY_SIMPLEX
while True:
    cv2.imshow('image', img)
    for key, spot in parking_spots.items():
        # cv2.circle(img, (spot['center'][0], spot['center'][1]), 20, color, thickness)
        # cv2.line(img, spot['tl'], spot['tr'], color, thickness)
        # cv2.line(img, spot['tr'], spot['br'], color, thickness)
        # cv2.line(img, spot['br'], spot['bl'], color, thickness)
        # cv2.line(img, spot['bl'], spot['tl'], color, thickness)
        # cv2.putText(img, str(key[4:]), spot['tl'], font, 3, color, thickness, cv2.LINE_AA)

        top_left_x = min([spot['tl'][0], spot['tr'][0], spot['br'][0], spot['bl'][0]])
        bot_right_x = max([spot['tl'][0], spot['tr'][0], spot['br'][0], spot['bl'][0]])
        top_left_y = min([spot['tl'][1], spot['tr'][1], spot['br'][1], spot['bl'][1]])
        bot_right_y = max([spot['tl'][1], spot['tr'][1], spot['br'][1], spot['bl'][1]])
        cropped_img = img[top_left_y:bot_right_y+1, top_left_x:bot_right_x+1]
        cv2.namedWindow('croppedImage', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('croppedImage', 800, 800)

        while True:
            cv2.imshow('croppedImage', cropped_img)
            if cv2.waitKey(1) == ord('q'):
                cv2.destroyWindow('croppedImage')
                print('QUIT')
                break
            elif cv2.waitKey(1) == ord('o'):
                now = datetime.now().time()
                cv2.imwrite('data/open/'+str(now)+'.png', cropped_img)
                cv2.destroyWindow('croppedImage')
                print('Saved open spot')
                break
            elif cv2.waitKey(1) == ord('c'):
                now = datetime.now().time()
                cv2.imwrite('data/cars/'+str(now)+'.png', cropped_img)
                cv2.destroyWindow('croppedImage')
                print('Saved car ')
                break
    if cv2.waitKey(10) == ord('q'):
        break