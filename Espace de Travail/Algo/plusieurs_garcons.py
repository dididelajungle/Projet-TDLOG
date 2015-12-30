# TDLOG - Projet
# Andréas Blondeau
# Déc 2015

import random
import copy
import unittest

 
guyprefers2 = {
    'alpha': ['C', 'A', 'B'],
    'beta': ['B', 'A', 'C'],
    'gamma': ['A', 'C', 'B'],
    'delta': ['A', 'B', 'C'],
}

galprefers2 = {
    'A': ['alpha', 'beta', 'gamma', 'delta'],
    'B': ['alpha', 'beta', 'gamma', 'delta'],
    'C': ['gamma', 'alpha', 'beta', 'delta'],
 }

capacity2 = {
    'A': 2,
    'B': 1,
    'C': 1,
}

guyprefers = {
 'abe':  ['abi', 'cath', 'bea'],
 'bob':  ['cath', 'abi', 'bea'],
 'col':  ['abi', 'bea', 'cath'],
 'dan':  ['bea', 'cath', 'abi'],
 'ed':   ['bea', 'cath', 'abi'],
 'fred': ['bea', 'abi', 'cath'],
 'gav':  ['bea', 'cath', 'abi'],
 'hal':  ['abi', 'cath', 'bea'],
 'ian':  ['cath', 'bea', 'abi'],
 'jon':  ['abi', 'bea', 'cath'],
 }

galprefers = {
 'abi':  ['bob', 'fred', 'jon', 'gav', 'ian', 'abe', 'dan', 'ed', 'col', 'hal'],
 'bea':  ['bob', 'abe', 'col', 'fred', 'gav', 'dan', 'ian', 'ed', 'jon', 'hal'],
 'cath': ['fred', 'bob', 'ed', 'gav', 'hal', 'col', 'ian', 'abe', 'dan', 'jon'],
 }

guys = sorted(guyprefers.keys())
gals = sorted(galprefers.keys())

capacity = {
    'abi':  4,
    'bea':  3,
    'cath': 1,
}




def inversedict(dico):
    inversedico = {}
    for she,they in dico.items():
        for he in they:
            inversedico[he] = she
    return inversedico
 
def check(engaged):
    inverseengaged = inversedict(engaged)
    for she, they in engaged.items():
        for he in they:
            shelikes = galprefers[she]
            shelikesbetter = shelikes[:shelikes.index(he)]
            helikes = guyprefers[he]
            helikesbetter = helikes[:helikes.index(she)]
            for guy in shelikesbetter:
                if guy not in engaged[she]:
                    guysgirl = inverseengaged[guy]
                    guylikes = guyprefers[guy]
                    if guylikes.index(guysgirl) > guylikes.index(she):
                        print("%s and %s like each other better than "
                              "their present partners: %s and %s, respectively"
                              % (she, guy, he, guysgirl))
                        return False
        for gal in helikesbetter:
            gallikes = galprefers[gal]
            girlsthey = engaged[gal]
            for girlsguy in girlsthey:
                if gallikes.index(girlsguy) > gallikes.index(he):
                    print("%s and %s like each other better than "
                          "their present partners: %s and %s, respectively"
                          % (he, gal, she, girlsguy))
                    return False
    return True

def orderlist(she, fiances):
    """ordonne la liste des fiances dans l'ordre de preference"""
    liste = []
    for guy in galprefers[she]:
        if guy in fiances:
            liste.append(guy)
    return liste

def matchmaker():
    guysfree = guys[:]
    engaged  = dict((she,[]) for she in gals)
    guyprefers2 = copy.deepcopy(guyprefers)
    galprefers2 = copy.deepcopy(galprefers)
    while guysfree:
        guy = guysfree.pop(0)
        guyslist = guyprefers2[guy]
        gal = guyslist.pop(0)
        fiances = engaged.get(gal)
        if len(fiances) < capacity[gal]:
            # She still has places
            engaged[gal].append(guy)
            engaged[gal] = orderlist(gal, engaged[gal])
            print("  %s and %s" % (guy, gal))
        else:
            # The bounder proposes to an engaged lass!
            lastfiance = engaged[gal][-1]
            galslist = galprefers2[gal]
            if galslist.index(lastfiance) > galslist.index(guy):
                # She prefers new guy
                del engaged[gal][-1]
                    # Remove lastfiance
                engaged[gal].append(guy)
                engaged[gal] = orderlist(gal, engaged[gal])
                print("  %s dumped %s for %s" % (gal, lastfiance, guy))
                if guyprefers2[lastfiance]:
                    # Ex has more girls to try
                    guysfree.append(lastfiance)
            else:
                # She is faithful to old fiance
                if guyslist:
                    # Look again
                    guysfree.append(guy)
    return engaged

def displayCouples(engaged):     
    print('\nCouples:')
    for she,they in sorted(engaged.items()):
        print('  ' + ',\n  '.join('%s is engaged to %s' % (she,he)
                                  for he in they))
    print()


class TestDeCase(unittest.TestCase):
    """Test la fiabilite du match"""
    
    def test_1_check_stability(self):
        """Verifie que la stabilite du match"""
        self.assertTrue(check(engaged))
        print('Engagement stability check PASSED'
          if check(engaged) else 'Engagement stability check FAILED')
        print()

    def test_2_check_instability(self):
        """Verifie l'instabilite du match si l'on introduit volontairement une erreur"""
        engaged2 = copy.deepcopy(engaged)
        she1,she2 = random.sample(gals, 2)
        index1 = random.randint(0, len(engaged[she1])-1)
        index2 = random.randint(0, len(engaged[she2])-1)
        print('\n\nSwapping two fiances to introduce an error')
        engaged2[she1][index1], engaged2[she2][index2] = engaged2[she2][index2], engaged2[she1][index1]
        for gal in (she1,she2):
            for guy in engaged2[gal]:
                if guy not in engaged[gal]:
                    print('  %s is now engaged to %s' % (gal, guy))
        print()
        self.assertTrue(not check(engaged2))
        print('Engagement instability check PASSED'
              if not check(engaged2) else 'Engagement instability check FAILED')


###################################### MAIN ########################################
if __name__ == '__main__':
    print('\nEngagements:')
    engaged = matchmaker()
    displayCouples(engaged)
    unittest.main()



        
