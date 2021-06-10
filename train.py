import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
import torchvision
import torch.nn as nn
import torchvision.models as models
import os
from PIL import Image
import matplotlib.pyplot as plt
from tqdm import trange


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

PATH = os.path.abspath(os.getcwd())

class CustomDset(Dataset):
    def __init__(self, root_dir, transform):
        self.root_dir = root_dir
        self.images = os.listdir(root_dir)
        self.transform = transform

    def __len__(self):
        return len(os.listdir(self.root_dir))

    def __getitem__(self, index):
        img_loc = os.path.join(self.root_dir,self.images[index])
        img = Image.open(img_loc).convert("RGB")
        label = 1 if os.path.basename(self.root_dir) == 'cars' else 0
        label = torch.tensor(label).to(device)

        if self.transform is not None:
            img = self.transform(img).to(device)
#             img = img.reshape((3,150,150))

        return img,label


tfms = torchvision.transforms.Compose([
    torchvision.transforms.Resize((150,150)),
    torchvision.transforms.ToTensor()])
carDset = CustomDset(PATH+'/data/cars', transform=tfms)
openDset = CustomDset(PATH+'/data/open', transform=tfms)

concat_dataset = torch.utils.data.ConcatDataset([carDset,openDset,openDset])
lengths = [int(len(concat_dataset)*0.8), int(len(concat_dataset)*0.2)]
train_set, val_set = torch.utils.data.random_split(concat_dataset, lengths)
train_loader = DataLoader(train_set,batch_size=8,shuffle=True)

train_iter = iter(train_loader)
images,labels = train_iter.next()

model = models.resnet18(pretrained=True)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 2)
model.to(device)

loss_list, acc_list = [],[]
loss_func = nn.CrossEntropyLoss().to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
num_epochs = 2
total_step = len(train_loader)
for epoch in range(num_epochs):
    for i, (images, labels) in enumerate(train_loader):
        outputs = model(images)
#         label = torch.max(labels,1)[1]

        loss = loss_func(outputs,labels)
        loss_list.append(loss.item())

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total = labels.size(0)
        _, predicted = torch.max(outputs.data,1)
        correct = (predicted == labels).sum().item()
        acc_list.append(correct/total)

        print('Epoch [{}/{}], Step [{},{}], Loss: {:.4f}, Accuracy: {:.2f}%'
                .format(epoch+1, num_epochs, i+1, total_step, loss.item(),
                       (correct/total)*100))

plt.ylim(-0.1,1.1)
plt.plot(loss_list)
plt.plot(acc_list)


model.eval()
accuracy_list = []
for img, label in val_set:
    img = img.unsqueeze(0)
    with torch.no_grad():
        output = model(img)
    predicted = torch.argmax(output)
    correct = 1 if predicted == label else 0
    accuracy_list.append(correct)

acc = sum(accuracy_list)/len(val_set)
print(acc)

sm = torch.jit.script(model)
sm.save("carClassify.pt")
#torch.save(model, './entireModel.pt')
