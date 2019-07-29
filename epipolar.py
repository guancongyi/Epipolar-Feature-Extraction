import cv2
import numpy as np
import time
import database
import os
import spaceIntersection
import statistics


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
        self.th = 30


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

    def drawMatches(self, path, path_good):
        # matches = sorted(self.matches, key=lambda x: x.distance)
        draw_params = dict(matchColor=(0, 255, 0),singlePointColor = (255, 0, 0),flags=0)
        img3 = cv2.drawMatches(self.im1, self.pts1, self.im2, self.pts2, self.matches, None, flags=0)
        img4 = cv2.drawMatches(self.im1, self.pts1, self.im2, self.pts2, self.goodMatches, None, flags=0)
        # img3 = cv2.resize(img3, (1400, 1300), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(path, img3)
        cv2.imwrite(path_good, img4)

    def extract(self):
        # Initiate FAST detector
        # surf1 = cv2.xfeatures2d.SURF_create()
        # self.pts1, self.des1 = surf1.detectAndCompute(self.im1,None)
        # surf2 = cv2.xfeatures2d.SURF_create()
        # self.pts2, self.des2 = surf2.detectAndCompute(self.im2,None)
        orb1 = cv2.ORB_create(3000)
        orb2 = cv2.ORB_create(3000)
        pts1 = orb1.detect(self.im1, None)
        pts2 = orb2.detect(self.im2, None)
        self.pts1, self.des1 = orb1.compute(cv2.cvtColor(self.im1,cv2.COLOR_BGR2GRAY), pts1)
        self.pts2, self.des2 = orb2.compute(cv2.cvtColor(self.im2,cv2.COLOR_BGR2GRAY), pts2)

    def BFmatch(self):
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        temp = bf.match(self.des1, self.des2)
        for match in temp:
            # if match.distance < 64:
            self.matches.append(match)

    def EpipolarMatch(self):
        # Every keypoint in image 1,its correspondent in image 2
        # should be on the same line as the one in image 1.
        error = []

        for match in self.matches:
            x1, y1 = self.pts1[match.queryIdx].pt
            x2, y2 = self.pts2[match.trainIdx].pt
            error.append(y2 - y1)


        med = statistics.median(error)

        sum = 0
        count = 0
        for match in self.matches:
            x1, y1 = self.pts1[match.queryIdx].pt
            x2, y2 = self.pts2[match.trainIdx].pt
            if abs(y2-y1-med) < self.th:
                sum += abs(y2-y1)
                self.goodMatches.append(match)
                count += 1

        print(sum/count)
        # self.printMatches(self.matches,self.pts1,self.pts2)


    def printMatches(self, matches, pts1, pts2):
        for match in matches:
            print(pts1[match.queryIdx].pt, pts2[match.trainIdx].pt, pts2[match.trainIdx].pt[1]-pts1[match.queryIdx].pt[1] )

    def getInfo(self):
        return self.goodMatches, self.pts1, self.pts2



if __name__ == '__main__':
    db = database.DB('extrinsic.db')

    imgList = os.listdir("./out")
    i = 0
    while i < len(imgList)-1:
        im1 = 'out/'+imgList[i]
        im2 = 'out/'+imgList[i+1]
        out = './matches/' + str(i) + '.jpg'
        out_good = './good_matches/' + str(i) + '.jpg'
        i += 2

        print("Start extracting and matching...")
        m = EpipolarMatching(im1, im2)
        m.extract()
        m.BFmatch()

        s = time.time()
        m.EpipolarMatch()
        matches, pts1, pts2 = m.getInfo()
        e = time.time()
        print('time elapased: ', e - s)
        print("Finish matching")
        m.drawMatches(out, out_good)


        print("Calculate matches...")

        space = spaceIntersection.spaceIntersect(db,im1,im2)
        space.getGeoLocation(matches, pts1, pts2)

    print("done")




