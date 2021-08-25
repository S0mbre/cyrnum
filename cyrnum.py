# -*- coding: utf-8 -*-

# https://en.wikipedia.org/wiki/Cyrillic_numerals
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps, ImageColor
import math, textwrap
from random import randint

DIGITS = {1: '\u0430', 2: '\u0432', 3: '\u0433', 4: '\u0434', 5: '\u0435', 6: '\u0455', 7: '\u0437', 8: '\u0438', 9: '\u045f', 10: '\u0456',
          20: '\u043a', 30: '\u043b', 40: '\u043c', 50: '\u043d', 60: '\u045c', 70: '\u043e', 80: '\u043f', 90: '\u0447', 100: '\u0440',
          200: '\u0441', 300: '\u0442', 400: '\u0443', 500: '\u0444', 600: '\u0445', 700: '\u0453', 800: '\u0491', 900: '\u0446'}
THOUSAND = '\uf030'
MAXNUMBER = 9999999999
FONTFILE = 'EvangelieTT.ttf'
DEFFONT = 'verdana.ttf'

class Cyrnum:

    def __init__(self, fontsize=256, bgcolor='white', color='black', transparent=False, 
                 koloda_simple=False, leodr_simple=False, titlo=True, draw_exceptions=False):
        self.bgcolor = ImageColor.getrgb(bgcolor)
        self.color = ImageColor.getrgb(color)
        if transparent:
            self.bgcolor = (self.bgcolor[0], self.bgcolor[1], self.bgcolor[2], 0)
            self.color = (self.color[0], self.color[1], self.color[2], 255)
        self.transparent = transparent
        self.fontsize = fontsize
        self.koloda_simple = koloda_simple
        self.leodr_simple = leodr_simple
        self.titlo = titlo
        self.draw_exceptions = draw_exceptions

    def _draw_exception(self, message, bgcolor=None, color=None):
        lines = textwrap.wrap(message, width=40)
        font = ImageFont.truetype(DEFFONT, math.ceil(self.fontsize / 4), encoding='unic')
        sizes = [font.getsize(line) for line in lines]
        maxw = max(sizes, key=lambda s: s[0])[0]
        maxh = max(sizes, key=lambda s: s[1])[1]
        margin = 10
        w = maxw + margin * 2
        h = len(lines) * (maxh + 2) + margin * 2 - 2
        img = Image.new('RGBA' if self.transparent else 'RGB', (w, h), bgcolor or self.bgcolor)
        draw = ImageDraw.Draw(img)
        y = margin
        color = color or self.color
        for line, sz in zip(lines, sizes):
            draw.text(((w - sz[0]) / 2, y), line, font=font, fill=color)
            y += sz[1] + 2
        return img
        
    def _autocrop(self, img, bgcolor=None, onbox=None):
        mode_ = 'RGBA' if self.transparent else 'RGB'
        if img.mode != mode_:
            img = img.convert(mode_)
        bgcolor = bgcolor or self.bgcolor
        bg = Image.new(mode_, img.size, bgcolor)
        diff = ImageChops.difference(img, bg)
        bbox = diff.getbbox()
        if bbox:
            if onbox: onbox(img, bbox)
            return img.crop(bbox)
        return img

    def _combine_images(self, images, margins_rl=0, margins_tb=0, yoffsets=None):
        if not images:
            raise Exception('Нет изображений для склеивания!')

        isdict = isinstance(images[0], dict)
        widths, heights = zip(*(i['img'].size for i in images)) if isdict else zip(*(i.size for i in images))
        xinterval = math.ceil(max(widths) * 0.05)
        
        total_width = sum(widths) + margins_rl*2 + (len(widths) - 1) * xinterval
        max_height = max(heights)
        total_height = max_height + margins_tb*2

        new_im = Image.new('RGBA' if self.transparent else 'RGB', (total_width, total_height), self.bgcolor)

        x_offset = margins_rl
        
        for j, im in enumerate(images):
            img = im['img'] if isdict else im
            yoffset = im['yoffset'] if isdict else 0
            if yoffsets: yoffset += yoffsets[j]
            new_im.paste(img, (x_offset, yoffset))
            x_offset += img.size[0] + xinterval
            
        return new_im

    def _draw_txt_rot(self, img, x, y, txt, angle=0):
        font = ImageFont.truetype(FONTFILE, math.ceil(self.fontsize * 0.3), encoding='unic')
        imcomma = Image.new('RGBA', (500, 500), self.bgcolor) if self.transparent else Image.new('L', (500, 500))
        draw = ImageDraw.Draw(imcomma)
        draw.text((0, 0), txt, fill=self.color if self.transparent else 255, font=font)
        imcomma1 = imcomma.rotate(360 - angle, expand=True)
        imcomma2 = imcomma1 if self.transparent else ImageOps.colorize(imcomma1, self.bgcolor, self.color)
        imcomma3 = self._autocrop(imcomma2)
        img.paste(imcomma3, (x - round(imcomma3.size[0]/2), y - round(imcomma3.size[1]/2)))

    def _draw_digit(self, dig, exp=0, **fontparams):
        dig_txt = DIGITS[dig]
        
        if exp > 9:
            raise Exception('Невозможно записать число с порядком более 9! ')
        
        font = ImageFont.truetype(FONTFILE, self.fontsize, encoding='unic')
        imgsize = font.getsize(' \u0192 ')
        img = Image.new('RGBA' if self.transparent else 'RGB', tuple(math.ceil(x * 3) for x in imgsize), self.bgcolor)
        draw = ImageDraw.Draw(img)
        point = (math.floor(imgsize[0] / 1.2), 0)

        outimg = {'img': None, 'yoffset': 0}

        # calc bounding box 
        tbox = draw.textbbox(point, dig_txt, font=font, **fontparams)
        tboxw = tbox[2] - tbox[0]
        tboxh = tbox[3] - tbox[1]
        
        if exp == 3:
            # draw thousand sign
            font2 = ImageFont.truetype(FONTFILE, round(self.fontsize * 0.5), encoding='unic')
            tbox = font2.getbbox(THOUSAND, **fontparams)
            pt = (point[0], point[1] + round(self.fontsize / 2))
            draw.text(pt, THOUSAND, fill=self.color, font=font2, **fontparams)
            point = (point[0] + tbox[2] + 2, point[1])
        
        draw.text(point, dig_txt, fill=self.color, font=font, **fontparams)        
        #draw.rectangle(tbox, outline='red')
            
        if exp < 4:
            # we're done!
            outimg['img'] = self._autocrop(img)
            return outimg

        #print(f'tbox = {tbox}')
        # get longest side
        llongest = max(tboxw, tboxh)       
        # calc circle bounding box
        d = 2
        # get outer bbox
        outerbox_tl = (round(tbox[0] - (llongest - tboxw) / 2 - d), round(tbox[1] - (llongest - tboxh) / 2 - d)) 
        outerbox = [outerbox_tl[0], outerbox_tl[1], outerbox_tl[0] + llongest + 2*d, outerbox_tl[1] + llongest + 2*d]        
        #draw.rectangle(outerbox, outline='blue')
        
        # get center point
        center = tuple(x + d + llongest//2 for x in outerbox_tl)
        r = round(math.hypot(llongest/2 + d, llongest/2 + d))
        #print(f'Center = {center}')

        w = math.ceil(self.fontsize / 24)
        img_src = self._autocrop(img)
        h_src = img_src.size[1]

        if exp == 4:
            # тьма -- кружок
            dif = w * 2
            outerbox2 = [outerbox[0] - dif, outerbox[1] - dif, outerbox[2] + dif, outerbox[3] + dif]
            draw.ellipse(outerbox2, outline=self.color, width=w)
                        
        elif exp == 5:
            # легион (неведий) -- кружок из точек
            dif = math.ceil(self.fontsize / 48)
            for deg in range(0, 360, 15):
                rad = math.radians(deg)
                x = center[0] + round(r * math.cos(rad))
                y = center[1] + round(r * math.sin(rad))
                if dif > 1:
                    draw.ellipse([x - dif, y - dif, x + dif, y + dif], fill=self.color)
                else:
                    draw.point([x, y], fill=self.color)
            
        elif exp == 6:
            # леодр -- кружок из палочек
            r2 = r + math.ceil(self.fontsize / 12)
            for deg in range(0, 360, 15):
                rad = math.radians(deg)
                sin_ = math.sin(rad)
                cos_ = math.cos(rad)
                if self.leodr_simple:
                    draw.line([center[0] + round(r * cos_), center[1] + round(r * sin_),
                            center[0] + round(r2 * cos_), center[1] + round(r2 * sin_)],
                            fill=self.color, width=w)
                else:
                    # в виде запятых
                    self._draw_txt_rot(img, center[0] + round(r * cos_), center[1] + round(r * sin_), '\u002c', deg + 270)
            
        elif exp == 7:
            # вран (ворон) -- кружок из крестиков
            dif = math.ceil(self.fontsize / 24)
            for deg in range(0, 360, 45):
                rad = math.radians(deg)
                x = center[0] + round(r * math.cos(rad))
                y = center[1] + round(r * math.sin(rad))                
                draw.line([x - dif, y - dif, x + dif, y + dif], fill=self.color, width=w)
                draw.line([x + dif, y - dif, x - dif, y + dif], fill=self.color, width=w)
            
        elif exp == 8:
            # клада (колода) -- 'колода', скобки сверху и снизу
            dif = math.ceil(self.fontsize / 36)
            if self.koloda_simple:
                draw.line([(tbox[0] - dif, tbox[1] + dif), (tbox[0] - dif, tbox[1] - dif * 2), 
                        (tbox[2] + dif, tbox[1] - dif * 2), (tbox[2] + dif, tbox[1] + dif)],
                        fill=self.color, width=w, joint='curve')
                draw.line([(tbox[0] - dif, tbox[3] - dif), (tbox[0] - dif, tbox[3] + dif * 2), 
                        (tbox[2] + dif, tbox[3] + dif * 2), (tbox[2] + dif, tbox[3] - dif)],
                        fill=self.color, width=w, joint='curve')
            else:
                dif = math.ceil(self.fontsize / 18) + w
                outerbox2 = [outerbox[0] - dif, outerbox[1] - dif, outerbox[2] + dif, outerbox[3] + dif]
                r = round((outerbox2[2] - outerbox2[0]) / 2)

                draw.arc(outerbox2, 200, 340, fill=self.color, width=w)
                rad = math.radians(200)
                x1 = center[0] + round(r * math.cos(rad)) + w
                y1 = center[1] + round(r * math.sin(rad))
                draw.line([x1, y1, x1 - dif - w, y1], fill=self.color, width=w)
                x1 = center[0] + round(r * math.cos(math.radians(340))) - w
                draw.line([x1, y1, x1 + dif + w, y1], fill=self.color, width=w)

                draw.arc(outerbox2, 20, 160, fill=self.color, width=w)
                rad = math.radians(160)
                x1 = center[0] + round(r * math.cos(rad)) + w
                y1 = center[1] + round(r * math.sin(rad))
                draw.line([x1, y1, x1 - dif - w, y1], fill=self.color, width=w)
                x1 = center[0] + round(r * math.cos(math.radians(20))) - w
                draw.line([x1, y1, x1 + dif + w, y1], fill=self.color, width=w)
        
        elif exp == 9:
            # тьма тем -- по три палки снизу, слева и справа и крестик сверху
            dif = w
            stickl = round(llongest / 3)
            halfstickl = round(stickl / 2)
            # left box
            x1 = tbox[0] - dif - stickl
            y1 = tbox[1] + round((tboxh - stickl) / 2)
            x2 = tbox[0] - dif
            for i in range(3):
                yy = y1 + i * halfstickl
                draw.line([x1, yy, x2, yy], fill=self.color, width=w)
            # right box
            x1 = tbox[2] + dif
            x2 = x1 + stickl
            for i in range(3):
                yy = y1 + i * halfstickl
                draw.line([x1, yy, x2, yy], fill=self.color, width=w)
            # bottom box
            x1 = tbox[0] + round((tboxw - stickl) / 2)
            y1 = tbox[3] + dif
            y2 = y1 + stickl
            for i in range(3):
                xx = x1 + i * halfstickl
                draw.line([xx, y1, xx, y2], fill=self.color, width=w)
            # upper cross
            y1 = tbox[1] - dif - stickl
            y2 = y1 + stickl
            draw.line([x1, y1 + halfstickl, x1 + stickl, y1 + halfstickl], fill=self.color, width=w)
            draw.line([x1 + halfstickl, y1, x1 + halfstickl, y2], fill=self.color, width=w)      
            
        outimg['img'] = self._autocrop(img)
        outimg['yoffset'] = round((h_src - outimg['img'].size[1]) / 2)
        return outimg

    def _draw_999(self, number, exp=0, dryrun=False, **kwargs):
        s = str(number)
        if len(s) > 3:
            raise Exception('Функция _draw_999() принимает только 1, 2 и 3-значные числа!')
        images = []
        ten = False
        if len(s) > 2:
            hund = int(s[0])
            num = hund * 100 if exp < 3 else hund
            images.append({'dig': hund, 'num': num, 'exp': exp + 2, 'char': DIGITS[num], 'img': None if dryrun else self._draw_digit(num, exp + 2, **kwargs)})
            s = s[1:]
        if len(s) > 1:
            tens = int(s[0])
            if tens:
                ten = (tens == 1)
                num = tens * 10 if exp < 3 else tens
                images.append({'dig': ten, 'num': num, 'exp': exp + 1, 'char': DIGITS[num], 'img': None if dryrun else self._draw_digit(num, exp + 1, **kwargs)})
            s = s[1:]
        ones = int(s[0])
        if ones:
            if exp < 3 and ten:
                pos = 1 if len(images) == 2 else 0
                images.insert(pos, {'dig': ones, 'num': ones, 'exp': exp, 'char': DIGITS[ones], 'img': None if dryrun else self._draw_digit(ones, exp, **kwargs)})
            else:
                images.append({'dig': ones, 'num': ones, 'exp': exp, 'char': DIGITS[ones], 'img': None if dryrun else self._draw_digit(ones, exp, **kwargs)})
                
        return images

    def _parse_number(self, number):
        s = str(number)
        l = []
        while len(s):
            l.insert(0, int(s[-3:]))
            s = s[:-3]
        return l

    def _get_char_offsets(self, text, debug=False, **fontparams):
        font = ImageFont.truetype(FONTFILE, self.fontsize, encoding='unic')
        
        imgsize = font.getbbox(text, **fontparams)
        m = 10 if debug else 0
        img = Image.new('RGB', (imgsize[2], imgsize[3] + m * 2), self.bgcolor)
        draw = ImageDraw.Draw(img)
        x = 0
        y = 0
        if debug:
            draw.text((x, y + m), text, fill=self.color, font=font, **fontparams)
            font2 = ImageFont.truetype(DEFFONT, 56, encoding='unic')
        offsets = []
        for ch in text:
            tbox = draw.textbbox((x, y + m), ch, font, **fontparams)
            offsets.append(tbox[1] - m)
            if debug:
                draw.rectangle(tbox, outline='#f00')
                draw.text((x + (tbox[2] - tbox[0]) // 2, y + 2), str(tbox[1] - m), fill='#f00', font=font2, anchor='mt')
            x = tbox[2]
        
        if debug:
            img.show()

        return offsets

    def draw(self, number):
        sdif = math.ceil(self.fontsize / 5)
        ldif = math.ceil(self.fontsize / 3)

        try:
            if number < 1 or number > MAXNUMBER:
                raise Exception('Число должно быть от 1 до 9 999 999 999!')
            chunks = self._parse_number(number)
            l = len(chunks)

            images_all = []
            for i, num in enumerate(chunks):
                if num: images_all += self._draw_999(num, (l - 1 - i) * 3)
            ssdif = sdif if self.titlo else 0
            yoffsets = [ssdif + off for off in self._get_char_offsets(''.join([im['char'] for im in images_all]))]
            combimg = self._combine_images([im['img'] for im in images_all], sdif, ldif if self.titlo else sdif, yoffsets=yoffsets)

        except Exception as err:
            if self.draw_exceptions:
                return self._draw_exception(str(err))
            else:
                raise
        
        # титло
        if self.titlo:
            draw = ImageDraw.Draw(combimg)
            x1 = sdif
            y1 = sdif
            x2 = combimg.size[0] - sdif
            y2 = y1 * 2
            draw.line([(x1, y2), (x1, y1), (x2, y1), (x2, y1 - sdif)], fill=self.color, width=math.ceil(self.fontsize / 12), joint='curve')
        
        return combimg

    def random_numbers(self, from_=1, to_=MAXNUMBER, n=1):
        numbas = []
        for _ in range(n):
            r = randint(from_, to_)
            numba = (r, self.draw(r))
            if n < 2: return numba
            numbas.append(numba)
        return numbas

    def __getitem__(self, key):
        return self.draw(key)

    def __call__(self, key=None):
        if key is None:
            return self.random_numbers()
        elif key > 0:
            return self.draw(key)
        raise Exception(f'Неверный параметр ({key})!')