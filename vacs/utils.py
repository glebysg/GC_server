from itertools import combinations
import re

class Order:
    ########################
    #from order import Order
    ##names_list = ['A','B','C','D', 'E'] # Names of files
    ##relations = ["E<C=B", "E<C<A", "E<C<D", "E<B<A", "E<B<D", "E<A<D"]
    #ord = Order(names_list, relations)
    #[order, ineq, scores] = ord.get_all()
    #order = ord.get_order()
    #ineq = ord.get_ineq()
    #scores = ord.get_scores()
    #print ord.glob_order
    #print ord.glob_ineq
    #print ord.glob_scores
    ########################

    names_list = [] #['A','B','C','D', 'E'] # Names of files
    relations = [] #["E<C=B", "E<C<A", "E<C<D", "E<B<A", "E<B<D", "E<A<D"] # Full list of comparisons
    combos = [] # All possible 2-combinations of names_list
    glob_order = [] # Final order of files
    glob_ineq = [] # Final inequalities in the final order
    glob_scores = [] # Scores attached to each file at the end

    def __init__(self, names_list, relations):
        self.names_list = names_list
        self.relations = relations
        self.combos = list(combinations(names_list, 2))
        self.combos = dict( zip(self.combos, ['' for i in range(len(self.combos))]))
        self.order()

    def comparator(self, x, y):
        if (x,y) in self.combos.keys():
            if self.combos[(x,y)] == '<':
                return -1
            elif self.combos[(x,y)] == '=':
                return 0
            elif self.combos[(x,y)] == '>':
                return 1
            else:
                print('Error in comparator - 1')
        elif (y,x) in self.combos.keys():
            if self.combos[(y,x)] == '<':
                return 1
            elif self.combos[(y,x)] == '=':
                return 0
            elif self.combos[(y,x)] == '>':
                return -1
            else:
                print('Error in comparator - 2')
        else:
            print (x,y)
            print('Error in comparator - 3')

    def get_all(self):
        return [self.glob_order, self.glob_ineq, self.glob_scores]

    def get_order(self):
        return self.glob_order

    def get_ineq(self):
        return self.glob_ineq

    def get_scores(self):
        return self.glob_scores


    def order(self):
        for rel in self.relations:
            rel = rel.replace(' ', '')
            rel_parts = re.split('<|=', rel)
            ineq = [rel[rel.index(rel_parts[1])-1], rel[rel.index(rel_parts[2])-1]]
            if ineq[0] == '<' or ineq[1] == '<':
                ineq.insert(1,'<')
            else:
                ineq.insert(1,'=')

            temp = list(combinations(rel_parts, 2))
            for ww in range(len(temp)):
                if temp[ww] in self.combos.keys():
                    self.combos[temp[ww]] = ''.join([self.combos[temp[ww]], ineq[ww]])
                elif (temp[ww][1],temp[ww][0]) in self.combos.keys():
                    if ineq[ww] == '=':
                        self.combos[(temp[ww][1],temp[ww][0])] = ''.join([self.combos[(temp[ww][1],temp[ww][0])], '='])
                    else:
                        self.combos[(temp[ww][1],temp[ww][0])] = ''.join([self.combos[(temp[ww][1],temp[ww][0])], '>'])

        for key, value in self.combos.items():
            xx, yy, zz = value.count('<'), value.count('='), value.count('>')
            temp = [xx, yy, zz]
            maxi = temp.index(max(temp))

            if maxi == 0 and xx != zz:
                self.combos[key] = '<'
            elif maxi == 1 or xx == zz:
                self.combos[key] = '='
            elif maxi == 2 and xx != zz:
                self.combos[(key[1], key[0])] = self.combos.pop(key)
                self.combos[(key[1], key[0])] = '<'

        self.glob_order = sorted(self.names_list, cmp = self.comparator)

        self.glob_ineq = []
        for idx in range(len(self.glob_order)-1):
            self.glob_ineq.append(self.combos[(self.glob_order[idx],self.glob_order[idx+1])])

        if self.glob_ineq.count('<') == 0:
            self.glob_scores = [1.0 for xx in range(len(self.glob_order))]

        print self.names_list
        print self.relations
        print(self.glob_ineq.count('<'))
        incr = 1.0/self.glob_ineq.count('<')
        self.glob_scores = [0]
        for idx in range(len(self.glob_ineq)):
            if self.glob_ineq[idx] == '=':
                self.glob_scores.append(self.glob_scores[idx])
            elif self.glob_ineq[idx] == '<':
                self.glob_scores.append(self.glob_scores[idx]+incr)

        self.glob_scores = [float('%.2f'% item) for item in self.glob_scores]

        #return [self.glob_order, self.glob_ineq, self.glob_scores]
