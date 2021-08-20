# -*- coding: utf-8 -*-

# https://en.wikipedia.org/wiki/Cyrillic_numerals
from cyrnum import Cyrnum

def main():
    cn = Cyrnum(480)
    
    # randn = cn()
    # print(randn[0])
    # randn[1].show()

    cn[9999999999].show()

if __name__ == '__main__':
    main()