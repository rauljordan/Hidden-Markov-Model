from ghmm import *
import itertools
import gen
import vq

def gen_alphabet():
    perm = [ [ [x,y] for y in xrange(0,3) ]   for x in xrange( -3, 3) ]
    return list(itertools.chain(*perm) )

def alphabet_to_hmm( vector ):
    return gen_alphabet().index( vector )


#system_states = ['straight', 'left_turn', 'right_turn']
def create_hmm():
    emit_states = range( len(gen_alphabet()) )
    sigma = Alphabet( emit_states )

    trans_p = [ [0.9, 0.05 , 0.05],
                [ 0.3, 0,69 ,0.01],
                [ 0.3, 0.01, 0.69]]
    le = len(emit_states)
    emit_p = [ [1.0/le]*le,
               [1.0/le]*le,
               [1.0/le]*le]
    pi = [ 0.95, 0.025, 0.025 ]
    return HMMFromMatrices( sigma, DiscreteDistribution(sigma), trans_p, emit_p, pi )

hmm = create_hmm()
training_straight = map(vq.convert, gen.left_turn() )
print training_straight



