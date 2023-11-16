import cv2
import numpy as np
import argparse
from Compress420 import Compress420

# Image path
parser = argparse.ArgumentParser()
parser.add_argument('--input_img', default = './ntust_cat.jpg', type = str)
args = parser.parse_args()

# Load the image
img0 = cv2.imread(args.input_img)
# Resize the image
img0 = cv2.resize(img0,(640,640))

# Initialize the compress object
compress420 = Compress420(img0)
# Convert image from bgr to ycrcb444
img0_444 = compress420.bgr_to_ycrcb444()
# Compress image from ycrcb444 to ycrcb420
img0_420 = compress420.ycrcb444_to_420()
# Restore image from ycrcb420 to ycrcb444
img_restore = compress420.ycrcb420_to_444()
# Convert image from ycrcb444 to bgr
img_result = compress420.ycrcb_to_bgr()

# Print Compress Rate
print(f'org_size: {np.size(img0)}')
print(f'compress_size: {np.size(img0_420)}')

# Show result
cv2.imshow('org',img0)
cv2.imshow('Result',img_result)
# Store result
cv2.imwrite('result.jpg',img_result)

cv2.waitKey()

cv2.destroyAllWindows()
    
