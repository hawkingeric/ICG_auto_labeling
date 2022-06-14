import tkinter as tk
import math

#整個應用程式流程如下
#1. 提供輸入框，讓使用者輸入身高，體重
#2. 點擊按鈕，馬上計算BMI
#3. 將結果顯示在畫面上

#設定視窗標題，大小，顏色
window = tk.Tk()
window.title('身體質量指數計算器')
window.geometry('800x600')
window.configure(background='white')

#加入元件
#1.標題顯示 "BMI計算器" 的文字區塊
#2. 身高體重輸入區塊
#3. 顯示結果和點擊按鈕
header_label = tk.Label(window, text='BMI計算器')
header_label.pack()

#以下為height_frame群組
height_frame = tk.Frame(window)
height_frame.pack(side=tk.TOP)
height_label = tk.Label(height_frame, text='身高 (m)')
height_label.pack(side=tk.LEFT)
height_entry = tk.Entry(height_frame)
height_entry.pack(side=tk.LEFT)

#以下為weight_frame群組
weight_frame = tk.Frame(window)
weight_frame.pack(side=tk.TOP)
weight_label = tk.Label(weight_frame, text='體重 (m)')
weight_label.pack(side=tk.LEFT)
weight_entry = tk.Entry(weight_frame)
weight_entry.pack(side=tk.LEFT)

result_label = tk.Label(window)
result_label.pack()

def calculate_bmi_number():
	height = float(height_entry.get())
	weight = float(weight_entry.get())
	bmi_value = round(weight/math.pow(height, 2), 2)
	result = "你的BMI指數為:{}{}".format(bmi_value, get_bmi_status_description(bmi_value))
	result_label.configure(text=result)

def get_bmi_status_description(bmi_value):
	if bmi_value < 18.5:
		return "體重過輕囉，多吃點吧!"
	if bmi_value >= 18.5 and bmi_value < 24:
		return "體重剛剛好，繼續保持!"
	if bmi_value >= 24:
		return "體重有點過重囉，少吃多運動!"
	


#透過command參數可以將calculate_bmi_number事件處理函式綁定在元件上
calculate_btn = tk.Button(window, text='馬上計算', command=calculate_bmi_number)
calculate_btn.pack()
#運行主程式
window.mainloop()

