import ghmm
import itertools
import random

class Dataset:
    def __init__(self, source, precision, signals, time_length = 20):
        self.SOURCE         = source
        self.SIGNALS        = signals
        self.PRECISION      = precision
        self.TIME_LENGTH    = time_length * 10 #input is given in seconds, we want to sample 10 values per second, like euroFoT
        self.ALPHABET       = self.__generate_alphabet()
        self.__setup_generation_params()

    def __setup_generation_params():
        self.MAX_SPEED    = 50
        self.MAX_STEERING = 70

        self.NOISE_EXP    = 0
        self.NOISE_VAR    = 2

        self.TURN_EXP     = 70
        self.TURN_VAR     = 20

        self.SPEED_EXP    = 70
        self.SPEED_VAR    = 20

    def __generate_alphabet(self):
        iterator = itertools.product(range(-self.PRECISION, self.PRECISION+1) , repeat=len(signals) )
        return [ x for x in iter(iterator) ]

    def get_dataset(self,num_samples raw=False):
        self.RAW = raw
        if self.SOURCE == 'fot':
            print "FoT is not supported"
            return None
        else:
            return self.__generate_data(num_samples)

    def __generate_data(self, num_samples):
        actions = [self.__left_turn, self.__right_turn, self.__straight]
        return [ random.choice(actions)(t) for t in xrange(num_samples) ]

    def __left_turn(self,time):

    def __right_turn(self):

    def __straight(self):

    def __turn_data(self,time):
        steering = lambda x:          math.e**(- ((x-exp_value)**2) / (2*variance**2 ))
        speed    = lambda x: 1- 0.9 * math.e**(- ((x-exp_value)**2) / (2*variance**2 ))
        norm     = random.normalvariate #Is used to add some variation to the data
        time_vector = []
        for signal in self.signals:
            if signal == 'steering':
                time_length.append( steering(time) + norm(self.NOISE_EXP,self.NOISE_VAR)
            elif signal == 'speed':
                time_length.append( speed(time)    + norm(self.NOISE_EXP,self.NOISE_VAR)

