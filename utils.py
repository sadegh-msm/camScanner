import numpy as np
import os
from PIL import Image
from matplotlib import pyplot as plt


def get_input(file_name):
    img = Image.open(file_name)
    img = np.asarray(img)
    img = to_mtx(img)
    return img


def to_mtx(img):
    """
    This method just reverse x and y of an image matrix because of the different order of x and y in PIL and Matplotlib library
    """
    H, V, C = img.shape
    mtr = np.zeros((V, H, C), dtype='int')
    for i in range(img.shape[0]):
        mtr[:, i] = img[i]
    return mtr


def get_coef(a, b, n):
    res = []
    b = [b[0], b[1], 1]
    dim = 3
    for i in range(dim):
        curr = [0] * dim * 4
        curr[i] = a[0]
        curr[dim + i] = a[1]
        curr[2 * dim + i] = 1 if i != 2 else 0

        curr[3 * dim + n - 1] = -b[i]
        res.append(curr)

    return res


def getPerspectiveTransform(pts1, pts2):
    A = []
    plen = len(pts1)

    for i in range(plen):
        A += get_coef(pts1[i], pts2[i], i)

    B = [0, 0, -1] * plen
    C = np.linalg.solve(A, B)

    res = np.ones(9)
    res[:8] = C.flatten()[:8]

    return res.reshape(3, -1).T


def showWarpPerspective(dst):
    width, height, _ = dst.shape

    # This part is for denoising the result matrix . You can use this if at first you have filled matrix with zeros
    for i in range(width - 1, -1, -1):
        for j in range(height - 1, -1, -1):
            if dst[i][j][0] == 0 and dst[i][j][1] == 0 and dst[i][j][2] == 0:
                if i + 1 < width and j - 1 >= 0:
                    dst[i][j] = dst[i + 1][j - 1]

    showImage(dst, title='Warp Perspective')


def showImage(image, title, save_file=True):
    final_ans = to_mtx(image)
    final_ans = final_ans.astype(np.uint8)

    plt.title(title)
    plt.imshow(final_ans)

    if save_file:
        try:
            os.mkdir('out')
        except OSError:
            pass
        path = os.path.join('out', title + '.jpg')
        plt.savefig(path, bbox_inches='tight')

    plt.show()


def Filter(img, filter_matrix):
    m, n, l = img.shape
    res = np.zeros((m, n, l))

    for i in range(m):
        for j in range(n):
            reshaped = np.reshape(img[i, j, :], newshape=(3,))
            res[i, j, :] = filter_matrix.dot(reshaped)

    return res
