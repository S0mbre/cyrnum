# -*- coding: utf-8 -*-

# https://en.wikipedia.org/wiki/Cyrillic_numerals
from cyrnum import Cyrnum

def main():
    cn = Cyrnum(480, color='blue', transparent=True, draw_exceptions=False)
    
    # randn = cn()
    # print(randn[0])
    # randn[1].show()

    cn[9000000000].show()

if __name__ == '__main__':
    main()