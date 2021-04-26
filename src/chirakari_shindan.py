import tkinter as tk
import main
import daily_check
import chirakari_hantei

class ChirakariShindanRunner():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(u"お片付け診断")
        self.root.geometry("600x400")
        self.question_counter = 0
        self.yes_counter = 0
        self.question_list = ['①ふだん使う物が手の届くところにないと落ち着かない', '②店員さんに「お似合いですよ」と言われると買ってしまいがち', '③物を捨てた後、悲しくなることがある', '④街で配っているポケットティッシュなどのノベルティをついもらってしまう', '⑤隙間なくきれいに収まっている収納を見ると気持ちいい', '⑥そういえば３年以上開けていない箱がある', '⑦出かけるときにカギや携帯電話をよく忘れる', '⑧周りの人から「やさしいね」「いい人ね」と言われることが多い', '⑨おっちょこちょいで面倒くさがりな性格で、物をチョイ置きすることが多い', '⑩環境が変わることや新しい場所が苦手', 'お疲れ様でした！\n質問は以上です。']
        self.question_box = tk.Label(text=self.question_list[self.question_counter])
        self.yes_button = tk.Button(text="yes")
        self.no_button = tk.Button(text="no")
        self.result_button = tk.Button(text="result")
        self.recommend_button = tk.Button(text="おすすめの機能")

    def run(self):
        def yes_clicked():
            self.yes_counter += 1
            self.question_counter += 1
            self.question_box.config(text=self.question_list[self.question_counter])
            if self.question_counter == 10:
                self.result_button.pack()
                self.yes_button.destroy()
                self.no_button.destroy()

        def no_clicked():
            self.question_counter += 1
            self.question_box.config(text=self.question_list[self.question_counter])
            if self.question_counter == 10:
                self.result_button.pack()
                self.yes_button.destroy()
                self.no_button.destroy()

        def result_clicked():
            self.result_button.destroy()
            self.recommend_button.pack()
            if self.yes_counter < 3:
                self.question_box.config(text="お片付けレベル★★★\nすでにお片付け体質！\n\nあなたへのおすすめ：今日はのんびり休もう\n\n")
                self.recommend_button.config(text="HOME画面に戻る", command=to_mode_1_clicked)
            elif self.yes_counter < 7:
                self.question_box.config(text="お片付けレベル★★☆\nやる気先行タイプ\n\nあなたへのおすすめ：毎日継続的に片付けよう\n\n")
                self.recommend_button.config(text="毎日ゴミ捨てチェックモードに進む", command=to_mode_2_clicked)
            elif self.yes_counter < 11:
                self.question_box.config(text="お片付けレベル★☆☆\n気合を入れて頑張ろう！\n\nあなたへのおすすめ：今すぐに散らかり度をチェックしよう\n\n")
                self.recommend_button.config(text="散らかり判定モードに進む", command=to_mode_3_clicked)


        def to_mode_1_clicked():
            self.root.destroy()
            main.main_func()

        def to_mode_2_clicked():
            self.root.destroy()
            daily_check.daily_check()

        def to_mode_3_clicked():
            self.root.destroy()
            chirakari_hantei.chirakari_hantei()

        self.yes_button.config(command=yes_clicked)
        self.no_button.config(command=no_clicked)
        self.result_button.config(command=result_clicked)

        self.question_box.pack()
        self.yes_button.pack()
        self.no_button.pack()

        self.question_box.mainloop()
        self.yes_button.mainloop()
        self.no_button.mainloop()
        self.result_button.mainloop()

def chirakari_shindan():
    chirakari_shindan_runner = ChirakariShindanRunner()
    chirakari_shindan_runner.run()

if __name__ == '__main__':
    chirakari_shindan()