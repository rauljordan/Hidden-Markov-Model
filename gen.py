import random
import pprint
class Generate:
    def __init__( self, init_vec, a, b ):
        self.a          = a
        self.b          = b
        self.init_vec   = init_vec
        self.result_log = []
        self.state_log  = []

    def run( self, iterations, print_output=False):
        state = self.roulette( self.init_vec )
        self.log_state( state )
        result = self.roulette( self.b[state] )
        self.log_result( result )

        for x in xrange( iterations - 1 ):
            state = self.roulette( self.a[state] )
            result = self.roulette( self.b[state] )
            self.log_result (result)
            self.log_state (state)

        if print_output:
            self.print_log()

        return self.result_log

    """ Roulette wheel selection """
    def roulette( self, vector ):
        rand_value = random.random()
        prob_sum = 0
        for state, prob in vector.iteritems():
            prob_sum += prob
            if rand_value <= prob_sum:
                return state
        raise Exception( 'roulette wheel selection failed' ) 

    def log_state( self, state ):
        self.state_log += [state] 

    def log_result( self, result ):
        self.result_log += [result]

    def print_log( self):
        print "state_log:  ", self.state_log
        print "result_log: ", self.result_log


def viterbi( obs, start_p, trans_p, emit_p, print_output=False):
    states = start_p.keys()
    v = [{}]

    for s in states:
        v[0][s] = emit_p[s][ obs[0] ] * start_p[s]

    for t in xrange(1, len(obs) ):
        v.append( {} )

        for s in states:
            (prob, state) = max(  [ (v[t-1][s_temp] * emit_p[s][obs[t]] * trans_p[s_temp][s], s_temp ) for s_temp in states ])
            v[t][s] = prob

    if print_output:
        pp = pprint.PrettyPrinter( indent = 4 )
        pp.pprint( v )

    #Backtracking, using an unreadable nested list-comprehension
    opt_path = [ max([(prob,state)  for (state,prob) in x.iteritems() ])[1] for x in v  ]
    return prob, opt_path
