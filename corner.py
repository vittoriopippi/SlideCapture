import cv2
import numpy as np

def search_exact_corner(img, ptn, radius=10):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)
    mask = np.zeros_like(dst)
    cv2.circle(mask, ptn, radius, 1, thickness=-1)
    dst *= mask
    corner = dst.argmax()
    ptn_found = np.unravel_index(corner, gray.shape)[::-1]
    if ptn_found == (0,0):
        ptn_found = ptn
    return ptn_found


if __name__ == "__main__":
    filename = 'dataset/screen.png'
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.04)

    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)

    # Threshold for an optimal value, it may vary depending on the image.
    img[dst>0.01*dst.max()]=[0,0,255]

    cv2.namedWindow('dst', cv2.WINDOW_NORMAL)
    cv2.imshow('dst',img)
    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()