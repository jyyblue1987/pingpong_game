  
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
            if lst1[0] == 'm':                
                pen.clear()
                pen.write(msg[2:], align="center", font=("Arial", 15, "normal"))
        except:
            print("Data Error", msg)

                
def salji_funkcija(y):
    x = str(y)
    s.send(x.encode('UTF-8'))

def igra(s):
    #Rezultat
    rez_a = 0
    rez_b = 0
    
    #Čekanje 10 sekundi
    sleep(10)
    #Glavni dio igre
    while True:
        wind.update()
        
        #Pomicanje loptice
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)
    
    
    	#Provjera granica
        if ball.ycor() > 140:
            ball.sety(140)
            ball.dy *= -1
    
        if ball.ycor() < -140:
            ball.sety(-140)
            ball.dy *= -1
    
        if ball.xcor() > 190:
            ball.goto(0, 0)
            ball.dx *= -1
            rez_a += 1
            pen.clear()
            pen.write("Igrač A: {}          Igrač B: {}".format(rez_a, rez_b), align="center", font=("Arial", 15, "normal"))
    
        if ball.xcor() < -190:
            ball.goto(0, 0)
            ball.dx *= -1
            rez_b += 1
            pen.clear()
            pen.write("Igrač A: {}          Igrač B: {}".format(rez_a, rez_b), align="center", font=("Arial", 15, "normal"))
    
        #Reket i loptica kolizija
        if ball.xcor() > 140 and ball.xcor() < 150 and ball.ycor() < paddle_b.ycor() + 40 and ball.ycor() > paddle_b.ycor() -40:
            ball.setx(140)
            ball.dx *= -1.2
    
        if ball.xcor() < -140 and ball.xcor() > -150 and ball.ycor() < paddle_a.ycor() + 40 and ball.ycor() > paddle_a.ycor() -40:
            ball.setx(-140)
            ball.dx /= -1.2
                

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
# start_new_thread(igra,(s,))
wind.mainloop()
