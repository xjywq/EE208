import os

import cv2

LOGO_DATASET_PATH = os.path.join(
    os.getcwd(), 'app', 'logo_search', 'logo', 'train')


def logo_matching(target_img_path):
    image1 = cv2.imread(target_img_path, cv2.IMREAD_GRAYSCALE)
    print(image1.shape)
    img_list = os.listdir(LOGO_DATASET_PATH)
    best_match_img = ''
    best_match_num = 0
    for img in img_list:
        img_path = os.path.join(LOGO_DATASET_PATH, img)
        image2 = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        # print(image1.shape, image2.shape)
        sift = cv2.xfeatures2d.SIFT_create()
        kp1, des1 = sift.detectAndCompute(image1, None)
        kp2, des2 = sift.detectAndCompute(image2, None)
        # @params:ratio
        ratio = 0.6
        # K近邻算法求取在空间中距离最近的K个数据点，并将这些数据点归为一类
        matcher = cv2.BFMatcher()
        raw_matches = matcher.knnMatch(des1, des2, k=2)
        good_matches = []
        for m1, m2 in raw_matches:
            #  如果最接近和次接近的比值大于一个既定的值，那么我们保留这个最接近的值，认为它和其匹配的点为good_match
            if m1.distance < ratio * m2.distance:
                good_matches.append([m1])
        # print(img, len(good_matches), sep=' ')
        if len(good_matches) > best_match_num:
            best_match_num = len(good_matches)
            best_match_img = img
    brand = best_match_img.split('_')[0]
    if brand == 'puma':
        return "彪马"
    return brand


# puma
if __name__ == '__main__':
    target_path = 'logo/test.jpg'
    print(logo_matching(target_path))
