import torch
import json
import torchvision
import cv2
import torch.nn as nn
from PIL import Image

if torch.cuda.is_available():
    map_location='cuda'
else:
    map_location='cpu'

def tuplify(listything):
    if isinstance(listything, list): return tuple(map(tuplify, listything))
    if isinstance(listything, dict): return {k:tuplify(v) for k,v in listything.items()}
    return listything

parking_spots = json.loads(open('coords.txt', 'r').read())
parking_spots = tuplify(parking_spots)

image_path = '2021-02-03 15:58:06.854442.png'
img = cv2.imread(image_path)
img2 = Image.open(image_path).convert("RGB")

empty_color = (0,255,0)
taken_color = (0,0,255)
thickness = 2.5

font = cv2.FONT_HERSHEY_SIMPLEX

#model
class ApdNet(torch.nn.Module):
    def __init__(self):
        super(ApdNet, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.layer2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.drop_out = nn.Dropout()
        self.fc1 = nn.Linear(87616, 1000)
        self.fc2 = nn.Linear(1000, 2)
    def forward(self,x):
        #Max pooling over (2,2) window
        out = self.layer1(x)
        out = self.layer2(out)
        out = out.reshape(out.size(0), -1)
        out = self.drop_out(out)
        out = self.fc1(out)
        out = self.fc2(out)
        return out
    
    def num_flat_features(self,x):
        size = x.size()[1:]
        num_features = 1
        for s in size:
            num_features *= s
        return num_features

model = ApdNet()
model.load_state_dict(torch.load('models/my_data.pt', map_location=map_location))

while True:
    for key, spot in parking_spots.items():
        top_left_x = min([spot['tl'][0], spot['tr'][0], spot['br'][0], spot['bl'][0]])
        bot_right_x = max([spot['tl'][0], spot['tr'][0], spot['br'][0], spot['bl'][0]])
        top_left_y = min([spot['tl'][1], spot['tr'][1], spot['br'][1], spot['bl'][1]])
        bot_right_y = max([spot['tl'][1], spot['tr'][1], spot['br'][1], spot['bl'][1]])
        cropped_img = img[top_left_y:bot_right_y+1, top_left_x:bot_right_x+1]
        cropped_img = Image.fromarray(cropped_img)
        cropped_img_tns = torchvision.transforms.functional.resize(cropped_img, (150,150))
        cropped_img_tns = torchvision.transforms.functional.to_tensor(cropped_img_tns)
        cropped_img_tns = cropped_img_tns.unsqueeze(0)

        model.eval()
        with torch.no_grad():
            output = model(cropped_img_tns)
        if(torch.argmax(output) == 1):
          # Move car image 
        else:
          # Move open image 
    #Move image to labeled images and pick new image

