# epipolar_feature_extraction

0. pix4d folder should contain three files generated from pix4d:
   test_calibrated_external_camera_parameters_wgs84.txt
   test_calibrated_internal_camera_parameters.cam
   test_calibrated_images_position.txt
   
1. run preprocess to extract information extrinsic parameters from external_camera_parameters....txt
   and intrinsic parameters from the other file.

2. run rectification to get the rectified images(epipolar images)

3. run epipolar to get the good matches between two pictures.