import numpy as np
import cv2

class spaceIntersect():
    def __init__(self, db, im1, im2):
        self.im1 = cv2.imread(im1)
        self.im2 = cv2.imread(im2)
        self.name1 = im1.split('/')[1]
        self.name2 = im2.split('/')[1]
        self.db = db


    def getGeoLocation(self, matches, pts1, pts2, dess1, dess2):
        cx1, cy1, f1, R1, XYZ1s, _, miu1 = self.db.getInfo(self.name1)
        Xs1, Ys1, Zs1 = XYZ1s
        cx2, cy2, f2, R2, XYZ2s, _, miu2 = self.db.getInfo(self.name2)
        Xs2, Ys2, Zs2 = XYZ2s
        R2 = np.zeros((3,3))
        R1 = R2

        for match in matches:
            pt1 = pts1[match.queryIdx].pt
            pt2 = pts2[match.trainIdx].pt
            des1 = dess1[match.queryIdx]
            des2 = dess2[match.trainIdx]
            x1, y1 = self.pix2Dist(miu1, self.im1.shape[1] / 2, self.im1.shape[0] / 2, pt1[1], pt1[0])
            x2, y2 = self.pix2Dist(miu2, self.im2.shape[1] / 2, self.im2.shape[0] / 2, pt2[1], pt2[0])
            temp = np.dot(R1,np.array([[x1],[y1],[-f1]]))
            temp += np.array([[Xs1],[Ys1],[Zs1]])
            l11 = f1 * R1[0][0] + (x1-cx1) * R1[0][2] # l1
            l12 = f2 * R2[0][0] + (x2-cx2) * R2[0][2] # l1 for right image
            l21 = f1 * R1[1][0] + (x1-cx1) * R1[1][2] # l2
            l22 = f2 * R2[1][0] + (x2-cx2) * R2[1][2] # l2 for right image
            l31 = f1 * R1[2][0] + (x1-cx1) * R1[2][2] # l3
            l32 = f2 * R2[2][0] + (x2-cx2) * R2[2][2] # l3 for right image
            l41 = f1 * R1[0][1] + (y1-cy1) * R1[0][2] # l4
            l42 = f2 * R2[0][1] + (y2-cy2) * R2[0][2] # l4 for right image
            l51 = f1 * R1[1][1] + (y1-cy1) * R1[1][2] # l5
            l52 = f2 * R2[1][1] + (y2-cy2) * R2[1][2] # l5 for right image
            l61 = f1 * R1[2][1] + (y1-cy1) * R1[2][2] # l6
            l62 = f2 * R2[2][1] + (y2-cy2) * R2[2][2] # l6 for right image
            lx1 = f1 * R1[0][0] * Xs1 + f1 * R1[1][0] * Ys1 + f1 * R1[2][0] * Zs1 + (x1-cx1) * R1[0][2] * Xs1 + (x1-cx1) * R1[1][2] * Ys1 + (x1-cx1) * R1[2][2] * Zs1
            lx2 = f2 * R2[0][0] * Xs2 + f2 * R2[1][0] * Ys2 + f2 * R2[2][0] * Zs2 + (x2-cx2) * R2[0][2] * Xs2 + (x2-cx2) * R2[1][2] * Ys2 + (x2-cx2) * R2[2][2] * Zs2
            ly1 = f1 * R1[0][1] * Xs1 + f1 * R1[1][1] * Ys1 + f1 * R1[2][1] * Zs1 + (y1-cy1) * R1[0][2] * Xs1 + (y1-cy1) * R1[1][2] * Ys1 + (y1-cy1) * R1[2][2] * Zs1
            ly2 = f2 * R2[0][1] * Xs2 + f2 * R2[1][1] * Ys2 + f2 * R2[2][1] * Zs2 + (y2-cy2) * R2[0][2] * Xs2 + (y2-cy2) * R2[1][2] * Ys2 + (y2-cy2) * R2[2][2] * Zs2

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
            ATAinv = np.linalg.inv(np.dot(A.T, A))
            XYZ = np.dot(np.dot(ATAinv, A.T),b)
            XYZ = (XYZ[0,0],XYZ[1,0],XYZ[2,0])
            # print('Store result', pt1, pt2, ' in database...')
            self.db.add_matches(self.name1, self.name2, pt1, pt2, des1, des2, XYZ)



    def pix2Dist(self, miu, mx, my, pix_x, pix_y):
        return (pix_x-mx)*miu, (pix_y-my)*miu
