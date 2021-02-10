import cv2
import json
import argparse

def tuplify(listything):
    if isinstance(listything, list): return tuple(map(tuplify, listything))
    if isinstance(listything, dict): return {k:tuplify(v) for k,v in listything.items()}
    return listything

parking_spots = json.loads(open('test.txt', 'r').read())
parking_spots = tuplify(parking_spots)

image_path = '2020-09-07 13:36:05.466150.png'
img = cv2.imread(image_path)

coords = {}
iterator = 0
touch_point = 0

color = (255,0,0)
thickness = 2.5

brk = False
def onMouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        if params == -1:
            print('x = {}, y = {}'.format(x,y))
            global iterator
            global touch_point
            global coords
            spotId = "spot" + str(iterator)
            if touch_point == 0: 
                coords[spotId] = {}
            coords[spotId]["id"] = iterator
            if touch_point == 0:
                coords[spotId]["tl"] = (x,y)
            elif touch_point == 1:
                coords[spotId]["tr"] = (x,y)
            elif touch_point == 2:
                coords[spotId]["bl"] = (x,y)
            elif touch_point == 3:
                coords[spotId]["br"] = (x,y)
            touch_point += 1
            if touch_point > 3:
                touch_point = 0
                iterator += 1
        else: 
            global brk
            spotId = "spot" + params
            if touch_point == 0:
                parking_spots[spotId]['tl'] = (x,y)
            elif touch_point == 1:
                parking_spots[spotId]['tr'] = (x,y)
            elif touch_point == 2:
                parking_spots[spotId]['bl'] = (x,y)
            elif touch_point == 3:
                parking_spots[spotId]['br'] = (x,y)
            touch_point += 1
            if touch_point > 3:
                coords = parking_spots
                brk = True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--spot', default=-1, help='spot id')
    args = parser.parse_args()
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('img', 1000,800)
    cv2.setMouseCallback('img', onMouse, args.spot)
    while True:
        cv2.imshow('img', img)
        global brk
        if cv2.waitKey(33) == ord('q') or brk == True:
            json.dump(coords, open('test.txt', 'w'))
            break

if __name__ == '__main__':
    main()

