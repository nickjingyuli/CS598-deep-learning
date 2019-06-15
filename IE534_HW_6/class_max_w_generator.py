import torch
import torchvision
import torchvision.transforms as transforms
from torch.autograd import Variable
import matplotlib
matplotlib.use('Agg')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import torch.nn as nn
import torch.nn.functional as F

######################## Synthetic Images Maximizing Classification Output ####################
batch_size = 128


class discriminator(nn.Module):
    def __init__(self):
        super(discriminator, self).__init__()
        self.conv1 = nn.Conv2d(3, 196, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(196, 196, kernel_size=3, stride=2, padding=1)
        self.conv3 = nn.Conv2d(196, 196, kernel_size=3, stride=1, padding=1)
        self.conv4 = nn.Conv2d(196, 196, kernel_size=3, stride=2, padding=1)
        self.conv5 = nn.Conv2d(196, 196, kernel_size=3, stride=1, padding=1)
        self.conv6 = nn.Conv2d(196, 196, kernel_size=3, stride=1, padding=1)
        self.conv7 = nn.Conv2d(196, 196, kernel_size=3, stride=1, padding=1)
        self.conv8 = nn.Conv2d(196, 196, kernel_size=3, stride=2, padding=1)
        self.pool = nn.MaxPool2d(4, 4)
        self.fc1 = nn.Linear(196, 1)
        self.fc10 = nn.Linear(196, 10)
        self.ln1 = nn.LayerNorm((196, 32, 32))
        self.ln2 = nn.LayerNorm((196, 16, 16))
        self.ln3 = nn.LayerNorm((196, 16, 16))
        self.ln4 = nn.LayerNorm((196, 8, 8))
        self.ln5 = nn.LayerNorm((196, 8, 8))
        self.ln6 = nn.LayerNorm((196, 8, 8))
        self.ln7 = nn.LayerNorm((196, 8, 8))
        self.ln8 = nn.LayerNorm((196, 4, 4))

    def forward(self, x):
        x = self.conv1(x)
        x = self.ln1(x)
        x = F.leaky_relu(x)

        x = self.conv2(x)
        x = self.ln2(x)
        x = F.leaky_relu(x)

        x = self.conv3(x)
        x = self.ln3(x)
        x = F.leaky_relu(x)

        # conv4
        x = self.conv4(x)
        x = self.ln4(x)
        x = F.leaky_relu(x)

        # conv5
        x = self.conv5(x)
        x = self.ln5(x)
        x = F.leaky_relu(x)

        # conv6
        x = self.conv6(x)
        x = self.ln6(x)
        x = F.leaky_relu(x)

        # conv7
        x = self.conv7(x)
        x = self.ln7(x)
        x = F.leaky_relu(x)

        # conv8
        x = self.conv8(x)
        x = self.ln8(x)
        x = F.leaky_relu(x)

        x = self.pool(x)
        output = x.view(-1, 196)
        output1 = self.fc1(output)
        output2 = self.fc10(output)

        return output1, output2

###### Generator network Archetecture
class generator(nn.Module):
    def __init__(self):
        super(generator, self).__init__()
        self.fc1 = nn.Linear(100, 196 * 4 * 4)
        self.conv1 = nn.ConvTranspose2d(196, 196, kernel_size=4, stride=2, padding=1)
        self.conv2 = nn.Conv2d(196, 196, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(196, 196, kernel_size=3, stride=1, padding=1)
        self.conv4 = nn.Conv2d(196, 196, kernel_size=3, stride=1, padding=1)
        self.conv5 = nn.ConvTranspose2d(196, 196, kernel_size=4, stride=2, padding=1)
        self.conv6 = nn.Conv2d(196, 196, kernel_size=3, stride=1, padding=1)
        self.conv7 = nn.ConvTranspose2d(196, 196, kernel_size=4, stride=2, padding=1)
        self.conv8 = nn.Conv2d(196, 3, kernel_size=3, stride=1, padding=1)
        self.batchnorm0 = nn.BatchNorm1d(196 * 4 * 4)
        self.batchnorm1 = nn.BatchNorm2d(196)
        self.batchnorm2 = nn.BatchNorm2d(196)
        self.batchnorm3 = nn.BatchNorm2d(196)
        self.batchnorm4 = nn.BatchNorm2d(196)
        self.batchnorm5 = nn.BatchNorm2d(196)
        self.batchnorm6 = nn.BatchNorm2d(196)
        self.batchnorm7 = nn.BatchNorm2d(196)

    def forward(self, x):
        x = self.fc1(x)
        x = self.batchnorm0(x)
        x = x.view(-1, 196, 4, 4)

        # conv1
        x = self.conv1(x)
        x = self.batchnorm1(F.relu(x))

        # conv2
        x = self.conv2(x)
        x = self.batchnorm2(F.relu(x))

        # conv3
        x = self.conv3(x)
        x = self.batchnorm3(F.relu(x))

        # conv4
        x = self.conv4(x)
        x = self.batchnorm4(F.relu(x))

        # conv5
        x = self.conv5(x)
        x = self.batchnorm5(F.relu(x))

        # conv6
        x = self.conv6(x)
        x = self.batchnorm6(F.relu(x))

        # conv7
        x = self.conv7(x)
        x = self.batchnorm7(F.relu(x))

        # conv8
        x = self.conv8(x)
        x = torch.tanh(x)
        return x

###### plot a 10 by 10 grid of images scaled between 0 and 1
def plot(samples):
    fig = plt.figure(figsize=(10, 10))
    gs = gridspec.GridSpec(10, 10)
    gs.update(wspace=0.02, hspace=0.02)

    for i, sample in enumerate(samples):
        ax = plt.subplot(gs[i])
        plt.axis('off')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_aspect('equal')
        plt.imshow(sample)
    return fig

###### Use the same plot function from the previous section and load your discriminator model trained without the generator.
transform_test = transforms.Compose([
    transforms.CenterCrop(32),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
])

testset = torchvision.datasets.CIFAR10(root='./', train=False, download=False, transform=transform_test)
testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=False, num_workers=8)
testloader = enumerate(testloader)

model = torch.load('tempD.model')
model.cuda()
model.eval()

###### Grab a sample batch from the test dataset. Create an alternative label which is simply +1 to the true label.
batch_idx, (X_batch, Y_batch) = testloader.__next__()
X_batch = Variable(X_batch,requires_grad=True).cuda()
Y_batch_alternate = (Y_batch + 1)%10
Y_batch_alternate = Variable(Y_batch_alternate).cuda()
Y_batch = Variable(Y_batch).cuda()


###### After loading in a model and a batch of images, calculate the mean image and make 10 copies (for num classes).
###### Make a unique label for each copy.
X = X_batch.mean(dim=0)
X = X.repeat(10,1,1,1)

Y = torch.arange(10).type(torch.int64)
Y = Variable(Y).cuda()

###### The model evaluates the images and extracts the output from the fc10 layer for each particular class.
lr = 0.1
weight_decay = 0.001
for i in range(200):
    _, output = model(X)

    loss = -output[torch.arange(10).type(torch.int64),torch.arange(10).type(torch.int64)]
    gradients = torch.autograd.grad(outputs=loss, inputs=X,
                              grad_outputs=torch.ones(loss.size()).cuda(),
                              create_graph=True, retain_graph=False, only_inputs=True)[0]

    prediction = output.data.max(1)[1]
    accuracy = ( float( prediction.eq(Y.data).sum() ) /float(10.0))*100.0
    print(i,accuracy,-loss)

    X = X - lr*gradients.data - weight_decay*X.data*torch.abs(X.data)
    X[X>1.0] = 1.0
    X[X<-1.0] = -1.0

## save images
samples = X.data.cpu().numpy()
samples += 1.0
samples /= 2.0
samples = samples.transpose(0,2,3,1)

fig = plot(samples)
plt.savefig('visualization/max_class_with_generator.png', bbox_inches='tight')
plt.close(fig)