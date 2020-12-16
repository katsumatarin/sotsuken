import chirakari_hantei
import daily_check

if __name__ == '__main__':
  print('散らかり判定をしたい場合は1, ゴミ捨てチェックをしたいときは2を入力してください')
  val = int(input())
  if val == 1:
    chirakari_hantei.chirakari_hantei()
  elif val == 2:
    daily_check.daily_check()
  else:
    print('1か2を入力してください。')