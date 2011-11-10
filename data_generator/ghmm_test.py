from ghmm import *
import random
import itertools
import gen
import vq

def gen_alphabet():
    perm = [ [ [x,y] for y in xrange(0,3) ]   for x in xrange( -3, 4) ]
    return list(itertools.chain(*perm) ) #return a flatten list

def alphabet_to_hmm( vector ):
    return gen_alphabet().index( vector )

def hmm_to_alphabet( idx ):
    return gen_alphabet()[idx]

def state_to_string( state_num ):
    return ['left_turn', 'right_turn'][state_num]

def gen_data_set():
    fs = [ gen.left_turn, gen.right_turn, gen.straight ]
    return [ random.choice( fs )() for x in xrange( 20 ) ]

#system_states = ['straight', 'left_turn', 'right_turn']
def create_hmm():
    emit_states = range( len(gen_alphabet()) )
    emit_domain = Alphabet( emit_states )

    trans_p = [ [0.9, 0.05 , 0.05],
                [ 0.1, 0.8 ,0.1],
                [ 0.1, 0.1, 0.8]]

    le = len(emit_states)
    emit_p = [ [1.0/le]*le,
               [1.0/le]*le,
               [1.0/le]*le]

    pi = [ 1, 0, 0 ]
    return HMMFromMatrices( emit_domain,
                            DiscreteDistribution(emit_domain),
                            trans_p,
                            emit_p,
                            pi
                            ),emit_domain
######################################################################

hmm, emit_domain = create_hmm()
print hmm
hmm.normalize()
for x in gen_data_set(): 
    training_set = map(alphabet_to_hmm, vq.convert_dataset( x ) )
    ghmm_training_set = EmissionSequence( emit_domain, training_set)
    hmm.baumWelch( ghmm_training_set, nrSteps=1 )
    print hmm
