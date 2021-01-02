import cv2
import src.constants as constants
from PIL import Image

# Additional mask work for better performance
def text_image_attach(img, g_type): 
    mask_image_num = cv2.imread(constants.IMAGE_PATH + '\\img_num.png')
    height, width = mask_image_num.shape[:2]

    if g_type == 'LEC':
        vec = constants.vec_LEC
    elif g_type == 'LCS':
        vec = constants.vec_LCS
    else:
        vec = constants.vec

    for i in vec.keys():
        if (i == "level") or (i == 'vision_score'):
            mask_image_num_resize = cv2.resize(mask_image_num, (int(width * 4/7), int(height * 4/7)), interpolation = cv2.INTER_LINEAR)
        elif i == "tower_score":
            mask_image_num_resize = cv2.resize(mask_image_num, (int(width * 5/7), int(height * 5/7)), interpolation = cv2.INTER_LINEAR)
        elif i == "set_score":
            mask_image_num_resize = cv2.resize(mask_image_num, (int(width * 9/7), int(height * 9/7)), interpolation = cv2.INTER_LINEAR)
        for j in range(len(vec[i])):
            x, y = int(vec[i][j][0]*1920),int(vec[i][j][1]*1080)
            # img.paste(mask_image_num_resize, (x,y), mask_image_num_resize)
            img[y:y + mask_image_num_resize.shape[0],
                x:x + mask_image_num_resize.shape[1]] = mask_image_num_resize

    return img

# Masking frame
def bit_operation(frame, g_type):
    
    # Define game type
    if g_type == "LCS":
        mask_img = "\\img_mask_LCS.png"
    elif g_type == "LEC":
        mask_img = "\\img_mask_LEC.png"
    else:
        mask_img = "\\img_mask_LCK.png"

    # read mask image
    m_image = cv2.imread(constants.IMAGE_PATH + mask_img)

    # convert colors to black and white
    image_to_gray = cv2.cvtColor(m_image, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(image_to_gray, 10, 255,
                              cv2.THRESH_BINARY)    # apply THRESH_BINARY

    # bitwise operation on mask image
    mask_bg = cv2.bitwise_and(frame, frame, mask=mask)
    
    # Additional mask 
    mask_result = text_image_attach(mask_bg, g_type)

    # if g_type == "LEC":
    #     t_vec = constants.coord_dict_LEC
    # elif g_type == "LCS":
    #     t_vec = constants.coord_dict_LCS
    # else:
    #     t_vec = constants.coord_dict
        
    # for coord in t_vec:
    #     cv2.rectangle(mask_result, (int(t_vec[coord][0]*1920), int(t_vec[coord][2]*1080)), (int(t_vec[coord][1]*1920), int(t_vec[coord][3]*1080)), (0, 0, 255), 1)

    # cv2.imshow('rectangle', mask_result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return mask_result