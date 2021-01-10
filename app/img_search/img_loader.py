import os
from collections import defaultdict

import time
import numpy as np
from progressbar import *
import pymysql
import torch
import torchvision.transforms as transforms
from torchvision.datasets.folder import default_loader
from urllib import request

from config import *


class DataLoader:
    def __init__(self, model_name):
        self._load_model(model_name)

    def load(self, db_config, table):
        self._connect_mysql(db_config, table)
        self._img_integration()
        # print(self.img_dict)
        self._extract_img_features()

    def _connect_mysql(self, config, table):
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT `id`, `image_url` FROM {}".format(table))
        self.img = cursor.fetchall()
        conn.commit()

    def _img_integration(self):
        self.img_dict = defaultdict()
        self.id_num = 0
        for item in self.img:
            if item[1]:
                self.id_num += 1
                self.img_dict[item[0]] = item[1]

    def _load_model(self, model_name):
        os.environ['CUDA_VISIBLE_DEVICES'] = '0'
        self.use_gpu = torch.cuda.is_available()
        print('Load model: {}'.format(model_name))
        self.model = torch.hub.load('pytorch/vision', model_name, pretrained=True)
        if self.use_gpu:
            self.model = self.model.cuda()
        normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                         std=[0.229, 0.224, 0.225])
        self.trans = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            normalize,
        ])
        return

    def __get_img_features(self, x):
        x = self.model.conv1(x)
        x = self.model.bn1(x)
        x = self.model.relu(x)
        x = self.model.maxpool(x)
        x = self.model.layer1(x)
        x = self.model.layer2(x)
        x = self.model.layer3(x)
        x = self.model.layer4(x)
        x = self.model.avgpool(x)
        return x

    def _save_img(self, url, jpg_name):
        if not os.path.exists('data/image/'):
            os.mkdir('data/image/')

        proxyHost = "u5795.5.tn.16yun.cn"
        proxyPort = "6441"
        proxyUser = "16VZCZVF"
        proxyPass = "944085"

        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }

        proxy_handler = request.ProxyHandler({
            "http": proxyMeta,
            "https": proxyMeta,
        })        

        opener = request.build_opener(proxy_handler)
        request.install_opener(opener)
        try:
            response = request.urlopen(url)
            time.sleep(0.2)
            name = os.path.join('data/image/', jpg_name)
            with open(name+'.jpg', 'wb') as f:
                f.write(response.read())
        except:
            print(url)
            return

    def _extract_img_features(self):
        print("Extracting img features...")
        if not os.path.exists('np/'):
            os.mkdir('np/')
        widgets = ['Progress: ', Percentage(), ' ', Bar('#'), ' ', Timer(), ' ', ETA()]
        pbar = ProgressBar(widgets=widgets, maxval=10*self.id_num).start()
        img_list = []
        pb_now = 0
        for key, value in self.img_dict.items():
            pb_now += 1
            item_id, img_set = key, eval(value)
            for index, img in enumerate(img_set):
                if not os.path.exists('np/'+str(item_id)+'_{}.npy'.format(index)):
                    self._save_img(img, str(item_id)+'_{}'.format(index))
                    path = os.path.join('data/image/', str(item_id)+'_{}.jpg'.format(index))
                    try:
                        image = default_loader(path)
                        input_image = self.trans(image)
                        if self.use_gpu:
                            input_image = input_image.cuda()
                        input_image = torch.unsqueeze(input_image, 0)
                        image_feature = self.__get_img_features(input_image)
                        image_feature = image_feature.cpu().detach().numpy()
                        img_list.append((image_feature, item_id))
                        np.save(os.path.join('np/', str(item_id)+'_{}.npy'.format(index)), image_feature)
                    except:
                        continue
            pbar.update(10 * pb_now + 1)
        pbar.finish()
    
    def extract_single_img_embed(self, imgpath):
        if 'http' in imgpath:
            self._save_img(imgpath, imgpath.replace('/'))
            path = os.path.join('data/image/', imgpath.replace('/')+'.jpg')
        else:
            path = imgpath
        image = default_loader(path)
        input_image = self.trans(image)
        if self.use_gpu:
            input_image = input_image.cuda()
        input_image = torch.unsqueeze(input_image, 0)
        image_feature = self.__get_img_features(input_image)
        image_feature = image_feature.cpu().detach().numpy()
        return image_feature



if __name__ == "__main__":
    data = DataLoader(MODEL_NAME)
    data.load(db_config, TABLE_NAME)
