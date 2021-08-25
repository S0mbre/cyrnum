# -*- coding: utf-8 -*-

# https://en.wikipedia.org/wiki/Cyrillic_numerals
from cyrnum import Cyrnum, DIGITS

def main():
    cn = Cyrnum(256, color='blue', transparent=False, draw_exceptions=True, titlo=True)
    
    # randn = cn()
    # print(randn[0])
    # randn[1].show()

    cn[178000000].show()
    # cn.get_char_offsets(''.join(DIGITS.values()))

if __name__ == '__main__':
    main()