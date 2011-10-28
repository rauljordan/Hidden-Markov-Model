import unittest
import random
import gen

class HmmTest( unittest.TestCase ):

    def setUp(self):
        self.init_seq = {'six' : 0.6 , 'four' : 0.4 }

        self.a = { 'six' : { 'six': 0.6 , 'four' : 0.4  },
                   'four': { 'six': 0.6 , 'four' : 0.4 } }

        self.b = { 'six' : { 1: 1.0/6 , 2: 1.0/6 , 3: 1.0/6 , 4: 1.0/6, 5: 1.0/6, 6: 1.0/6 },
                   'four': { 1: 1.0/4 , 2: 1.0/4 , 3: 1.0/4 , 4: 1.0/4, 5: 0.0,   6: 0.0   }}

        self.g = gen.Generate( self.init_seq, self.a, self.b )


    def test_roulette( self ):
        stats = { 'six' : 0 , 'four' : 0 }

        for x in xrange(1000):
            result = self.g.roulette( self.init_seq )
            stats[result] += 1

        self.assertTrue( stats['six']  > stats['four'] )
        self.assertTrue( stats['six']  > 0 )
        self.assertTrue( stats['four'] > 0 )

    def test_main_function( self ):
        seq_length = 10
        result_seq = self.g.run( seq_length )
        self.assertTrue( len(result_seq) == seq_length )

    def test_viterbi_function( self ):
        obs = self.g.run( 10 )
        obs = [6, 6]
        prob, sys_states = gen.viterbi(obs,self.init_seq, self.a,self.b,print_output=False)
        self.assertTrue( sys_states == ['six','six'] )

if __name__ == '__main__':
    unittest.main()
