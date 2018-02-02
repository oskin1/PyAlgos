import random


"""
Implementation of Gale-Shapley Stable Marriage Problem algorithm.
See: http://www.columbia.edu/~js1353/pubs/tst-ipco99.pdf
"""


class Pairable:
    
    def __init__(self, idx):
        self.idx = idx
        self.free = True
        self.prefs = []

    def gen_preferences(self, variants):
        points = range(0, 11)
        self.prefs = sorted([(v, random.choice(points)) for v in variants],
                            key=lambda v: v[1], reverse=True)

    def get_rating_for(self, variant):
        return list(filter(lambda i: i[0] is variant, self.prefs))[0][1]


class X(Pairable):
    
    def __init__(self, idx):
        super().__init__(idx)
        self.ys_tried = []

    def try_pair(self, pairable):
        if not isinstance(pairable, X):
            self.ys_tried.append(pairable)
            if pairable.free:
                return True
            return False
        raise Exception("Invalid pair")

    def __repr__(self):
        return "<X: {}>".format(self.idx)
    

class Y(Pairable):

    def __init__(self, idx):
        super().__init__(idx)

    def __repr__(self):
        return "<Y: {}>".format(self.idx)
    

class Group:
    
    def __init__(self, size):
        self.size = size
        self.xs = [X(idx) for idx in range(0, size)]
        self.ys = [Y(idx+11) for idx in range(0, size)]
        print(self.xs)
        print(self.ys)
        self.pairs = []
        self.iterations_done = 0

        for x in self.xs:
            x.gen_preferences(self.ys)

        for y in self.ys:
            y.gen_preferences(self.xs)

    def _make_pair(self, pair):
        pair[0].free, pair[1].free = False, False
        self.pairs.append(pair)

    def _replace_pair(self, old_pair, new_pair):
        self.pairs.remove(old_pair)
        self._make_pair(new_pair)

    def find_pairs(self):
        free_xs = list(filter(lambda x: x.free, self.xs))
        while len(free_xs):
            if self.iterations_done > (self.size * self.size):
                raise Exception("Not all pairs were found.")
            x = free_xs[0]
            if len(x.ys_tried) < self.size:
                i = 0
                while i < (len(self.ys) - 1) and x.free:
                    y = x.prefs[i][0]
                    i += 1
                    print("$ Testing {} with {}".format(x, y))
                    if not y in x.ys_tried:
                        if x.try_pair(y):
                            self._make_pair((x, y))
                        else:
                            y_pair = list(filter(lambda i: i[1] is y, self.pairs))
                            if len(y_pair) > 1:
                                raise Exception("<Y: {}> has more than 1 partner".format(y.idx))
                            elif len(y_pair) < 1:
                                raise Exception("<Y: {}> has no partner, but marked as free".format(y.idx))
                            
                            y_x = y_pair[0][0]
                            y_x_rating = y.get_rating_for(y_x)
                            x_rating = y.get_rating_for(x)
                            
                            if x_rating > y_x_rating:
                                self._replace_pair((y_x, y), (x, y))
                                y_x.free = True
                                
            free_xs = list(filter(lambda x: x.free, self.xs))
            self.iterations_done += 1
            print("Free XS Q: ", len(free_xs))

    def _sort_pairs(self):
        self.pairs = sorted(self.pairs,
                            key=lambda i: i[0].get_rating_for(i[1]) + i[1].get_rating_for(i[0]),
                            reverse=True)

    def print_final_pairs(self):
        print("Iterations done: {}".format(self.iterations_done))
        print("Index  :  ({x}, {y})  : CompScore\n")
        self._sort_pairs()
        for p in self.pairs:
            print("{pos}  :  ({x}|{xsc}, {y}|{ysc})  :  {ci}\n".format(pos=(self.pairs.index(p) + 1),
                                                         x=p[0], y=p[1], xsc=p[0].get_rating_for(p[1]), ysc=p[1].get_rating_for(p[0]),
                                                         ci=(p[0].get_rating_for(p[1]) + p[1].get_rating_for(p[0]))))

    def print_prefs_table(self):
        print("Preferences table for X's:")
        for x in self.xs:
            print(x, " ", x.prefs)
        print("Preferences table for Y's:")
        for y in self.ys:
            print(y, " ", y.prefs)


def main():
    group_size = int(input("Enter group size:  "))
    g = Group(group_size)
    g.find_pairs()
    g.print_prefs_table()
    g.print_final_pairs()
           

if __name__ == "__main__":
    main()
