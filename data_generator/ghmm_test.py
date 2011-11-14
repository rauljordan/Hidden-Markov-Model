from ghmm import *
import random
import itertools
import gen
import vq

def state_to_string( state_num ):
    return ['straight','left_turn', 'right_turn', 'weird output'][state_num]

def generate_emit_p():
    straight    = [ vq.dataset_to_alphabet(gen.straight())   for x in xrange(5) ]
    left_turns  = [ vq.dataset_to_alphabet(gen.left_turn())  for x in xrange(10) ]
    right_turns = [ vq.dataset_to_alphabet(gen.right_turn()) for x in xrange(10) ]
    data_sets = [ straight, left_turns, right_turns ]
    gen_data_set = { 0: {}, 1: {}, 2: {} }

    for idx, dataset in enumerate(data_sets):
        for sample in dataset: 
            for alpha in sample:
                if alpha not in gen_data_set[idx]:
                    gen_data_set[idx][alpha] = 1
                else:
                    gen_data_set[idx][alpha] += 1

    alpha_size = len(vq.gen_alphabet() )
    emit_p = [  [0.01 for x in xrange(alpha_size) ] for x in xrange(3) ]

    for idx, stats in gen_data_set.iteritems():
        for k,v in stats.iteritems():
            emit_p[idx][k] = v

    return normalize_emit_probabilites( emit_p )

def normalize_emit_probabilites( emit_p ):
    return [ [ round(y / sum(x), 3 ) for y in x  ]  for x in emit_p ]

def create_hmm():
    emit_states = range( len(vq.gen_alphabet()) )
    emit_domain = Alphabet( emit_states )

    trans_p = [ [0.9, 0.05 , 0.05],
                [ 0.1, 0.8 ,0.1],
                [ 0.1, 0.1, 0.8]]
    emit_p = generate_emit_p()
    pi = [ 0.9, 0.05, 0.05 ]

    return HMMFromMatrices( emit_domain,
                            DiscreteDistribution(emit_domain),
                            trans_p,
                            emit_p,
                            pi
                            ),emit_domain

def train_hmm(hmm, emit_domain):
    for x in xrange(100):
        ghmm_training_set = hmm.sample(100,500)
        hmm.baumWelch( ghmm_training_set )

    for x in gen.gen_data_set(0):
        training_set = vq.dataset_to_alphabet( x )
        ghmm_training_set = EmissionSequence( emit_domain, training_set)
        hmm.baumWelch( ghmm_training_set)

    return hmm

def classify(hmm):
    left_turn = gen.right_turn()

    for time_t in xrange(1, len(left_turn)):

        obs_interval = vq.dataset_to_alphabet( left_turn[:time_t] )
        obs_sequence = EmissionSequence( emit_domain, obs_interval ) 
        state = hmm.viterbi( obs_sequence )
#        print state
        print state_to_string( state[0][-1]) , left_turn[time_t]
######################################################################

if __name__ == '__main__' or True:
    print "Calculating emission and transition probabilities"
    hmm, emit_domain = create_hmm()
    print "HMM created"
    #print hmm
    hmm.normalize()

    ##### Training the hmm #######
    print "Training HMM, generating training data"
    hmm = train_hmm(hmm, emit_domain)

    ##### Classifying #####
    print "Classifying training data"
    classify(hmm)

