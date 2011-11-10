import random
import math

def left_turn(label_data = False):
    data_vars = ['steering', 'speed']
    turn_label = 'left_turn' if label_data else None
    turn_seq = [ turn_data(t , data_vars, turn_label) for t in xrange(get_distance() ) ]

    flip = lambda s: [-s[0]] + s[1:]
    return map( flip , turn_seq )

def right_turn(label_data = False):
    data_vars = ['steering', 'speed']
    turn_label = 'right_turn' if label_data else None

    return [ turn_data(t , data_vars, turn_label) for t in xrange(get_distance() ) ]

def straight():
    distance = get_distance()
    return [ straight_data(['steering', 'speed'] ) for x in xrange(distance) ]

def turn_data(t, data_vars, turn_label):
    max_steering = 70
    max_speed    = 50
    steering = lambda x:          math.e**(- ((x-50)**2) / (2*20**2 ))
    speed    = lambda x: 1- 0.9 * math.e**(- ((x-50)**2) / (2*20**2 ))
    norm     = random.normalvariate

    output_tuple = []
    for var in data_vars:
        if var == 'steering':
            output_tuple.append( max_steering * steering(t) + norm(0,1) )
        elif var == 'speed':
            output_tuple.append( max_speed * speed(t) + norm(0,1) )
    if turn_label:
        if abs( max_steering * steering(t) + norm(0,1)) > 3:
            output_tuple.append( turn_label )
        else:
            output_tuple.append( 'straight' )

    return output_tuple

def straight_data(data_vars):
    output_tuple = []
    for var in data_vars:
        if var == 'steering':
            output_tuple.append( random.normalvariate(0, 3 ) )
        elif var == 'speed':
            output_tuple.append( random.normalvariate( 50, 2) )
    return output_tuple

def get_distance():
    return random.normalvariate( 15*10 , 5*10 ).__int__()

