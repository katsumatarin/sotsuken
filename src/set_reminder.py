import main
import tkinter as tk

class SetReminderRunner():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('300x200')
        self.root.title('リマインダーを設定')

        # ラベル
        self.lbl = tk.Label(text='リマインダーを設定する日付を入力してください。\n例: 20210201')
        self.lbl.pack()

        # テキストボックス
        self.txt = tk.Entry(width=20)
        self.txt.pack()

        def set_reminder_btn_click():
            # テキスト取得
            date = int(self.txt.get())
            with open('./data/remind_date.txt', 'a') as f:
                print(date, file=f)
            self.root.destroy()

        # リマインダー設定ボタン
        self.set_reminder_btn = tk.Button(self.root, text='設定', command=set_reminder_btn_click)
        self.set_reminder_btn.pack()

        def return_btn_click():
            self.root.destroy()
            main.main_func()

        self.return_btn = tk.Button(self.root, text='メイン画面に戻る', command=return_btn_click)
        self.return_btn.pack()

    def run(self):
        # 画面をそのまま表示
        self.root.mainloop()
        return

def set_reminder():
    set_reminder_runner = SetReminderRunner()
    set_reminder_runner.run()

if __name__ == '__main__':
    chirakari_shindan()