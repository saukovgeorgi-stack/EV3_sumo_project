#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.parameters import Port, Stop
from pybricks.tools import wait

# инициализация
ev3 = EV3Brick()

motor_r = Motor(Port.B)
motor_l = Motor(Port.C)

us_front = UltrasonicSensor(Port.S3)
us_left  = UltrasonicSensor(Port.S2)
us_right = UltrasonicSensor(Port.S4)

# константы
MAX_POWER = 100        
SEARCH_POWER = 70       
DETECT_DIST_F = 400     #60 см
DETECT_DIST_SIDE = 300  #450
DOVOROT_MOTOR_DEG = 100 

# Флаги состояния
first_encounter = True
last_turn_dir = 0  # 1 крутились вправо, -1 крутились влево, 0 стоим ровно

wait(450)

while True:
    dist_f = us_front.distance()
    dist_l = us_left.distance()
    dist_r = us_right.distance()

    #1 противник по центру
    if dist_f < DETECT_DIST_F:
        if first_encounter:
            motor_l.hold()
            motor_r.hold()
            wait(50)
            # Если нас несло вправо, доворачиваем чуть влево, и наоборот
            if last_turn_dir == 1:
                # Доворот влево
                motor_l.run_angle(1300, DOVOROT_MOTOR_DEG, wait=False)
                motor_r.run_angle(1300, -DOVOROT_MOTOR_DEG, wait=True)
            elif last_turn_dir == -1:
                # Доворот вправо
                motor_l.run_angle(1300, -DOVOROT_MOTOR_DEG, wait=False)
                motor_r.run_angle(1300, DOVOROT_MOTOR_DEG, wait=True)
            
            first_encounter = False

        #атака
        motor_l.dc(MAX_POWER)
        motor_r.dc(MAX_POWER)

    #2 противник слева
    elif dist_l < DETECT_DIST_SIDE:
        last_turn_dir = -1
        motor_l.dc(-MAX_POWER)
        motor_r.dc(MAX_POWER)

    #3 противник справа
    elif dist_r < DETECT_DIST_SIDE:
        last_turn_dir = 1
        motor_l.dc(MAX_POWER)
        motor_r.dc(-MAX_POWER)

    #4 поиск
    else:
        if last_turn_dir == -1:
            motor_l.dc(-SEARCH_POWER)
            motor_r.dc(SEARCH_POWER)
        else:
            last_turn_dir = 1
            motor_l.dc(SEARCH_POWER)
            motor_r.dc(-SEARCH_POWER)