import random
import pprint
class Hmm:
    def __init__( self, init_vec, trans_p, emit_p):
        self.trans_p          =trans_p
        self.emit_p          = emit_p
        self.init_vec   = init_vec
        self.result_log = []
        self.state_log  = []

    def generate( self, iterations ):
        state = self.roulette( self.init_vec )
        result = self.roulette( self.emit_p[state] )
        self.log_result( result )

        for x in xrange( iterations - 1 ):
            state = self.roulette( self.trans_p[state] )
            result = self.roulette( self.emit_p[state] )
            self.log_result (result)

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

    def log_result( self, result ):
        self.result_log += [result]

    def viterbi( self, obs):
        states = self.init_vec.keys()
        v = [{}]

        for s in states:
            v[0][s] = self.emit_p[s][ obs[0] ] * self.init_vec[s]

        for t in xrange(1, len(obs) ):
            v.append( {} )

            for s in states:
                (prob, state) = max(  [ (v[t-1][s_temp] * self.emit_p[s][obs[t]] * self.trans_p[s_temp][s], s_temp ) for s_temp in states ])
                v[t][s] = prob

        #Backtracking, using an unreadable nested list-comprehension
        opt_path = [ max([(prob,state)  for (state,prob) in x.iteritems() ])[1] for x in v  ]
        return prob, opt_path
