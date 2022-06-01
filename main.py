import utils
from utils import *
import numpy as np


def warpPerspective(img, transform_matrix, output_width, output_height):
    img2 = np.zeros((output_width, output_height, 3), dtype='float')

    for i in range(800):
        for j in range(1000):
            arrayX = np.full((3, 1), 1)
            arrayX[0][0] = i
            arrayX[1][0] = j
            arrayX = np.dot(transform_matrix, arrayX)
            xx = arrayX[0][0] / arrayX[2][0]
            yy = arrayX[1][0] / arrayX[2][0]

            if xx < output_width and yy < output_height:
                img2[int(xx)][int(yy)] = img[i][j]

    return img2


def grayScaledFilter(img):
    gray = np.array([0.299, 0.587, 0.114])
    img2 = utils.Filter(img, gray)
    return img2


def crazyFilter(img):
    crazy = np.array([[0, 0, 1],
                     [0, 0.5, 0],
                     [0.5, 0.5, 0]])
    img2 = utils.Filter(img, crazy)
    invert = np.linalg.inv(crazy)
    img3 = utils.Filter(img2, invert)
    return img2, img3


def scaleImg(img, scale_width, scale_height):
    img2 = np.zeros((scale_width * 300, scale_height * 400, 3), dtype='int')

    for i in range(300 * scale_width):
        for j in range(400 * scale_height):
            img2[i][j] = img[int(i / scale_width)][int(j / scale_height)]

    return img2


def permuteFilter(img):
    for i in range(300):
        for j in range(400):
            temp = img[i][j][2]
            img[i][j][2] = img[i][j][0]
            img[i][j][0] = temp
    return img


if __name__ == "__main__":
    image_matrix = get_input('pic.jpg')

    # You can change width and height if you want
    width, height = 300, 400

    # upperLeftX = input("upper left x:")
    # upperLeftY = input("upper left y:")
    # upperRightX = input("upper right x:")
    # upperRightY = input("upper right y:")
    # downLeftX = input("down left x:")
    # downLeftY = input("down left y:")
    # downRightX = input("down right x:")
    # downRightY = input("down right y:")

    showImage(image_matrix, title="Input Image")

    pts1 = np.float32([[250, 20], [600, 180], [260, 980], [620, 900]])
    # pts1 = np.float32([[upperLeftX, upperLeftY], [upperRightX, upperRightY], [downLeftX, downLeftY], [downRightX,
    # downRightY]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    m = getPerspectiveTransform(pts1, pts2)

    warpedImage = warpPerspective(image_matrix, m, width, height)
    showWarpPerspective(warpedImage)

    grayScalePic = grayScaledFilter(warpedImage)
    showImage(grayScalePic, title="Gray Scaled")

    crazyImage, invertedCrazyImage = crazyFilter(warpedImage)
    showImage(crazyImage, title="Crazy Filter")
    showImage(invertedCrazyImage, title="Inverted Crazy Filter")

    scaledImage = scaleImg(warpedImage, 3, 4)
    showImage(scaledImage, title="Scaled Image")

    permuteImage = permuteFilter(warpedImage)
    showImage(permuteImage, title="Permuted Image")
    showImage(image_matrix, title="Input Image")
