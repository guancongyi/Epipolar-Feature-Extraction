from match import Match
import cv2
import numpy as np

'''
# feature extract and match
path1 = 'test/im1.jpg'
path2 = 'test/im2.jpg'
m = Match(path1, path2)
kpts1, kpts2 = m.extract()
'''
path1 = 'test/A_01774_23284.jpg'
path2 = 'test/E_01777_25477.jpg'

# cam A:
fx1 = 50 # mm
fy1 = 50
cx1 = -0.046989
cy1 = -0.148033



cam1 = np.array([[fx1,0,cx1],
                 [0,fy1,cy1],
                 [0,0,0]])
# cam E
fx2 = 40 # mm
fy2 = 40
cx2 = -0.07302
cy2 = -0.009029

cam1 = np.array([[fx2,0,cx2],
                 [0,fy2,cy2],
                 [0,0,0]])

# outputs
P1 = np.zeros((3,4))
P2 = np.zeros((3,4))

# cv2.stereoRectify()









