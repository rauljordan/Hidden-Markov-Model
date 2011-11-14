import itertools

min_value_norm = -6
max_value_norm = 5
precision = 5.0

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
    perm = [ [ [x,y] for y in xrange(min_value_norm,max_value_norm) ]   for x in xrange( min_value_norm, max_value_norm) ]
    return list(itertools.chain(*perm) ) #return a flatten list

# [[0.432, 30.2] , [-0.1, 32,1] ] -> [[ 0, 1] , [ 0, 1]]
def convert_dataset_norm( dataset):
    return map( convert, dataset)

def convert( input_vector ):
    return map( squash, input_vector)

def squash(x):
    var = int( x/precision)
    if var >= max_value_norm :
        return max_value_norm -1 
    elif var <= min_value_norm:
        return min_value_norm
    else:
        return var
