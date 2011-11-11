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
    return ['straight','left_turn', 'right_turn'][state_num]

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
    emit_p = [ [0.05, 0, 0, 0, 0, 0, 0, 0.05, 0, 0, 0, 0.9, 0, 0, 0,0,0,0,0,0,0],
               [0.45, 0, 0, 0, 0, 0, 0, 0.45, 0, 0, 0, 0.1, 0, 0, 0,0,0,0,0,0,0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.1, 0, 0.45, 0,0,0,0,0.45,0,0]]

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

##### Training the hmm #######
for x in gen_data_set(): 
    training_set = map(alphabet_to_hmm, vq.convert_dataset( x ) )
    ghmm_training_set = EmissionSequence( emit_domain, training_set)
    ghmm_training_set = hmm.sample(10,50)
    hmm.baumWelch( ghmm_training_set, nrSteps=1, loglikelihoodCutoff = 0.1 )
    print hmm

##### Classifying #####
left_turn = gen.left_turn()
for time_t in xrange(1, len(left_turn)):
    lower = time_t - 100 if time_t - 100 > 0 else 0

    obs_interval =  map( alphabet_to_hmm, vq.convert_dataset(left_turn[lower:time_t] ) )
    obs_sequence = EmissionSequence( emit_domain, obs_interval ) 
   # print obs_interval 
    state = hmm.viterbi( obs_sequence )
    print state_to_string( state[0][-1]) , left_turn[time_t]
        #print state_to_string( state ), left_turn[time_t]
