import os
import time
import csv
import numpy as np
import cv2

import torch
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim
cudnn.benchmark = True

from torchvision import datasets, transforms
import torchvision

import models
from metrics import AverageMeter, Result
import utils
from PIL import Image

import sys
sys.path.insert(0, os.path.abspath(os.path.dirname('dataloaders/')))
from transforms import ToTensor

args = utils.parse_command()
print(args)
os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu # Set the GPU.

fieldnames = ['rmse', 'mae', 'delta1', 'absrel',
            'lg10', 'mse', 'delta2', 'delta3', 'data_time', 'gpu_time']
best_fieldnames = ['best_epoch'] + fieldnames
best_result = Result()
best_result.set_to_worst()

def main():
    global args, best_result, output_directory, train_csv, test_csv

    checkpoint = torch.load('./results/mobilenet-nnconv5dw-skipadd-pruned.pth.tar', map_location='cpu')
    if type(checkpoint) is dict:
        model = checkpoint['model']
    else:
        model = checkpoint
    model.eval()



    #data_path = '/home/yarl/Desktop/Github/AutonomousDrone/Output'
    #t = transforms.Compose([transforms.Resize(255), transforms.CenterCrop(224), transforms.ToTensor()])
    #dataset = torchvision.datasets.ImageFolder(root=data_path, transform=t)
    #loader = torch.utils.data.DataLoader(dataset, batch_size=1, num_workers=0, shuffle=False)
    #for batch_idx, (data, target) in enumerate(loader):

    folder = '/home/yarl/Desktop/Github/AutonomousDrone/Output/ipadVideo'
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))

        #img = cv2.resize(img, (640, 480))
        img = cv2.resize(img, (224, 224))

        #x = np.zeros([1, 3, 224, 224])
        #x[0, :, :, :] = np.transpose(img, (2,0,1))
        #x = x.astype('float32')
        #tensor = torch.from_numpy(x)
        #pred = model(tensor/255)

        toTensor = ToTensor()
        tensor = toTensor.__call__(img)/255
        pred = model(tensor[None, ...])

        depth_img = np.squeeze(pred.data.cpu().numpy())

        #d_min = np.min(depth_img)
        #d_max = np.max(depth_img)
        d_min = np.min(0)
        d_max = np.max(10)

        output = (depth_img - d_min) / (d_max - d_min)
        cv2.imshow('input', img)
        cv2.imshow('output', output)
        cv2.waitKey(1)
    return


def validate(val_loader, model, epoch, write_to_file=True):
    average_meter = AverageMeter()
    model.eval() # switch to evaluate mode
    end = time.time()
    for i, (input, target) in enumerate(val_loader):
        input, target = input.cuda(), target.cuda()
        # torch.cuda.synchronize()
        data_time = time.time() - end

        # compute output
        end = time.time()
        with torch.no_grad():
            pred = model(input)
        # torch.cuda.synchronize()
        gpu_time = time.time() - end

        # measure accuracy and record loss
        result = Result()
        result.evaluate(pred.data, target.data)
        average_meter.update(result, gpu_time, data_time, input.size(0))
        end = time.time()

        # save 8 images for visualization
        skip = 50

        if args.modality == 'rgb':
            rgb = input

        if i == 0:
            img_merge = utils.merge_into_row(rgb, target, pred)
        elif (i < 8*skip) and (i % skip == 0):
            row = utils.merge_into_row(rgb, target, pred)
            img_merge = utils.add_row(img_merge, row)
        elif i == 8*skip:
            filename = output_directory + '/comparison_' + str(epoch) + '.png'
            utils.save_image(img_merge, filename)

        if (i+1) % args.print_freq == 0:
            print('Test: [{0}/{1}]\t'
                  't_GPU={gpu_time:.3f}({average.gpu_time:.3f})\n\t'
                  'RMSE={result.rmse:.2f}({average.rmse:.2f}) '
                  'MAE={result.mae:.2f}({average.mae:.2f}) '
                  'Delta1={result.delta1:.3f}({average.delta1:.3f}) '
                  'REL={result.absrel:.3f}({average.absrel:.3f}) '
                  'Lg10={result.lg10:.3f}({average.lg10:.3f}) '.format(
                   i+1, len(val_loader), gpu_time=gpu_time, result=result, average=average_meter.average()))

    avg = average_meter.average()

    print('\n*\n'
        'RMSE={average.rmse:.3f}\n'
        'MAE={average.mae:.3f}\n'
        'Delta1={average.delta1:.3f}\n'
        'REL={average.absrel:.3f}\n'
        'Lg10={average.lg10:.3f}\n'
        't_GPU={time:.3f}\n'.format(
        average=avg, time=avg.gpu_time))

    if write_to_file:
        with open(test_csv, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'mse': avg.mse, 'rmse': avg.rmse, 'absrel': avg.absrel, 'lg10': avg.lg10,
                'mae': avg.mae, 'delta1': avg.delta1, 'delta2': avg.delta2, 'delta3': avg.delta3,
                'data_time': avg.data_time, 'gpu_time': avg.gpu_time})
    return avg, img_merge

if __name__ == '__main__':
    main()
