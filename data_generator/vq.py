import itertools

#converts a whole dataset from continues input to ghmm alphabet
def dataset_to_alphabet( dataset ):
    dataset_norm = convert_dataset_norm( dataset )
    return [ data_to_alphabet(d)  for d in dataset_norm ]

# converts a normalized vector to alphabet
def data_to_alphabet( data_vector ):
    return gen_alphabet().index(data_vector)

# converts a alphabet symbol to a normalized vector
def alphabet_to_data( hmm_alphabet_char ):
    return gen_alphabet()[ hmm_alphabet_char]

# generates alphabet to vector mapping
def gen_alphabet():
    perm = [ [ [x,y] for y in xrange(0,3) ]   for x in xrange( -3, 4) ]
    return list(itertools.chain(*perm) ) #return a flatten list

# [[0.432, 30.2] , [-0.1, 32,1] ] -> [[ 0, 1] , [ 0, 1]]
def convert_dataset_norm( dataset):
    return map( convert, dataset)

def convert( input_vector ):
    return map( squash, input_vector)

def squash(x):
    var = int( x/20.0 )
    if var >= 3:
        return 3
    elif var <= -3:
        return -3
    else:
        return var
