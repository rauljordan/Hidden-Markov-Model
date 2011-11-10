def convert_dataset( dataset):
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
