import torch
import json
import torchvision

def tuplify(listything):
    if isinstance(listything, list): return tuple(map(tuplify, listything))
    if isinstance(listything, dict): return {k:tuplify(v) for k,v in listything.items()}
    return listything

parking_spots = json.loads(open('coords.txt', 'r').read())
parking_spots = tuplify(parking_spots)

image_path = '2020-09-07 13:36:05.466150.png'
img = cv2.imread(image_path)

color = (255,0,0)
thickness = 2.5

font = cv2.FONT_HERSHEY_SIMPLEX

model = torch.load('cnr_car_combined_model.pt')
model.eval()

while True:
    cv2.imshow('img', img)

    for key, spot in parking_spots.items():
        top_left_x = min([spot['tl'][0], spot['tr'][0], spot['br'][0], spot['bl'][0]])
        bot_right_x = max([spot['tl'][0], spot['tr'][0], spot['br'][0], spot['bl'][0]])
        top_left_y = min([spot['tl'][1], spot['tr'][1], spot['br'][1], spot['bl'][1]])
        bot_right_y = max([spot['tl'][1], spot['tr'][1], spot['br'][1], spot['bl'][1]])
        cropped_img = img[top_left_y:bot_right_y+1, top_left_x:bot_right_x+1]

        cropped_img_tns = torchvision.transforms.functional.resize(cropped_img, (150,150))
        cropped_img_tns = torchvision.transforms.functional.to_tensor(cropped_img_tns)
        cropped_img_tns = cropped_img_tns.unsqueeze(0)

        with torch.no_grad():
            output = model(cropped_img_tns)
        print(output)
    if cv2.waitKey(1) == ord('q'):
        break