import matplotlib.pyplot
import numpy as np
from PIL import Image
import pytesseract
import cv2
from scipy.ndimage import gaussian_filter1d
from skimage.transform import downscale_local_mean
from pyzbar.pyzbar import decode

extrema=[]
downscaled=None

#initialize pytesseract
pytesseract.pytesseract.tesseract_cmd=r'pytesseract filepath'

#shift the image left right up and down and then only mark vaulues different from the original true. Then, add all the edges together into a big picture
def shift(a, u, d):
    e = np.empty_like(a)
    if u==0:
        #horizantol shift
        if d >= 0:
            #right shift
            e[:,:d] = 0
            e[:,d:] = a[:,:-d]
        else:
            #left shift
            e[:,d:] = 0
            e[:,:d] = a[:,-d:]
    if u==1:
        #vertical shift
        if d >= 0:
            #down shift
            e[:d,:] = 0
            e[d:,:] = a[:-d,:]
        else:
            #up shift
            e[d:,:] = 0
            e[:d,:] = a[-d:,:]
    return e

def coordinate_recurs(coords):
    global extrema, downscaled
    #y,x
    #set the starting value and prime the neighbor_values array with a 1 value. Create the neighbors array for later referencing, add x to temp and tested, and state that the last successful value was x
    x=[coords[0][0],coords[1][0]]
    neighbor_values=[1]
    temp=[x]
    tested=[x]
    last_successful=[x]
    
    #while there are still edges detected, which means the edge isn't done being traced
    while 1 in neighbor_values:
        neighbors=[]
        for x in last_successful:
            #create neighbors list...
            neighbors=neighbors+[[x[0]-1,x[1]],[x[0],x[1]-1],[x[0],x[1]+1],[x[0]+1,x[1]]]
        #...but only with untested values within the bounds of the image
        neighbors=[neighbors[x] for x in range(len(neighbors)) if neighbors[x] not in tested and downscaled.shape[0]>=neighbors[x][0]>=0 and downscaled.shape[1]>=neighbors[x][1]>=0 and neighbors[x] not in neighbors[:x]]
        #get the values in edges of all the neighbors, add the detected edges to temp, add all values to tested, and set last successful as the detected edges just from this round
        try:
            neighbor_values=[downscaled[x[0],x[1]] for x in neighbors]
        except:
            neighbor_values=[0]
            continue
        temp=temp+[neighbors[x] for x in range(len(neighbors)) if neighbor_values[x]!=0]
        tested=tested+neighbors
        last_successful=[neighbors[x] for x in range(len(neighbors)) if neighbor_values[x]!=0]

    #add the max and min y and x as a list to the extrema list
    arr=np.array(temp).T
    extrema.append([arr[0].max()*5,arr[0].min()*5,arr[1].max()*5,arr[1].min()*5])

    #make the outline all zeros in the edges matrix
    for x in temp:
        downscaled[x[0],x[1]]=0

    coords=np.where(downscaled==1)

    #recursion
    if len(coords[0])>0:
        coordinate_recurs(coords)

def ocr_preprocess(filepath):
    image = cv2.imread(filepath)
    gray= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.threshold(blur, 0, 255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening
    return invert

def process_image(filepath):
    global extrema, downscaled
    #load image into array
    #get input from external source
    img=matplotlib.pyplot.imread(filepath)
    
    #rgb to greyscale (brightness)
    gray = np.dot(img, [0.2989, 0.5870, 0.1140])
    
    #if a value is sufficiently white it is true and otherwise is false
    gray=gray>165
    
    #sum up the rows and columns and divide them by the row and column length respectively to get the percentage of the row or column that is white
    row_sums=gray.sum(axis=1)/gray.shape[1]
    column_sums=gray.sum(axis=0)/gray.shape[0]
    
    #get the borders of the label from the row and column sums with the demarcation line being 99% whiteness
    top_border=np.argmax(row_sums>0.99)
    bottom_border=gray.shape[0]-np.argmax(np.flip(row_sums)>0.99)
    left_border=np.argmax(column_sums>0.99)
    right_border=gray.shape[1]-np.argmax(np.flip(column_sums)>0.99)
    
    #crop the image to the borders
    gray=gray[top_border:bottom_border,left_border:right_border]
    
    #blur and resharpen image
    gray_blurred=gaussian_filter1d(gray,sigma=10,axis=1)==1

    edge_field=np.pad(gray_blurred, 2)
    
    gray_left=shift(edge_field,0,-1)
    gray_right=shift(edge_field,0,1)
    gray_up=shift(edge_field,1,-1)
    gray_down=shift(edge_field,1,1)
    
    left_edges=edge_field!=gray_left
    right_edges=edge_field!=gray_right
    top_edges=edge_field!=gray_up
    bottom_edges=edge_field!=gray_down
    
    edges=left_edges+right_edges+top_edges+bottom_edges
        
    #crops the whitespace off, plus 1 because the edge lines spill over
    edges=edges[3:-3,3:-3]

    Image.fromarray(edges).save('test.png')
    
    #edges detected, now time to find the objects
    #ymax, ymin, xmax, xmin
    downscaled=downscale_local_mean(edges, (5,5))!=0
    coords=np.where(downscaled==1)

    coordinate_recurs(coords)
    
    #output text and location
    outputs=[]

    #preprocess original image into a form more easily readable by the computer
    text_image=ocr_preprocess(filepath)
    
    for x in extrema:
        
        if x[0]>gray.shape[0]: x[0]=gray.shape[0]
        if x[2]>gray.shape[1]: x[2]=gray.shape[1]
        if (x[0]-x[1])*(x[2]-x[3]) < 5000 or (x[0]-x[1])*(x[2]-x[3]) > 1500000 or (x[2]-x[3])<450: continue
        try:
            code=decode(img[x[1]:x[0],x[3]:x[2]])
            if code!=[]:
                outputs.append({
                    'typ':'barcode',
                    'outp':str(code[0].data).split('\'')[1],
                    'ymax':str(x[0]/gray.shape[0]),
                    'ymin':str(x[1]/gray.shape[0]),
                    'xmax':str(x[2]/gray.shape[1]),
                    'xmin':str(x[3]/gray.shape[1])
                })
                continue
            text=pytesseract.image_to_string(text_image[x[1]:x[0],x[3]:x[2]], lang='eng', config='--psm 6')
            if text!=' \n' and text!='':
                outputs.append({
                    'typ':'text',
                    'outp':text.replace('\n','').replace('\x0c',''),
                    'ymax':str(x[0]/gray.shape[0]),
                    'ymin':str(x[1]/gray.shape[0]),
                    'xmax':str(x[2]/gray.shape[1]),
                    'xmin':str(x[3]/gray.shape[1])
                })
        except:
            pass

    extrema=[]
    downscaled=None
    return outputs
