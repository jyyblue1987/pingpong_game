  
# -*- coding: utf-8 -*-

#Za GUI
from turtle import Turtle, Screen
#Za komunikaciju
from socket import socket, AF_INET, SOCK_STREAM
#Za multi-threading
from _thread import start_new_thread
#Za odgodu-vrijeme
from time import sleep

def primi_thread(s):
    while True:
        try:
            msg = s.recv(500).decode('UTF-8')
            print('Server Msg', msg)
            lst1 = msg.split(":")
            if lst1[0] == 'p':
                paddle_a.sety(int(lst1[1]))

            if lst1[0] == 'b':                   
                wind.update()     
                x = int(lst1[1])
                y = int(lst1[2])
                
                ball.setx(x)
                ball.sety(y)
            if lst1[0] == 'r':                
                rez_a = int(lst1[1])
                rez_b = int(lst1[2])

                info = "Igrač A: {}           Igrač B: {}".format(rez_a, rez_b)

                pen.clear()
                pen.write(info, align="center", font=("Arial", 15, "normal"))
        except:
            print("Data Error", msg)

                
def salji_funkcija(y):
    x = str(y)
    s.send(x.encode('UTF-8'))

def paddle_b_up():
    y = paddle_b.ycor()
    y += 20
    paddle_b.sety(y)
    salji_funkcija(y)

def paddle_b_down():
    y = paddle_b.ycor()
    y -= 20
    paddle_b.sety(y)
    salji_funkcija(y)

wind = Screen()
wind.title("Ping-pong: Klijent")
wind.bgcolor("#222222")
wind.setup(width=450, height=350)
wind.tracer(0)

#Reket A
paddle_a = Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("blue")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-150, 0)

#Reket B
paddle_b = Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("red")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(150, 0)

#Loptica
ball = Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 1
ball.dy = -1

#Pen
pen = Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 110)
pen.write("Igrač A: 0          Igrač B: 0", align="center", font=("Arial", 15, "normal"))

wind.listen()
wind.onkeypress(paddle_b_up, "Up")
wind.onkeypress(paddle_b_down, "Down")

s=socket(AF_INET, SOCK_STREAM)
s.connect(('127.0.0.1',7010))
#nit za posluživanje sesije
start_new_thread(primi_thread,(s,))
wind.mainloop()
