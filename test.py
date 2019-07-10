from match import Match
import cv2

# feature extract and match
path1 = 'test/im1.jpg'
path2 = 'test/im2.jpg'
m = Match(path1, path2)
kpts1, kpts2 = m.extract()

# do stereoCalibrate()
cv2.stereoRectify()





