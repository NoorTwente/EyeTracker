import turtle
import time
import sys
t = turtle.Turtle()
class app():
    def draw_rectangle(length, height):
        for i in range(0,4):
            if i % 2 == 0: 
                t.forward(length)
                t.right(90)
            else: 
                t.forward(height)
                t.right(90)

app.draw_rectangle(100, 200)
sys.exit(app.exec_())