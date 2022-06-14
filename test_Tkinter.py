import tkinter as tk

window = tk.Tk()
top_frame = tk.Frame(window)

top_frame.pack()
bottom_frame = tk.Frame(window)
bottom_frame.pack(side=tk.BOTTOM)

def echo_hello():
	print('hello world!')

def echo_red():
	print('red selected')

def echo_green():
	print('green selected')

def echo_blue():
	print('blue selected')


left_button = tk.Button(top_frame, text='RED', fg='red', command=echo_red)
left_button.pack(side=tk.LEFT) #---put the button on the left (default: up to down)

middle_button = tk.Button(top_frame, text='GREEN', fg='green', command=echo_green)
middle_button.pack(side=tk.LEFT)

right_button = tk.Button(top_frame, text='BLUE', fg='blue', command=echo_blue)
right_button.pack(side=tk.LEFT)

bottom_button = tk.Button(bottom_frame, text='BLACK', fg='Black', command=echo_hello)
bottom_button.pack(side=tk.BOTTOM)

window.mainloop()
