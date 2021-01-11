import tkinter as tk
import chirakari_hantei
import daily_check
import chirakari_shindan
import set_reminder
import datetime

def main_func():
    root = tk.Tk()
    root.title(u"HOME")
    root.geometry("600x400")

    today_reminded = False
    today = datetime.date.today()
    # date型を'20201201'みたいなstring型に変換
    today_str = today.strftime('%Y%m%d')

    with open('data/remind_date.txt', 'r') as f:
        for line in f:
            if line.rstrip('\n') == today_str:
                today_reminded = True

    if today_reminded:
        remind_label = tk.Label(text=u'**片付けリマインドが今日に設定されています。部屋を綺麗にしましょう。**')
        remind_label.pack()

    label = tk.Label(text=u'使用する機能を選んでください')
    label.pack()

    # clickイベント
    def chirakari_hantei_button_click():
        root.destroy()
        chirakari_hantei.chirakari_hantei()

    def daily_check_button_click():
        root.destroy()
        daily_check.daily_check()

    def chirakari_shindan_button_click():
        root.destroy()
        chirakari_shindan.chirakari_shindan()

    def set_reminder_button_click():
        root.destroy()
        set_reminder.set_reminder()

    # ボタン
    chirakariHanteiButton = tk.Button(root, text='散らかり判定', command=chirakari_hantei_button_click)
    chirakariHanteiButton.pack()
    dailyCheckButton = tk.Button(root, text='ゴミ捨てチェック', command=daily_check_button_click)
    dailyCheckButton.pack()
    chirakariShindanButton = tk.Button(root, text='タイプ別判定', command=chirakari_shindan_button_click)
    chirakariShindanButton.pack()
    setReminderButton = tk.Button(root, text='リマインダーを設定', command=set_reminder_button_click)
    setReminderButton.pack()

    root.mainloop()

if __name__ == '__main__':
  main_func()