import cv2
import numpy as np
import argparse
import sys
import subprocess

blobsize  = 45
threshold = 165


def removeBlob(img):

    #find all your connected components (white blobs in your image)
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(img, connectivity=8)

    #the following part is just taking out the background which is also considered a component, but most of the time we don't want that.
    sizes = stats[1:, -1]; nb_components = nb_components - 1

    # minimum size of particles we want to keep (number of pixels)
    #here, it's a fixed value, but you can set it as you want, eg the mean of the sizes or whatever
    min_size = blobsize

    #your answer image
    img = np.zeros((output.shape))
    
    #for every component in the image, you keep it only if it's above min_size
    for i in range(0, nb_components):
      if sizes[i] >= min_size:
        img[output == i + 1] = 255

    return [255]-img


def resolve(path):

    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    retval, img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((3,3), np.uint8)
    img = np.uint8([255])-img
    img = cv2.dilate(img, kernel, iterations = 1)

    img = np.uint8([255])-img
    img = removeBlob(img)

    #img = removeBlob([255]-img)
    return img;


def solve(path):
    img = resolve(path)
    cv2.imwrite('tmp.jpe', img)
    result = subprocess.Popen("tesseract tmp.jpe stdout -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789 -psm 8 2> /dev/null", shell=True, stdout=subprocess.PIPE).stdout.readlines()[0].decode("utf-8") 
    return result;


def main(args):
    parser = argparse.ArgumentParser(description="solve telerik captcha")
    parser.add_argument("path", metavar="path",  help="path of image")
    args = parser.parse_args()
    return solve(args.path)

if __name__ == "__main__":
  result =  main(sys.argv)
  print(result)


