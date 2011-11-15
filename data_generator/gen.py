import random
import math

def gen_data_set(size= 30):
    labels = { straight: 0, left_turn: 1, right_turn: 2 }
    fs = [ left_turn, right_turn, straight ]
    unlabel_sequence = [ random.choice( fs ) for x in xrange( size) ]
    return [ [ f(), labels[f] ] for f in unlabel_sequence ]

def left_turn(label_data = False):
    data_vars = ['steering', 'speed']
    turn_label = 'left_turn' if label_data else None
    turn_seq = [ turn_data(t , data_vars, turn_label) for t in xrange(get_distance() ) ]

    #We are generating a right turn, adding a - to the value creates a left turn
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
    exp_value    = 70
    variance     = 20
    steering = lambda x:          math.e**(- ((x-exp_value)**2) / (2*variance**2 ))
    speed    = lambda x: 1- 0.9 * math.e**(- ((x-exp_value)**2) / (2*variance**2 ))
    norm     = random.normalvariate #Is used to add some variation to the data

    output_tuple = []
    for var in data_vars:
        if var == 'steering':
            output_tuple.append( max_steering * steering(t) + norm(0,1) )
        elif var == 'speed':
            output_tuple.append( max_speed * speed(t) + norm(0,1) )

    if turn_label:
        if abs( max_steering * steering(t) ) > 3:
            output_tuple.append( turn_label )
        else:
            output_tuple.append( 'straight' )

    rounding = lambda x: round( x , 2 )
    return map( rounding , output_tuple )

def straight_data(data_vars):
    output_tuple = []
    for var in data_vars:
        if var == 'steering':
            output_tuple.append( random.normalvariate(0, 3 ) )
        elif var == 'speed':
            output_tuple.append( random.normalvariate( 50, 2) )
    rounding = lambda x: round( x , 2 )
    return map( rounding, output_tuple )

def get_distance():
    return 15*10

