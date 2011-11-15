from ghmm import *
import random
import itertools
import gen
import vq

#Converts ghmms inner state representation to a human readable output
def state_to_string( state_num ):
    return ['straight','\033[1;32mleft_turn\033[0m', '\033[1;32mright_turn\033[0m', '\033[1;31mweird output\033[0m'][state_num]

def generate_emit_p():
    straight    = [ vq.dataset_to_alphabet(gen.straight())   for x in xrange(50) ]
    left_turns  = [ vq.dataset_to_alphabet(gen.left_turn())  for x in xrange(100) ]
    right_turns = [ vq.dataset_to_alphabet(gen.right_turn()) for x in xrange(100) ]
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

    for x, label in gen.gen_data_set(size_generated_training_set):
        training_set = vq.dataset_to_alphabet( x )
        ghmm_training_set = EmissionSequence( emit_domain, training_set)
        ghmm_training_set.setSeqLabel(label)
        hmm.baumWelch( ghmm_training_set,loglikelihoodCutoff=0.000001, nrSteps = 10)

    for x in xrange(size_sampled_training_set):
        ghmm_training_set = hmm.sample(100,500)
        hmm.baumWelch( ghmm_training_set )
    return hmm

def classify(hmm):
    unclassified_data = gen.right_turn() + gen.left_turn()

    for time_t in xrange(1, len(unclassified_data)):
        obs_interval = vq.dataset_to_alphabet(unclassified_data[:time_t][-observation_size:] )
        obs_sequence = EmissionSequence( emit_domain, obs_interval ) 
        state = hmm.viterbi( obs_sequence )
#        print state
        print state_to_string( state[0][-1]) , unclassified_data[time_t] , state[1]
######################################################################

if __name__ == '__main__' or True:

    # 10 is one sec, 100 is 10sec
    observation_size = 40
    size_sampled_training_set = 50
    size_generated_training_set = 0

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
    print hmm

