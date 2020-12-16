#グリッド線を引く

import cv2

fname0 = "./data/temp/result_0sec.jpg"
fname40 = "./data/temp/result_40sec.jpg"

y_step=20 #高さ方向のグリッド間隔(px)
x_step=20 #幅方向のグリッド間隔(px)

img0 = cv2.imread(fname0) #画像を読み出しオブジェクトimg0に代入
img40 = cv2.imread(fname40) #画像を読み出しオブジェクトimg40に代入

#オブジェクトimgのshapeメソッドの1つ目の戻り値(画像の高さ)をimg_yに、2つ目の戻り値(画像の幅)をimg_xに
img0_y,img0_x=img0.shape[:2]
img40_y,img40_x=img40.shape[:2]

#横線を引く
img0[y_step:img0_y:y_step, :, :] = 255
img40[y_step:img40_y:y_step, :, :] = 255
#縦線を引く
img0[:, x_step:img0_x:x_step, :] = 255
img40[:, x_step:img40_x:x_step, :] = 255

cv2.imwrite('./data/temp/0sec_grid.png',img0) #img0を保存
cv2.imwrite('./data/temp/40sec_grid.png',img40) #img40を保存