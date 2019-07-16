import numpy as np
import database
import cv2



# get extrinsic form database
im1 = 'E_00025_23725.jpg'
im2 = 'E_00026_23726.jpg'

db = database.DB('extrinsic.db')
(R1,T1,XYZ1) = db.get_RT(im1)
(R2,T2,XYZ2) = db.get_RT(im2)


# using opencv to do recitification
# by giving camera's intrinsic parameter,
# extrinsic parameters, and so on.
path1 = 'test/' + im1
path2 = 'test/' + im2

# cam E1:
fx2 = 40 # mm
fy2 = 40
cx2 = -0.07302
cy2 = -0.009029

cam1 = np.array([[fx2,0,cx2],
                 [0,fy2,cy2],
                 [0,0,0]])
# cam E2
cam2 = cam1

# outputs
P1 = np.zeros((3,4))
P2 = np.zeros((3,4))

# cv2.stereoRectify()









