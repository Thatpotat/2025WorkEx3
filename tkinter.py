import tkinter as tk
import time

framerate = 60
frame_duration = 1 / framerate

window = tk.Tk()
window.geometry('1000x600')
window.title('Pong')

canvas_width = 1000
Canvas_height = 600

Canvas = tk.Canvas(window, width = canvas_width, height = Canvas_height, background = 'blue')
Canvas.pack()

class mallet():
    def __init__(self, x, y, radius, colour):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        
    def move(self, event):
        self.x = event.x
        self.y = event.y

    def draw(self):
        Canvas.create_oval((self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius), fill = self.colour)

player1 = mallet(50, 300, 20, 'red')

run = True
while run:
    start_time = time.time()
    Canvas = tk.Canvas(window, width = canvas_width, height = Canvas_height, background = 'blue')
    Canvas.place(x=0, y=0)
    window.bind("<Motion>", player1.move)
    player1.draw()
    window.update()
    print(player1.x)
    print(window.winfo_pointerx())
    end_time = time.time()
    elapsed_time = end_time - start_time
    sleep_duration = frame_duration - elapsed_time
    if sleep_duration > 0:
        time.sleep(sleep_duration)
