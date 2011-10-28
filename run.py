#!/usr/bin/python2.7
import gen


if __name__ == "__main__":
    init_seq = {'six' : 0.6 , 'four' : 0.4 }
    a = { 'six' : { 'six': 0.6 , 'four' : 0.4  },
          'four': { 'six': 0.6 , 'four' : 0.4 } }

    b = { 'six' : { 1: 1.0/6 , 2: 1.0/6 , 3: 1.0/6 , 4: 1.0/6, 5: 1.0/6, 6: 1.0/6 },
          'four': { 1: 1.0/4 , 2: 1.0/4 , 3: 1.0/4 , 4: 1.0/4, 5: 0.0,   6: 0.0   }}

    g = gen.Generate(init_seq, a,b)
    obs = g.run(10, print_output=False)
    print obs
    path = gen.viterbi(obs,init_seq, a,b,print_output=False)
    print path
