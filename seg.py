import cv2
import numpy as np
import tensorflow as tf

IMAGE_SIZE = 512

def makeWhiteEdge(img_arr, k_size=3, iterations=3):
    pad_num = 50
    paddings = tf.constant([[pad_num, pad_num], [pad_num, pad_num]])
    try:
        r,g,b,alpha = img_arr[:,:,0], img_arr[:,:,1], img_arr[:,:,2], img_arr[:,:,3]        
        r,g,b,alpha = (np.array(tf.pad(r, paddings, "CONSTANT")), 
                       np.array(tf.pad(g, paddings, "CONSTANT")), 
                       np.array(tf.pad(b, paddings, "CONSTANT")),
                       np.array(tf.pad(alpha, paddings, "CONSTANT")) )
        img_arr = np.stack([r,g,b,alpha], axis=2)
        im_alpha = img_arr[:,:,3]

        kernel = np.ones((k_size,k_size), np.uint8)
        result = cv2.dilate(im_alpha, kernel, iterations=iterations)

        white_space_mask = np.stack([np.where(result - im_alpha>0, True,False)]*3, axis=2)

        img_arr[:,:,3] = result
        img_arr[:,:,:3][white_space_mask] = 255
#         img_arr = np.stack([img_arr[:,:,2], img_arr[:,:,1], img_arr[:,:,0], img_arr[:,:,3]], axis=2)
#         print('d')
        return crop_blank(img_arr)
    except:
        return crop_blank(img_arr)
    
def crop_blank(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY);
    index = cv2.boundingRect(gray);
    (x,y,w,h)=index;
    img_crop = img[y:y + h + 1, x : x + w + 1, :];

    return img_crop

def read_image(image_path, original=False):
    image = tf.io.read_file(image_path)
    image = tf.image.decode_png(image, channels=3)
    image.set_shape([None, None, 3])
    if not original:
        image = tf.image.resize(images=image, size=[IMAGE_SIZE, IMAGE_SIZE])
        image = image/255
    return image

def segSave(model, image_path, save_path=None):
    original_image = read_image(image_path, original=True)
    input_image = read_image(image_path)
    input_pred = model.predict(input_image[np.newaxis,...])

    thresh_hold = 0.4
    pred_mask = input_pred > thresh_hold
    alpha = cv2.resize(np.squeeze(np.where(pred_mask, 1.0,0)), (original_image.shape[1], original_image.shape[0]))
    alpha = np.where(alpha>0,1,0).astype(np.float32)

    try:
        pad_num = 50
        paddings = tf.constant([[pad_num, pad_num], [pad_num, pad_num]])
        padded = np.array(tf.pad(alpha, paddings, "CONSTANT"))
        contours_coor ,info = cv2.findContours(padded.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        info_ = np.where(info[0][:,-1]==-1)[0]
        for i, num in enumerate(info_):
            contour_coor = contours_coor[num]
            if i == 0:
                filled_hole = cv2.fillPoly(padded.astype(np.uint8), [np.squeeze(contour_coor)], 255)
            else :
                filled_hole = cv2.fillPoly(filled_hole, [np.squeeze(contour_coor)], 255)
        filled_hole_ = filled_hole[pad_num:padded.shape[0]-pad_num, pad_num:padded.shape[1]-pad_num]
        filed_mask = np.where(filled_hole_[...,np.newaxis] > 0, 1,0)
        masked_image = original_image * filed_mask
        masked_image_png = np.concatenate([masked_image[:,:,2][...,np.newaxis], masked_image[:,:,1][...,np.newaxis],
                                        masked_image[:,:,0][...,np.newaxis] ,(filed_mask).astype(np.uint8)*255], axis=2)
    except:
        alpha_ = alpha[...,np.newaxis]
        masked_image = original_image * alpha_
        masked_image_png = np.concatenate([masked_image[:,:,2][...,np.newaxis], masked_image[:,:,1][...,np.newaxis],
                                        masked_image[:,:,0][...,np.newaxis], (alpha_).astype(np.uint8)*255 ], axis=2)
    
    if save_path:
        cv2.imwrite(save_path, masked_image_png)

    return masked_image_png

# def segSave(model, image_path, save_path=None):
#     original_image = read_image(image_path, original=True)
#     input_image = read_image(image_path)
#     input_pred = model.predict(input_image[np.newaxis,...])

#     thresh_hold = 0.3
#     pred_mask = input_pred > thresh_hold
#     alpha = cv2.resize(np.squeeze(np.where(pred_mask, 1.0,0)), (original_image.shape[1], original_image.shape[0]))
#     alpha = np.where(alpha>0,1,0).astype(np.float32)

#     try:
#         contours_coor ,info = cv2.findContours(alpha.astype(np.uint8), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
#         info_ = np.where(info[0][:,-1]==-1)[0]
#         for i, num in enumerate(info_):
#             contour_coor = contours_coor[num]
#             if i == 0:
#                 filled_hole = cv2.fillConvexPoly(alpha.astype(np.uint8), np.squeeze(contour_coor), 255)
#             else :
#                 filled_hole = cv2.fillConvexPoly(filled_hole, np.squeeze(contour_coor), 255)
#         filed_mask = np.where(filled_hole[...,np.newaxis] > 0, 1,0)
#         masked_image = original_image * filed_mask
#         masked_image_png = np.concatenate([masked_image[:,:,2][...,np.newaxis], masked_image[:,:,1][...,np.newaxis],
#                           masked_image[:,:,0][...,np.newaxis] ,(filed_mask).astype(np.uint8)*255], axis=2)
#     except:
#         alpha_ = alpha[...,np.newaxis]
#         masked_image = original_image * alpha_
#         masked_image_png = np.concatenate([masked_image[:,:,2][...,np.newaxis], masked_image[:,:,1][...,np.newaxis],
#                                            masked_image[:,:,0][...,np.newaxis], (alpha_).astype(np.uint8)*255 ], axis=2)
#     if save_path:
#         cv2.imwrite(save_path, masked_image_png)

#     return masked_image_png