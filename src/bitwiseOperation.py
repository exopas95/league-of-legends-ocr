import cv2


# Masking frame
def bit_operation(frame):
    # read mask image
    m_image = cv2.imread('./data/img/img_mask.png')

    # convert colors to black and white
    image_to_gray = cv2.cvtColor(m_image, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(image_to_gray, 10, 255,
                              cv2.THRESH_BINARY)    # apply THRESH_BINARY

    # bitwise operation on mask image
    mask_bg = cv2.bitwise_and(frame, frame, mask=mask)
    return mask_bg
  
    # will be removed
    # cv2.imshow('image', mask_bg)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


# frame = cv2.imread('1107_screen.png')
# bit_operation(frame)
