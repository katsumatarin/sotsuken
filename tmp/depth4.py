# -*- coding: utf-8 -*-

#############################################
##      D415 Depth画像の表示&キャプチャ
#############################################
# ライブラリのインポート
import pyrealsense2 as rs
import numpy as np
import cv2

TARGET_DISTANCE = 2 # 2m以上は表示しない
OUTPUT_VIDEO_FILE = './data/temp/sample_depth2.mp4'

# ストリーム(Depth/Color)の設定
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# ストリーミング開始
profile = pipeline.start(config)

# Depthスケール取得
#   距離[m] = depth * depth_scale
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
# 対象範囲の閾値
distance_max = TARGET_DISTANCE/depth_scale
print('Depth Scale = {} -> {}'.format(depth_scale, distance_max))

# Output file
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter(OUTPUT_VIDEO_FILE, fourcc, 24, (640, 480))

if out.isOpened() == False:
    print('File {0} open error.'.format(OUTPUT_VIDEO_FILE))
    exit()

try:
    while True:
        # フレーム待ち(Depth & Color)
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue
        color_image = np.asanyarray(color_frame.get_data())
        # Depth画像前処理(2m以内を画像化)
        depth_image = np.asanyarray(depth_frame.get_data())
        depth_image = (depth_image < distance_max) * depth_image
        depth_graymap = depth_image * 255. / distance_max
        depth_graymap = depth_graymap.reshape((480, 640)).astype(np.uint8)
        depth_colormap = cv2.cvtColor(depth_graymap, cv2.COLOR_GRAY2BGR)

        # 入力画像表示
        images = np.hstack((color_image, depth_colormap))
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        out.write(depth_colormap)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break


finally:
    # ストリーミング停止
    pipeline.stop()
    cv2.destroyAllWindows()