
'''
    Parameters to Initialise the Motors
        1. Motor Number [0-5] : 
            -Supports 5 stepper motors in parallel. 
            -Each motor is configured according to the suitable application required.
        2. Motor Irms current [milliampere] : 
            -Fine tune the stepper motor in the range of [0-4000] 
        3. Rsense : 
            -Rsense is the sense resistors which provides a fine tuning of motor current to suit the requirenents. 
            -In the current application a constant value of 0.05 is set
            -Ref : TMC5160/TMC5160A DATASHEET (Rev. 1.14 / 2020-MAY-19), Selecting Sense Resistors, Pg : 74 
        4. Velocity Profile : 
            -The velocity profile is configured using 6 point S curve, 
            -Detailed configuration : TMC5160/TMC5160A DATASHEET (Rev. 1.14 / 2020-MAY-19), Motion Profiles, Pg : 82
        5. Homing Velocity profile :
            -The velocity profile is suited to follow trapazoidal ramp with decrease in velocity to minimise the stopping inertia
        6. Steps caliberation : Each motor is configured in terms to mm as per the required application
'''

motor_1= 0 #Vertical Motor
motor_2= 1 #Horizontal Motor
motor_3= 2 #rotor 

motor_4 = 3 #buttom_spacing
motor_5 = 4 #left_plunger
motor_6 = 5 #right_plunger

motor_1_irms = 2000
motor_2_irms = 2000
motor_3_irms = 1000

motor_4_irms = 1500
motor_5_irms = 400
motor_6_irms = 400

rsense = 0.05

motor_1_vstart = 1
motor_1_a1 = 3500
motor_1_v1 = 50000
motor_1_amax = 10000
motor_1_vmax = 100000 
motor_1_dmax = 5000
motor_1_d1 = 2000
motor_1_vstop = 10
#-----------------------HORIZONTAL

motor_2_vstart = 1
motor_2_a1 = 3500
motor_2_v1 = 50000
motor_2_amax = 10000
motor_2_vmax = 100000
motor_2_dmax = 5000
motor_2_d1 = 2000
motor_2_vstop = 10

motor_3_vstart = 1
motor_3_a1 = 5000
motor_3_v1 = 10000
motor_3_amax = 10000
motor_3_vmax = 200000
motor_3_dmax = 10000
motor_3_d1 = 14000
motor_3_vstop = 10



motor_4_vstart = 1
motor_4_a1 = 5000
motor_4_v1 = 10000
motor_4_amax = 10000
motor_4_vmax = 200000
motor_4_dmax = 100000
motor_4_d1 =  14000
motor_4_vstop = 10


motor_5_vstart = 1
motor_5_a1 = 20000
motor_5_v1 = 20000
motor_5_amax = 100000
motor_5_vmax = 1000000
motor_5_dmax = 100000
motor_5_d1 = 14000
motor_5_vstop = 10
motor_5_microstep = 120

motor_6_vstart = 1
motor_6_a1 = 20000
motor_6_v1 = 20000
motor_6_amax = 100000
motor_6_vmax = 1000000
motor_6_dmax = 100000
motor_6_d1 = 14000
motor_6_vstop = 10
motor_6_microstep = 120

#-----HOMING VELOCITY---



motor_1_vstart_homing = 1
motor_1_a1_homing = 3500
motor_1_v1_homing = 5000
motor_1_amax_homing = 10000
motor_1_vmax_homing = 10000 
motor_1_dmax_homing = 5000
motor_1_d1_homing = 2000
motor_1_vstop_homing = 10

motor_2_vstart_homing = 1
motor_2_a1_homing = 3500
motor_2_v1_homing = 5000
motor_2_amax_homing = 10000
motor_2_vmax_homing = 10000
motor_2_dmax_homing = 5000
motor_2_d1_homing = 2000
motor_2_vstop_homing = 10

motor_3_vstart_homing = 1
motor_3_a1_homing = 1500
motor_3_v1_homing = 5000
motor_3_amax_homing = 1000
motor_3_vmax_homing = 20000
motor_3_dmax_homing = 3000
motor_3_d1_homing = 1500
motor_3_vstop_homing = 10



motor_4_vstart_homing = 1
motor_4_a1_homing = 5000
motor_4_v1_homing = 50000
motor_4_amax_homing = 10000
motor_4_vmax_homing = 30000
motor_4_dmax_homing = 3000
motor_4_d1_homing =  1500
motor_4_vstop_homing = 10


motor_5_vstart_homing = 1
motor_5_a1_homing = 3500
motor_5_v1_homing = 50000
motor_5_amax_homing = 10000
motor_5_vmax_homing = 150000
motor_5_dmax_homing = 10000
motor_5_d1_homing = 2000
motor_5_vstop_homing = 10
motor_5_microstep_homing = 120

motor_6_vstart_homing = 1
motor_6_a1_homing = 3500
motor_6_v1_homing = 50000
motor_6_amax_homing = 10000
motor_6_vmax_homing = 150000
motor_6_dmax_homing = 100000
motor_6_d1_homing = 2000
motor_6_vstop_homing = 10
motor_6_microstep_homing = 120



#------------------------




motor_1_real_min_lenght = 0
motor_1_real_max_lenght = 250
motor_1_steps_min  = 0
motor_1_steps_max = 221250

motor_2_real_min_lenght = 0
motor_2_real_max_lenght = 250
motor_2_steps_min  = 0
motor_2_steps_max = 221250

motor_3_real_min_lenght = 0
motor_3_real_max_lenght = 360
motor_3_steps_min  = 0
motor_3_steps_max = -153600

motor_4_real_min_lenght = 0
motor_4_real_max_lenght = 64
motor_4_steps_min  = 0
motor_4_steps_max =  494595

motor_5_real_min_lenght = 0
motor_5_real_max_lenght = 24
motor_5_steps_min  = 0
motor_5_steps_max = -500000

motor_6_real_min_lenght = 0
motor_6_real_max_lenght = 24
motor_6_steps_min  = 0
motor_6_steps_max = -500000
