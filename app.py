from glob import glob
import pandas as pd
import os.path
from os import path

import h5py
import matplotlib.pyplot as plt
import os.path
from os import path
import time
import concurrent.futures

t1 = time.perf_counter()

myfilename = []
folders = glob('records/*')


myexceldatadata = pd.read_excel('myecg.xlsx')
def generatefolder():

  for i in range(len(myexceldatadata['ECG_ID'])):

    mypath = 'myfolder/'

    
    mypath = mypath+str(myexceldatadata['mylabel'][i])

    if path.exists(mypath) == False:
      os.mkdir(mypath)

generatefolder()


def generatefilename():
  for f in folders:
    
    myfilename.append(f.split("records")[1][1:-3])
  


generatefilename()


myexceldict = {}
def generateexelldata():
  for i in range(len(myexceldatadata['ECG_ID'])):
    myexceldict[myexceldatadata['ECG_ID'][i]] = myexceldatadata['mylabel'][i]


generateexelldata()



list1 = []



def myscript():
  for key,value in myexceldict.items():
    if key in myfilename:
      if key not in list1:
        list1.append(key)
        imagepath = 'myfolder/'+value+'/'+key+'.png'
        
        return imagepath


figsize=(150, 12)
color="black"
def convertimage(arr1,arr2,arr3):

  for i in range(3):

    if i == 0:
      
      plt.figure(figsize=figsize)
      plt.plot(arr1,color=color)
      plt.axis('off')
      plt.savefig('image1',bbox_inches='tight', pad_inches=0)
      plt.close()
    if i == 1:
      
      plt.figure(figsize=(figsize))
      plt.plot(arr2,color=color)
      plt.axis('off')
      plt.savefig('image2',bbox_inches='tight', pad_inches=0)
      plt.close()
    if i == 2:
      
      plt.figure(figsize=(figsize))
      plt.plot(arr3,color=color)
      plt.axis('off')
      plt.savefig('image3',bbox_inches='tight', pad_inches=0)
      plt.close()
    combineimage()
  
import PIL
from PIL import Image
def combineimage():
   
    try:
      list_im = ['image1.png', 'image2.png', 'image3.png']
      imgs = [ Image.open(i) for i in list_im ]
      min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
      imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
      imgs_comb = Image.fromarray( imgs_comb)
      mypath = myscript()
      print("mypath--------------",mypath)
      imgs_comb.save(mypath)

    except:
      None

import numpy as np
def func(name):
    filename = name
    filename = filename
    print("records/"+filename)
    
    arr1 = []
    arr2 = []
    arr3 = []

    with h5py.File("records/"+filename, 'r') as f:
      signal = f['ecg'][()]

      arr1 = np.concatenate((signal[0], signal[3],signal[6],signal[9]))
      arr2 = np.concatenate((signal[1], signal[4],signal[7],signal[10]))
      arr3 = np.concatenate((signal[2], signal[5],signal[8],signal[11]))

    convertimage(arr1,arr2,arr3)
    

    
# for f in folders:
    

#     filesname = [f.split('/')[-1]]
#     filesname = ' '.join(filesname)
#     func(filesname)



with concurrent.futures.ThreadPoolExecutor() as executor:
    for f in folders:
        filesname = [f.split('/')[-1]]
        filesname = ' '.join(filesname)
        executor.submit(func, filesname)
    

t2 = time.perf_counter()




print(f'Finished in {t2-t1} seconds')