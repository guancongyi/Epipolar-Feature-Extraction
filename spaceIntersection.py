import numpy as np
import cv2

class spaceIntersect():
    def __init__(self, db, im1, im2):
        self.im1 = cv2.imread(im1)
        self.im2 = cv2.imread(im2)
        self.name1 = im1.split('/')[1]
        self.name2 = im2.split('/')[1]
        self.db = db


    def getGeoLocation(self, matches, pts1, pts2):
        cx1, cy1, f1, R1, XYZ1s, _, miu1 = self.db.getInfo(self.name1)
        Xs1, Ys1, Zs1 = XYZ1s
        cx2, cy2, f2, R2, XYZ2s, _, miu2 = self.db.getInfo(self.name2)
        Xs2, Ys2, Zs2 = XYZ2s

        for match in matches:
            pt1 = pts1[match.queryIdx].pt
            pt2 = pts2[match.trainIdx].pt
            x1, y1 = self.pix2Dist(cx1, cy1, miu1, int(self.im1.shape[0] / 2), int(self.im1.shape[1] / 2), pt1[0], pt1[1])
            x2, y2 = self.pix2Dist(cx2, cy2, miu2, int(self.im2.shape[0] / 2), int(self.im2.shape[1] / 2), pt2[0], pt2[1])
            l11 = f1 * R1[0][0] + x1 * R1[0][2] # l1
            l12 = f2 * R2[0][0] + x2 * R2[0][2] # l1 for right image
            l21 = f1 * R1[1][0] + x1 * R1[1][2] # l2
            l22 = f2 * R2[1][0] + x2 * R2[1][2] # l2 for right image
            l31 = f1 * R1[2][0] + x1 * R1[2][2] # l3
            l32 = f2 * R2[2][0] + x2 * R2[2][2] # l3 for right image
            l41 = f1 * R1[0][1] + y1 * R1[0][2] # l4
            l42 = f2 * R2[0][1] + y2 * R2[0][2] # l4 for right image
            l51 = f1 * R1[1][1] + y1 * R1[1][2] # l5
            l52 = f2 * R2[1][1] + y2 * R2[1][2] # l5 for right image
            l61 = f1 * R1[2][1] + y1 * R1[2][2] # l6
            l62 = f2 * R2[2][1] + y2 * R2[2][2] # l6 for right image
            lx1 = f1 * R1[0][0] * Xs1 + f1 * R1[1][0] * Ys1 + f1 * R1[2][0] * Zs1 + x1 * R1[0][2] * Xs1 + x1 * R1[1][2] * Ys1 + x1 * R1[2][2] * Zs1
            lx2 = f2 * R2[0][0] * Xs2 + f2 * R2[1][0] * Ys2 + f2 * R2[2][0] * Zs2 + x2 * R2[0][2] * Xs2 + x2 * R2[1][2] * Ys2 + x2 * R2[2][2] * Zs2
            ly1 = f1 * R1[0][1] * Xs1 + f1 * R1[1][1] * Ys1 + f1 * R1[2][1] * Zs1 + y1 * R1[0][2] * Xs1 + y1 * R1[1][2] * Ys1 + y1 * R1[2][2] * Zs1
            ly2 = f2 * R2[0][1] * Xs2 + f2 * R2[1][1] * Ys2 + f2 * R2[2][1] * Zs2 + y2 * R2[0][2] * Xs2 + y2 * R2[1][2] * Ys2 + y2 * R2[2][2] * Zs2

            A = np.array([  [l11, l21, l31],
                            [l41, l51, l61],
                            [l12, l22, l32],
                            [l42, l52, l62]
                            ])
            b = np.array([  [lx1],
                            [ly1],
                            [lx2],
                            [ly2]
                            ])
            Ainv = np.linalg.inv(np.dot(A.T, A))
            XYZ = np.dot(np.dot(Ainv, A.T),b)



    def pix2Dist(self, cx, cy, miu, mx, my, pix_x, pix_y):
        return abs((mx-pix_x)*miu+cx), abs((my-pix_y)*miu+cy)
