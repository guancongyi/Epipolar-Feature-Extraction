import cv2
import numpy as np


class Match:
    def __init__(self, img1, img2):
        self.im1 = cv2.imread(img1)
        self.im2 = cv2.imread(img2)

    def drawPts(self,pts1,pts2):
        ''' img1 - image on which we draw the epilines for the points in img2
        lines - corresponding epilines '''
        img1 = self.im1
        img2 = self.im2
        for pt1,pt2 in zip(pts1,pts2):
            color = tuple(np.random.randint(0,255,3).tolist())
            img1 = cv2.circle(img1,tuple(pt1),90,color,-1)
            img2 = cv2.circle(img2,tuple(pt2),90,color,-1)


        # img1 = cv2.resize(img1,(600,600),interpolation=cv2.INTER_CUBIC)
        # img2 = cv2.resize(img2,(600,600),interpolation=cv2.INTER_CUBIC)
        # cv2.imshow('1', img1)
        # cv2.imshow('2', img2)
        # cv2.waitKey(0)

    def extract(self):

        sift = cv2.xfeatures2d.SIFT_create()

        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(self.im1,None)
        kp2, des2 = sift.detectAndCompute(self.im2,None)

        # FLANN parameters
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks=50)

        flann = cv2.FlannBasedMatcher(index_params,search_params)
        self.matches = flann.knnMatch(des1,des2,k=2)

        good = []
        pts1 = []
        pts2 = []

        # ratio test as per Lowe's paper
        for i,(m,n) in enumerate(self.matches):
            if m.distance < 0.7*n.distance:
                good.append(m)
                pts2.append(kp2[m.trainIdx].pt)
                pts1.append(kp1[m.queryIdx].pt)

        pts1 = np.int32(pts1)
        pts2 = np.int32(pts2)
        F, mask = cv2.findFundamentalMat(pts1,pts2,cv2.RANSAC,0.5,1)

        # We select only inlier points
        pts1 = pts1[mask.ravel()==1]
        pts2 = pts2[mask.ravel()==1]

        img3 = cv2.drawMatches(self.im1, kp1, self.im2, kp2, good[:10], None, flags=2)
        cv2.imshow('3', img3)
        cv2.waitKey(0)
        return pts1, pts2, img3


if __name__ == '__main__':
    im1 = 'result.jpg' #7230*6742
    im2 = 'result3.jpg' #7222*6738
    m = Match(im1, im2)
    pts1, pts2, img3 = m.extract()
    cv2.imwrite('match.jpg', img3)




