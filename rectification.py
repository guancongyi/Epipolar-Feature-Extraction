import numpy as np
import database
import cv2

class rectification():
    def __init__(self, cx, cy, f, R, miu):
        self.f = f
        self.cx = cx
        self.cy = cy
        self.miu = miu
        self.a1, self.a2, self.a3 = R[0, 0], R[0, 1], R[0, 2]
        self.b1, self.b2, self.b3 = R[1, 0], R[1, 1], R[1, 2]
        self.c1, self.c2, self.c3 = R[2, 0], R[2, 1], R[2, 2]

    def getEpipolarImage(self, src):
        r, c = dst.shape[:2]
        cr, cc = r / 2, c / 2
        for i in range(0, r):
            for j in range(0, c):
                u, v = pixToDist((cr, cc), (i, j), (self.cx, self.cy), self.miu)

    def getResultImgSize(self, size):
        r, c = size
        c1x, c1y = pixToDist((r / 2, c / 2), (0, 0), (self.cx, self.cy), self.miu)
        c2x, c2y = pixToDist((r / 2, c / 2), (r, c), (self.cx, self.cy), self.miu)
        # top left
        return (r, c)

    def slantToParallel(self, x, y, u, v):
        x = int((-self.f * (self.a1 * u + self.b1 * v - self.c1 * self.f)) / (self.a3 * u + self.b3 * v + self.c3 * self.f))
        y = int((-self.f * (self.a2 * u + self.b2 * v - self.c2 * self.f)) / (self.a3 * u + self.b3 * v + self.c3 * self.f))

    def pixToDist(self, center, xy):
        mx, my = center
        x, y = xy
        return ((mx - x) * self.miu + self.cx, (my - y) * self.miu + self.cy)










if __name__ == '__main__':
    # get extrinsic from database
    im1 = 'E_00025_23725.jpg'
    im2 = 'E_00026_23726.jpg'

    db = database.DB('extrinsic.db')
    (R1, T1, XYZ1) = db.get_RT(im1)
    (R2, T2, XYZ2) = db.get_RT(im2)
    cx1 = -0.07302
    cy1 = -0.009029
    miu1 = 0.0046
    f1 = 41.9401

    # find epipolar image by using epipolar rectification
    path1 = 'test/' + im1
    # path2 = 'test/' + im2
    img1 = cv2.imread(path1)
    # img2 = cv2.imread(path2)

    # estimate the result image size by
    # estimating the original image's
    # left up corner and bottom right corner.
    (r,c) = getResultImgSize(img1,cx1,cy1,miu1)
    dst = np.zeros((r,c,3), np.uint8)
    getEpipolarImage(img1,dst,R1,f1,cx1,cy1,miu1)



'''
# using opencv to do recitification
# by giving camera's intrinsic parameter,
# extrinsic parameters, and so on.
path1 = 'test/' + im1
path2 = 'test/' + im2

# cam E1:
fx2 = 41.94 # mm
fy2 = 41.94
cx2 = -0.07302
cy2 = -0.009029

cam1 = np.array([[fx2,0,cx2],
                 [0,fy2,cy2],
                 [0,0,0]])

# cam E2
cam2 = cam1

img1 = cv2.imread(path1)
img2 = cv2.imread(path2)


# outputs
OP1 = np.zeros((3,4))
OP2 = np.zeros((3,4))
OR1 = np.zeros((3,3))
OR2 = np.zeros((3,3))
Q = np.zeros((4,4))

cv2.stereoRectify(cam1,None,cam2,None,img1.shape,)
'''








