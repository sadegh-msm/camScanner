import utils
from utils import *
import numpy as np


def warpPerspective(img, transform_matrix, output_width, output_height):
    width_img, height_img, depth_img = img.shape

    img2 = np.zeros((output_width, output_height, depth_img), dtype='float')

    for i in range(width_img):
        for j in range(height_img):
            array_x = np.full((3, 1), 1)
            array_x[0][0] = i
            array_x[1][0] = j
            array_x = np.dot(transform_matrix, array_x)
            xx = array_x[0][0] / array_x[2][0]
            yy = array_x[1][0] / array_x[2][0]

            if xx < output_width and yy < output_height:
                if xx >= 0 and yy >= 0:
                    img2[int(xx)][int(yy)] = img[i][j]

    return img2.astype(np.uint8)


def grayScaledFilter(img):
    width_img, height_img, depth_img = img.shape

    img2 = np.zeros((width_img, height_img, depth_img), dtype='float')
    gray = np.array([0.299, 0.587, 0.114])
    img2 = utils.Filter(img, gray)

    return img2


def crazyFilter(img):
    # transformation matrix
    crazy = np.array([[0, 0, 1],
                     [0, 0.5, 0],
                     [0.5, 0.5, 0]])
    # crazy filter
    img2 = utils.Filter(img, crazy)
    invert = np.linalg.inv(crazy)
    # Inverted Crazy Filter
    img3 = utils.Filter(img2, invert)

    return img2, img3


def scaleImg(img, scale_width, scale_height):
    width_img, height_img, depth_img = img.shape

    img2 = np.zeros((scale_width * width_img, scale_height * height_img, depth_img), dtype='float')

    for i in range(width_img * scale_width):
        for j in range(height_img * scale_height):
            img2[i][j] = img[int(i / scale_width)][int(j / scale_height)]

    return img2


def permuteFilter(img):
    width_img, height_img, _ = img.shape

    for i in range(width_img):
        for j in range(height_img):
            temp = img[i][j][2]
            img[i][j][2] = img[i][j][0]
            img[i][j][0] = temp
    return img


if __name__ == "__main__":
    image_matrix = get_input('pic.jpg')

    width, height = 300, 400

    # upperLeftX = input("upper left x:")
    # upperLeftY = input("upper left y:")
    # upperRightX = input("upper right x:")
    # upperRightY = input("upper right y:")
    # downLeftX = input("down left x:")
    # downLeftY = input("down left y:")
    # downRightX = input("down right x:")
    # downRightY = input("down right y:")

    show_image(image_matrix, title="Input Image")

    pts1 = np.float32([[250, 20], [600, 180], [260, 980], [620, 900]])
    # pts1 = np.float32([[upperLeftX, upperLeftY], [upperRightX, upperRightY], [downLeftX, downLeftY], [downRightX,
    # downRightY]])

    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    m = get_perspective_transform(pts1, pts2)

    warpedImage = warpPerspective(image_matrix, m, width, height)
    show_warp_perspective(warpedImage)

    grayScalePic = grayScaledFilter(warpedImage)
    show_image(grayScalePic, title="Gray Scaled")

    crazyImage, invertedCrazyImage = crazyFilter(warpedImage)
    show_image(crazyImage, title="Crazy Filter")
    show_image(invertedCrazyImage, title="Inverted Crazy Filter")

    scaledImage = scaleImg(warpedImage, 3, 4)
    show_image(scaledImage, title="Scaled Image")

    permuteImage = permuteFilter(warpedImage)
    show_image(permuteImage, title="Permuted Image")
