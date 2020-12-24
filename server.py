# -*- coding: utf-8 -*-

#Za GUI
from turtle import Turtle, Screen
#Za komunikaciju
from socket import socket, AF_INET, SOCK_STREAM
#Za multi-threading
from _thread import start_new_thread
#Za odgodu-vrijeme
from time import sleep

def primi_thread(c):
    while True:
        y = c.recv(500).decode('UTF-8')
        paddle_b.sety(int(y))

def salji_funkciju(y):
    msg = 'p:' + str(y)
    c.send(msg.encode('UTF-8'))    
    
def igra(c):
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
            
            info = "Igrač A: {}           Igrač B: {}".format(rez_a, rez_b)
            msg = 'm:' + info
            c.send(msg.encode('UTF-8'))     
            
            pen.clear()
            pen.write(info, align="center", font=("Arial", 15, "normal"))
    
        if ball.xcor() < -190:
            ball.goto(0, 0)
            ball.dx *= -1
            rez_b += 1
            
            info = "Igrač A: {}           Igrač B: {}".format(rez_a, rez_b)
            msg = 'm:' + info
            c.send(msg.encode('UTF-8'))     

            pen.clear()
            pen.write(info, align="center", font=("Arial", 15, "normal"))
    
        #Reket i loptica kolizija
        if ball.xcor() > 140 and ball.xcor() < 150 and ball.ycor() < paddle_b.ycor() + 40 and ball.ycor() > paddle_b.ycor() -40:
            ball.setx(140)
            ball.dx *= -1.2
    
        if ball.xcor() < -140 and ball.xcor() > -150 and ball.ycor() < paddle_a.ycor() + 40 and ball.ycor() > paddle_a.ycor() -40:
            ball.setx(-140)
            ball.dx /= -1.2

        msg = 'b:' + str(int(ball.xcor())) + ":" + str(int(ball.ycor()))
        print('Server Send Msg', msg)
        c.send(msg.encode('UTF-8'))     
        
    
def paddle_a_up():
    y = paddle_a.ycor()
    y += 20
    paddle_a.sety(y)
    salji_funkciju(y)

def paddle_a_down():
    y = paddle_a.ycor()
    y -= 20
    paddle_a.sety(y)
    salji_funkciju(y)

wind = Screen()
wind.title("Ping Pong: Server")
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

#Pen-napis
pen = Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 110)
pen.write("Igrač A: 0          Igrač B: 0", align="center", font=("Arial", 15, "normal"))

wind.listen()
wind.onkeypress(paddle_a_up, "w")
wind.onkeypress(paddle_a_down, "s")

#Kreiranje socketa
s=socket(AF_INET, SOCK_STREAM)
#IP servera
host = '127.0.0.1'
#Port
port = 7010
#Povezivanje IP i porta jedno s drugim
s.bind((host, port))
#Čekamo da se klijent poveže
s.listen(1)
print ("Uspostavljen poslužitelj...")

#Prihvaćen zahtjev za povezivanje od klijenta
#vraćamo broj sesije i IP / port klijenta
c, add=s.accept()
print ("Uspostavljena veza...")
#Nit za posluživanje sesije
start_new_thread(primi_thread,(c,))

start_new_thread(igra,(c,))
wind.mainloop()
