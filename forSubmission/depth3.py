# 距離情報の利用

import pyrealsense2 as rs # ライブラリ（PyRealsense2）のインポート
import numpy as np # ライブラリ（NumPy）のインポート
import cv2 # ライブラリ（OpenCV）のインポート

# ストリーム(Depth/Color)の設定
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30) # ストリーム(Color)の設定
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30) # ストリーム(Depth)の設定
config.enable_stream(rs.stream.infrared, 640, 480, rs.format.y8, 30) # ストリーム(Infrared)の設定
config.enable_record_to_file('./data/d415data_distanceImage.mp4') # ファイル名を設定


pipeline = rs.pipeline()
profile = pipeline.start(config) # ストリーミング開始

#   距離[m] = depth * depth_scale
depth_sensor = profile.get_device().first_depth_sensor() # ？？？？？
depth_scale = depth_sensor.get_depth_scale() # 深度画像の単位とメートル間のマッピングを取得し、depth_scaleに代入
clipping_distance_in_meters = 1.0 # meter
clipping_distance = clipping_distance_in_meters / depth_scale

# Alignオブジェクト生成
align_to = rs.stream.color # depth_framesを整列するストリームタイプをalign_toに代入（英語のドキュメントをそのまま和訳しているため？？？？？）
align = rs.align(align_to) #rs.alignを用いてdepth_framesを他のフレームに位置合わせをし、alignに代入（英語のドキュメントをそのまま和訳しているため？？？？？）

try:
    while True:
        # フレーム待ち(Color & Depth)
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames) # 指定されたframesで位置合わせプロセスを実行して位置合わせされたフレームのセットを取得し、戻り値をaligned_framesに代入
        color_frame = aligned_frames.get_color_frame() # aligned_frames.get_color_frameで最初のカラーフレームを取得し、戻り値をcolor_frameに代入
        depth_frame = aligned_frames.get_depth_frame() # aligned_frames.get_depth_frameで最初のカラーフレームを取得し、戻り値をdepth_frameに代入
        if not depth_frame or not color_frame: # depth_frameかcolor_frameが取得できなかった時
            continue # while文の先頭に戻る

        color_image = np.asanyarray(color_frame.get_data()) # color_frameに代入された値を基に2次元配列を生成し（ndarray）、color_imageに代入
        depth_image = np.asanyarray(depth_frame.get_data()) # depth_frameに代入された値を基に2次元配列を生成し（ndarray）、depth_imageに代入
        # Depth画像前処理(1m以内を画像化)
        grey_color = 153 # ？？？？？ gray_colorの値を153と定義
        depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) # 2次元配列（depth_image, depth_image,depth_image）を横に結合し、depth_image_3dに代入
        bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, color_image) # depth_image_3d > clipping_distanceかdepth_image_3d <= 0を満たす時、gray_colorとcolor_imageをbg_removedに代入

        # レンダリング
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET) # 擬似カラー（カラーマップ）変換 convertScaleAbsとは
        images = np.hstack((bg_removed, depth_colormap)) # 2次元配列（color_removed, depth_colormap）を横に結合し、imagesに代入
        cv2.namedWindow('Align Example', cv2.WINDOW_AUTOSIZE) # ウィンドウの設定
        cv2.imshow('RealSense', images) # Depth画像を表示
        if cv2.waitKey(1) & 0xff == 27: # ESC key を押した時
            break # 処理を終了

finally:
    pipeline.stop() # ストリーミング停止
    cv2.destroyAllWindows() # ウィンドウを閉じる