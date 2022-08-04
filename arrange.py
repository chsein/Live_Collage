import cv2
import numpy as np
import pyautogui as pg
import matplotlib.pyplot as plt

def crop_blank(img):

    '''Segmentaion 된 이미지의 여백 부분을 상하좌우로 오려내기 위한 function'''

    for i in range(img.shape[0]):
        if sum(sum(img[i]))==0:
            continue
        else :
            temp_up=i;
            #print('temp_up :', temp_up);
            break

    for i in range(img.shape[0]):
        j=img.shape[0]-1-i
        if sum(sum(img[j]))==0:
            continue
        else :
            temp_down=j;
            #print('temp_down :', temp_down);
            break

    img_T=img.transpose((1,0,2));

    for i in range(img.shape[1]):
        if sum(sum(img_T[i]))==0:
            continue
        else :
            temp_left=i;
            #print('temp_left :', temp_left);
            break

    for i in range(img.shape[1]):
        j = img.shape[1] - 1 - i
        if sum(sum(img_T[j]))==0:
            continue

        else :
            temp_right=j;
            #print('temp_right :', temp_right);
            break

    img_crop=img[temp_up:temp_down+1,temp_left:temp_right+1,:];

    return img_crop;

def decision_position(img_list):

    '''Segmentaion 된 이미지를 순서별로 각 배경의 위치로 이동시키기 위한 좌표 얻는 function
        - 현재 가지고 있는 6장의 이미지에 맞춘 가중치 적용으로 어떤 이미지가 들어오든간에 오류안나게 확자해야 함'''

    center_index= round(img_list[-1].shape[1]/2) , round(0.5*img_list[-1].shape[0]);
    index_tuple=[]

    for i in range(len(img_list)):
        if i == 6:
            break

        temp = np.zeros(image_list[-1].shape, dtype='uint8');
        center_obj=round(img_list[i].shape[1]/2) , round(0.5*img_list[i].shape[0]);

        if i == 0:
            x_obj= center_index[0];
            y_obj = center_index[1]+1.3*center_obj[1];


        elif i == 5:
            x_obj= center_index[0];
            y_obj = center_index[1]-3*center_obj[1];

        elif i == 1:
            x_obj = center_index[0]-1*center_obj[0];
            y_obj= np.tan(-1/3*np.pi)*(x_obj-center_index[0])+center_index[1];


        elif i == 4:
            x_obj = center_index[0] + 0.7 * center_obj[0];
            y_obj = np.tan(-1 / 6 * np.pi)*(x_obj - center_index[0]) + center_index[1];

        elif i == 2:
            x_obj = center_index[0] + 0.7 * center_obj[0];
            y_obj = np.tan(1 / 3 * np.pi)*(x_obj - center_index[0]) + center_index[1];

        elif i == 3:
            x_obj = center_index[0] - 0.5 * center_obj[0];
            y_obj = np.tan(1 / 6 * np.pi)*(x_obj - center_index[0]) + center_index[1];

        index_tuple.append((round(x_obj),round(y_obj)))

    return index_tuple

def padding_position(img_list):

    '''각 객체별 좌표를 가지고 크롭된 이미지를 패딩된 이미지 위에 씌워 배경과 같은 사이즈로 만들어줌'''
    
    index_tuple=decision_position(img_list);
    padding_image_list = [];

    for i in range(len(img_list)):
        if i == 6:
            padding_image_list.append(img_list[-1]);
            break

        temp = np.zeros(image_list[-1].shape, dtype='uint8');
        x_ = image_list[i].shape[1];  # 일반 list 와 np.ndarray x,y 인덱스 위치 차이
        y_ = image_list[i].shape[0];
        x = round(index_tuple[i][0] - 0.5 * x_);
        y = round(index_tuple[i][1] - 0.5 * y_);

        temp[y:y + y_, x:x + x_, :] = img_list[i];
        padding_image_list.append(temp);


    return padding_image_list

def projection_image(img_list):
    ''' 순위가 높은 이미지가 제일 위, 배경이 제일 아래라 생각하고 쌓인 이미지를
    위에서 아래로 투영한다고 생각하고 짠 함수'''


    final_image = np.zeros(img_list[-1].shape, dtype='uint8');
    for x_index in range(img_list[-1].shape[1]):
        for y_index in range(img_list[-1].shape[0]):
            for z_index in range(len(img_list)):
            # if padding_image_list[z_index][y_index,x_index,:]==np.array([0,0,0],dtype='uint8'):
                if sum(img_list[z_index][y_index, x_index, :]) == 0:
                    continue
                else:
                    final_image[y_index, x_index, :] = img_list[z_index][y_index, x_index, :];
                    break

    return final_image

image_list=[];


#1 segmentation original 이미지 하나의 list에 저장
#2 BGR에서 RGB 순으로 파일 정렬
#3 임시로 배경과 객체 사이즈 적은 범위 내로 고정

for i in range(1,8):
    if i<7:
        temp = cv2.imread('ex_' + str(i) + '.png', cv2.IMREAD_COLOR);
        temp = cv2.cvtColor(temp, cv2.COLOR_BGR2RGB); #2
        temp=crop_blank(temp);
        temp=cv2.resize(temp, [400,round(400*temp.shape[0]/temp.shape[1])]); #3

    else :
        temp=cv2.imread('g_sunny.jpg', cv2.IMREAD_COLOR);
        temp = cv2.cvtColor(temp, cv2.COLOR_BGR2RGB); #2
        temp = crop_blank(temp);
        temp = cv2.resize(temp, [1000, round(1000*temp.shape[0]/temp.shape[1])]);  #3

    image_list.append(temp);

after_padd=padding_position(image_list);
final_image=projection_image(after_padd);

plt.figure();
plt.imshow(final_image);


