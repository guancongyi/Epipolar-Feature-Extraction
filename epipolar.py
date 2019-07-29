import cv2
import numpy as np
import time
import database
import os


class EpipolarMatching:
    def __init__(self, img1, img2):
        self.im1 = cv2.imread(img1)
        self.im2 = cv2.imread(img2)
        self.pts1 = []
        self.des1 = []
        self.pts2 = []
        self.des2 = []
        self.matches = []
        self.goodMatches = []
        self.error = 100


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

    def drawMatches(self, matches):
        # matches = sorted(self.matches, key=lambda x: x.distance)
        draw_params = dict(matchColor=(0, 255, 0),singlePointColor = (255, 0, 0),flags=0)
        img3 = cv2.drawMatches(self.im1, self.pts1, self.im2, self.pts2, matches, None, flags=0)
        # img3 = cv2.resize(img3, (1400, 1300), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite('3.jpg', img3)



    def extract(self):
        # Initiate FAST detector
        orb1 = cv2.ORB_create()
        orb2 = cv2.ORB_create()
        pts1 = orb1.detect(self.im1, None)
        pts2 = orb2.detect(self.im2, None)
        self.pts1, self.des1 = orb1.compute(self.im1, pts1)
        self.pts2, self.des2 = orb2.compute(self.im2, pts2)

    def BFmatch(self):
        # FLANN_INDEX_KDTREE = 0
        # index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        # search_params = dict(checks=50)  # or pass empty dictionary
        # flann = cv2.FlannBasedMatcher(index_params, search_params)
        # matches = flann.knnMatch(self.des1, self.des2, k=2)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        self.matches = bf.match(self.des1, self.des2)
        self.drawMatches(self.matches)

    def EpipolarMatch(self):
        # Every keypoint in image 1,its correspondent in image 2
        # should be on the same line as the one in image 1.
        count = 0
        sum = 0
        for match in self.matches:
            x1, y1 = self.pts1[match.queryIdx].pt
            x2, y2 = self.pts2[match.trainIdx].pt
            error = abs(y2 - y1)
            if error <= self.error:
                count += 1
                sum += error
                self.goodMatches.append(match)

        # self.printMatches(self.goodMatches,self.pts1,self.pts2)
        # self.drawMatches(self.goodMatches)
        print("error " , sum/count)

    def printMatches(self, matches, pts1, pts2):
        for match in matches:
            print(pts1[match.queryIdx].pt, pts2[match.trainIdx].pt)

    def getInfo(self):
        return self.goodMatches, self.pts1, self.pts2

def getGeoLocation(im, matches, pts1, pts2):
    cx, cy, f, R, XYZs, _, miu = db.getInfo(im)
    for match in matches:
        pass


if __name__ == '__main__':
    db = database.DB('extrinsic.db')

    imgList = os.listdir("./out")
    i = 0
    while i < len(imgList)-1:
        im1 = 'out/'+imgList[i]
        im2 = 'out/'+imgList[i+1]
        i += 2

        print("Start extracting and matching...")
        m = EpipolarMatching(im1, im2)
        m.extract()
        m.BFmatch()

        s = time.time()
        m.EpipolarMatch()
        matches, pts1, pts2 = m.getInfo()
        e = time.time()
        print(e - s)
        print("Finish matching")

        print("Calculate matches...")
        #getGeoLocation(im1, matches, pts1, pts2)

    print("done")




