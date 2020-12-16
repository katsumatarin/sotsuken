# ライブラリのインポート
import pyrealsense2 as rs
import numpy as np
import cv2
import os

def capture_depth_image(output_video_file_name):
  TARGET_DISTANCE = 2 # 2m以上は表示しない

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
  out = cv2.VideoWriter(output_video_file_name, fourcc, 24, (640, 480))

  if out.isOpened() == False:
      print('File {0} open error.'.format(output_video_file_name))
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

def save_frame_sec(video_path, sec, result_path):
  cap = cv2.VideoCapture(video_path)

  if not cap.isOpened():
      return

  os.makedirs(os.path.dirname(result_path), exist_ok=True)

  fps = cap.get(cv2.CAP_PROP_FPS)

  cap.set(cv2.CAP_PROP_POS_FRAMES, round(fps * sec))

  ret, frame = cap.read()

  if ret:
      cv2.imwrite(result_path, frame)

# 指定した画像(path)の物体を検出し、外接矩形の画像を出力
def detect_contour(path):

  # 画像を読込
  src = cv2.imread(path, cv2.IMREAD_COLOR)

  # グレースケール画像へ変換
  gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

  # 2値化
  retval, bw = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

  # 輪郭を抽出
  #   contours : [領域][Point No][0][x=0, y=1]
  #   cv2.CHAIN_APPROX_NONE: 中間点も保持する
  #   cv2.CHAIN_APPROX_SIMPLE: 中間点は保持しない
  contours, hierarchy = cv2.findContours(bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

  # 矩形検出された数（デフォルトで0を指定）
  detect_count = 0

  # 各輪郭に対する処理
  for i in range(0, len(contours)):

    # 輪郭の領域を計算
    area = cv2.contourArea(contours[i])

    # ノイズ（小さすぎる領域）と全体の輪郭（大きすぎる領域）を除外
    if area < 1e2 or 1e5 < area:
      continue

    # 外接矩形
    if len(contours[i]) > 0:
      rect = contours[i]
      x, y, w, h = cv2.boundingRect(rect)
      cv2.rectangle(src, (x, y), (x + w, y + h), (0, 255, 0), 2)

      # 外接矩形毎に画像を保存
      path_dir_base, path_ext = os.path.splitext(path)
      out_path = path_dir_base + '_detect' + path_ext

      cv2.imwrite(out_path, src[y:y + h, x:x + w])

      detect_count = detect_count + 1

  if detect_count > 10:
    print('部屋が汚れています！大至急片付けましょう！')
  elif detect_count > 0:
    print('部屋が少し汚いので片付けてください！')
  else:
    print('とても綺麗です！このまま継続しましょう！')

  # 外接矩形された画像を表示
  cv2.imshow('output', src)
  cv2.waitKey(0)

  # 終了処理
  cv2.destroyAllWindows()

if __name__ == '__main__':
  print("出力ファイル名を入力してください")
  output_name = input()
  os.makedirs(f'../data/out/{output_name}')

  output_video_file_name = f'../data/out/{output_name}/{output_name}.mp4'
  capture_depth_image(output_video_file_name)

  while(True):
    print(f"何秒目の部屋の散らかりをチェックしますか？終了する場合は-1を入力してください。")
    sec = int(input())

    if sec == -1:
      break

    output_image_file_name = f'../data/out/{output_name}/{output_name}_{sec}sec.jpg'
    save_frame_sec(output_video_file_name, sec, output_image_file_name)
    detect_contour(output_image_file_name)

  os.remove(output_video_file_name)
