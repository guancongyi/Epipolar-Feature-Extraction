import cv2
import numpy as np


class EpipolarMatching:
    def __init__(self, img1, img2):
        self.im1 = cv2.imread(img1)
        self.im2 = cv2.imread(img2)
        self.pts1 = []
        self.des1 = []
        self.pts2 = []
        self.des2 = []

    def drawPts(self):
        img1 = self.im1
        img2 = self.im2
        pts1 = self.pts1[:30]
        pts2 = self.pts2[:30]
        for marker in self.pts1:
            img1 = cv2.drawMarker(img1, tuple(int(i) for i in marker.pt), color=(0, 255, 0), markerSize=100,
                                  thickness=10)

        for marker in self.pts2:
            img2 = cv2.drawMarker(img2, tuple(int(i) for i in marker.pt), color=(0, 255, 0), markerSize=100,
                                  thickness=10)

        img1 = cv2.resize(img1,(1400,1300),interpolation=cv2.INTER_CUBIC)
        img2 = cv2.resize(img2,(1400,1300),interpolation=cv2.INTER_CUBIC)
        cv2.imshow('1', img1)
        cv2.imshow('2', img2)
        cv2.waitKey(0)

    def extract(self):
        # Initiate FAST detector
        orb1 = cv2.ORB_create()
        orb2 = cv2.ORB_create()
        pts1 = orb1.detect(self.im1, None)
        pts2 = orb2.detect(self.im2, None)
        self.pts1, self.des1 = orb1.compute(self.im1, pts1)
        self.pts2, self.des2 = orb2.compute(self.im2, pts2)
        #self.drawPts()


    def match(self):

        pass



if __name__ == '__main__':
    im1 = 'result0.jpg'  # 7230*6742
    im2 = 'result3.jpg' # 7222*6738
    m = EpipolarMatching(im1, im2)
    m.extract()


    # cv2.imwrite('match.jpg', img3)




