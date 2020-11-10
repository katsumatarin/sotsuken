# coding: utf-8

#############################################
# ファイルへの保存
#############################################

import pyrealsense2 as rs # ライブラリ（PyRealsense2）のインポート
import numpy as np # ライブラリ（NumPy）のインポート
import cv2 # ライブラリ（OpenCV）のインポート


# ストリーム(Color/Depth)の設定
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.infrared, 640, 480, rs.format.y8, 30)
# ↓ ここでファイル名設定
config.enable_record_to_file('./data/d415data.bag')

pipeline = rs.pipeline()
profile = pipeline.start(config) # ストリーミング開始

try:
    while True:
      　# フレーム待ち(Color & Depth)
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame() # frames.get_color_frameで最初のカラーフレームを取得し、戻り値をcolor_frameに代入
        depth_frame = frames.get_depth_frame() # frames.get_depth_frameで最初の深度フレームを取得し、戻り値をdepth_frameに代入
        if not depth_frame or not color_frame: # depth_frameかcolor_frameが取得できなかった時
            continue # while文の先頭に戻る
        color_image = np.asanyarray(color_frame.get_data()) # color_frameに代入された値を基に2次元配列を生成し（ndarray）、color_imageに代入

        # Depth画像
        depth_color_frame = rs.colorizer().colorize(depth_frame) # ？？？？？ 取得した深度フレームを基にカラー画像を生成し、depth_color_frameに代入
        depth_color_image = np.asanyarray(depth_color_frame.get_data()) # depth_color_frameに代入された値を基に2次元配列を生成し（ndarray）、depth_color_imageに代入

        # 表示
        images = np.hstack((color_image, depth_color_image)) # 2次元配列（color_image, depth_color_image）を横に結合し、imagesに代入
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE) # ウィンドウの設定
        cv2.imshow('RealSense', images) # Depth画像を表示
        if cv2.waitKey(1) & 0xff == 27: # ESC key を押した時
            break # 処理を終了

finally:
    pipeline.stop() # ストリーミング停止
    cv2.destroyAllWindows() # ウィンドウを閉じる