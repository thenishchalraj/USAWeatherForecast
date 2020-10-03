import sys, random
import numpy as nump
import math
import pandas as pd
import urllib.request
import requests
import shutil
import os

from PIL import Image

#GRayscale values as ASCII
grayscale_1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

class ConvertImages():
    
    def __init__(self, soupRef):
        main_arr = []
        baseDir = 'images/'
        if os.path.exists(baseDir):
            shutil.rmtree(baseDir)
        os.mkdir(baseDir)
        
        imgs = soupRef.find_all("li", class_='forecast-tombstone')
        img_arr = []
        for image in imgs:
            img_tag = image.findChildren("img")
            img_arr.append(("https://forecast.weather.gov/"+img_tag[0]["src"], img_tag[0]["alt"]))
        for i in range(0, len(img_arr)):
            self.downloadImg(img_arr[i])
        f = open('output.txt', 'a')
        imgList = os.listdir("./images")
        for i in imgList:
            aimg = self.convertImageToAscii("./images/"+i, 86, 0.43, True)
            for row in aimg:
                f.write(row + '\n')
            f.write('\n\n')
        f.close()
        shutil.rmtree(baseDir)
            
            
    
    def downloadImg(self, image):
        response = requests.get(image[0], stream = True)
        name = ''.join(e for e in image[1] if e.isalnum())
        file = open("./images/{}.jpg".format(name), 'wb')
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, file)
        del response

    def getAverageL(self, image):  
        im = nump.array(image) 
        w,h = im.shape 
        return nump.average(im.reshape(w*h)) 
        
    def convertImageToAscii(self, fileName, cols, scale, moreLevels): 
        global grayscale_1, grayscale_2 
        
        image = Image.open(fileName).convert('L') 
        
        W, H = image.size[0], image.size[1] 
        w = W/cols         
        h = w/scale 
        rows = int(H/h) 
        
        aimg = [] 

        for j in range(rows): 
            y1 = int(j*h) 
            y2 = int((j+1)*h) 
        
            if j == rows-1: 
                y2 = H 

            aimg.append("") 
        
            for i in range(cols): 
        
                x1 = int(i*w) 
                x2 = int((i+1)*w) 
    
                if i == cols-1: 
                    x2 = W 
    
                img = image.crop((x1, y1, x2, y2)) 
        
                # get average luminance 
                avg = int(self.getAverageL(img)) 
        
                if moreLevels: 
                    gsval = grayscale_1[int((avg*69)/255)] 
                else: 
                    gsval = grayscale_2[int((avg*9)/255)] 
    
                # append ascii char to string 
                aimg[j] += gsval 
            
        # return txt image 
        return aimg

