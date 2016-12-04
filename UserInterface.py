import tkinter as tk
import QLearningRobot
import threading

CANVAS_WIDTH = 900
CANVAS_HEIGHT = 300
alpha, discount, epsilon = 0.5, 0.5, 0.5
crawler = QLearningRobot.QLearningRobot(alpha=alpha, discount=discount, epsilon=epsilon)
runningThread = None
thread_stop = False


def update_display():
    vec = crawler.get_all_positions_in_world_frame()
    # 清除现有图案
    cvs.delete(tk.ALL)
    # 直线AB
    cvs.create_line(vec[0][0], CANVAS_HEIGHT - vec[0][1], vec[1][0], CANVAS_HEIGHT - vec[1][1], fill='black')
    # 直线BC
    cvs.create_line(vec[1][0], CANVAS_HEIGHT - vec[1][1], vec[2][0], CANVAS_HEIGHT - vec[2][1], fill='black')
    # 直线CD
    cvs.create_line(vec[2][0], CANVAS_HEIGHT - vec[2][1], vec[3][0], CANVAS_HEIGHT - vec[3][1], fill='black')
    # 直线DA
    cvs.create_line(vec[3][0], CANVAS_HEIGHT - vec[3][1], vec[0][0], CANVAS_HEIGHT - vec[0][1], fill='black')
    # 直线CE
    cvs.create_line(vec[2][0], CANVAS_HEIGHT - vec[2][1], vec[4][0], CANVAS_HEIGHT - vec[4][1], fill='red')
    # 直线EP
    cvs.create_line(vec[4][0], CANVAS_HEIGHT - vec[4][1], vec[5][0], CANVAS_HEIGHT - vec[5][1], fill='green')
    cvs.update()


def onStartClickCallBack():
    global runningThread, thread_stop
    if start_button['text'] == '开始':
        start_button['text'] = '停止'
        update_display()

        def run():
            while not thread_stop:
                crawler.run_one_step()
                update_display()

        thread_stop = False
        runningThread = threading.Thread(target=run)
        runningThread.start()
    else:
        thread_stop = True
        start_button['text'] = '开始'


def onSaveClickCallBack():
    file = open("data.txt", 'w')
    file.write(str(crawler.q_value_table))
    pass


def onAppliedClickCallBack():
    global alpha
    global epsilon
    alpha = float(text_of_alpha.get())
    epsilon = float(text_of_epsilon.get())
    print(alpha, epsilon)
    crawler.alpha = alpha
    crawler.epsilon = epsilon
    text_of_alpha.set(alpha)
    text_of_epsilon.set(epsilon)



top = tk.Tk()
top.title("Crawler")

# 在窗口中创建标签
labelHello = tk.Label(top, text="--Crawler--")
labelHello.pack()
start_button = tk.Button(top, text="开始", command=onStartClickCallBack)
start_button.pack()

text_of_alpha = tk.StringVar()
text_of_alpha.set(alpha)
alpha_entry = tk.Entry(top, textvariable=text_of_alpha)
alpha_entry.pack()

text_of_epsilon = tk.StringVar()
text_of_epsilon.set(epsilon)
epsilon_entry = tk.Entry(top, textvariable=text_of_epsilon)
epsilon_entry.pack()

apply_button = tk.Button(top, text='应用', command=onAppliedClickCallBack)
apply_button.pack()

save_button = tk.Button(top, text='保存', command=onSaveClickCallBack)
save_button.pack()
cvs = tk.Canvas(top, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='#EEEEEE')
cvs.pack()
cvs.create_line(0, 10, CANVAS_WIDTH, 10, fill='black')
# 运行并显示窗口
top.mainloop()
