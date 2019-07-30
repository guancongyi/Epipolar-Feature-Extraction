# epipolar_feature_extraction

project folder
-- data
 -- image1.jpg
 -- ...
-- out
 -- image1.jpg
 -- ...
-- matches
 -- matched_img1.jpg
 -- ...
-- goodmatches
 -- goodmatched_img1.jpg
 -- ...

0. pix4d folder should contain three files generated from pix4d:
   test_calibrated_external_camera_parameters_wgs84.txt         # this contains euler angles
   test_calibrated_internal_camera_parameters.cam               # this contains internal parameter
   test_calibrated_images_position.txt                          # this contains image position 
                                                                  in UTM projection
   
1. run preprocess to extract information extrinsic/intrinsic parameters, and image positions and so on. 
    A file named extrinsic.db will be created 
    in the same directory as the project.

2. run rectification to get the rectified images(epipolar images). 

3. run epipolar to get the good matches between two pictures, and get the XYZ location in UTM 
   for each point.