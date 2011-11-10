from ghmm import *
import itertools
import gen
import vq

def gen_alphabet():
    perm = [ [ [x,y] for y in xrange(0,3) ]   for x in xrange( -3, 3) ]
    return list(itertools.chain(*perm) ) #return a flatten list

def alphabet_to_hmm( vector ):
    return gen_alphabet().index( vector )

def hmm_to_alphabet( idx ):
    return gen_alphabet[idx]

def state_to_string( state_num ):
    return ['straight', 'left_turn', 'right_turn'][state_num]

#system_states = ['straight', 'left_turn', 'right_turn']
def create_hmm():
    label_domain = ['straight', 'left_turn', 'right_turn']
    emit_states = range( len(gen_alphabet()) )
    emit_domain = Alphabet( emit_states )

    trans_p = [ [0.9, 0.05 , 0.05],
                [ 0.3, 0,69 ,0.01],
                [ 0.3, 0.01, 0.69]]

    le = len(emit_states)
    emit_p = [ [1.0/le]*le,
               [1.0/le]*le,
               [1.0/le]*le]

    pi = [ 0.95, 0.025, 0.025 ]
    return HMMFromMatrices( emit_domain,
                            DiscreteDistribution(emit_domain),
                            trans_p,
                            emit_p,
                            pi,
                            labelDomain=label_domain
                            ),emit_domain

hmm, emit_domain = create_hmm()

training_set = map(alphabet_to_hmm, vq.convert_dataset(gen.left_turn() ))
ghmm_training_set = EmissionSequence( emit_domain, training_set)

print emit_domain, training_set

hmm.baumWelch( ghmm_training_set )
print hmm
