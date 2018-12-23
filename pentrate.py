import random
import time
from epal_parser import epal_parser as hopefully_dope_parser
from epal_parser_without_optimization import epal_parser as old_and_clunky_epal_parser
import os


keywords = ["if ", "scur ", "cfh ", "end ", "blah ", "do ", "for ", "\n"]
words = 100000

if __name__ == "__main__":
    with open("penetrate_example.epal", 'w+') as penetrate_file:
        for i in range(words):
            penetrate_file.write(keywords[random.randint(0, 7)])
        comp_time = time.time()
        try:
            old_and_clunky_epal_parser("penetrate_example.epal")
        except:
            pass
        print("exec time old_parser parsing of " + str(words) + " words: " + str(time.time() - comp_time) + "s")
    with open("penetrate_example.epal", 'w+') as penetrate_file:
        for i in range(words):
            penetrate_file.write(keywords[random.randint(0, 7)])
        comp_time = time.time()
        try:
            hopefully_dope_parser("penetrate_example.epal")
        except:
            pass
        print("exec time new_parser parsing of " + str(words) + " words: " + str(time.time() - comp_time) + "s")
    os.remove("penetrate_example.cpp")

