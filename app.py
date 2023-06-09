import sys
import csv
import heapq
import os

GENDER = {'f':'die','m':'der','n':'das','':'None'}
CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nouns.csv')

def distance(s1, s2):
    d = [[x for x in range(len(s1)+1)] for _ in range(len(s2)+1)]
    
    for y in range(1,len(s2)+1):
        d[y][0] = d[y-1][0] + 1

    for x in range(1, len(s1)+1):
        for y in range(1, len(s2)+1):
            if s1[x-1] == s2[y-1]:
                d[y][x] = d[y-1][x-1]
            else:
                substute = d[y-1][x-1] + 1
                add = d[y][x-1] + 1
                delete = d[y-1][x] + 1
                d[y][x] = min(add, substute, delete)
    return d[-1][-1]


class HeapWordList:

    def __init__(self,max_count=3) -> None:
        self.heap_list = []
        self.max_count = max_count
        
    def __call__(self, count, word, lemma, genus):
        new_item = (-distance(word,lemma), lemma, GENDER.get(genus))

        if count < self.max_count:
            heapq.heappush(self.heap_list, new_item)
            return 
        if new_item[0] < self.heap_list[0][0]:
            return

        heapq.heapreplace(self.heap_list, new_item)

    def __iter__(self):
        for score, lemma, genus in self.heap_list:
            yield (score, lemma, genus)

    def __repr__(self):
        heap_list = [(- score , lemma, genus ) for score, lemma, genus in self.heap_list]
        return str(heap_list)


def read_csv(csv_name):
    with open(csv_name, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            yield row

def read_word_from_arg():
    if len(sys.argv) > 1:
        word = sys.argv[1]
        return word.lower()

def display_result(result):
    for _, lemma, genus in result:
        if genus == "None": continue
        print(f'{genus} {lemma.capitalize()}')

def run():
    word = read_word_from_arg()
    world_list = HeapWordList(max_count=5)

    for count, row in enumerate(read_csv(CSV_PATH)):
        lemma = row['lemma'].lower()
        genus = row['genus']
        if lemma == word:
            print(f"{GENDER.get(genus)} {lemma.capitalize()}")
            sys.exit()

        world_list(count=count, word=word, lemma=lemma, genus=genus)

    display_result(world_list)

if __name__ == "__main__":
    run()
