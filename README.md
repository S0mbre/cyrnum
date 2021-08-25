# cyrnum

## [EN]

### Convert integer numbers to archaic Cyrillic letter form. See Wikipedia article [here](https://en.wikipedia.org/wiki/Cyrillic_numerals).

Pure Python app with local (console) and web (GUI) version to convert any numbers from *1* to  *10^9^ - 1* to the [Cyrillic format](https://en.wikipedia.org/wiki/Cyrillic_numerals).

The engine in `cyrnum.py` is the `Cyrnum` class. Its main method is `draw()` taking a single argument -- an integer number and returning a PIL image of the Cyrillic representation, given the rendering parameters passed to the class constructor. For example, `draw(2021)` will produce the following image:

![2021](https://disk.yandex.ru/i/H8uYHTGV_yLbMg)

#### Console App
To run the **console app**, launch `cyrnummain.py` (see examples in that file). You first create an instance of `Cyrnum`:
```python
cn = Cyrnum(256, # font size
            color='black', # black characters
            transparent=False, # opaque background (default = white)
            draw_exceptions=True, # output exceptions as images
            titlo=True) # show 'titlo' symbol above the Cyrillic characters
```

The rendering parameters you can pass to the constructor are:
- `fontsize`: size of text controlling the size of the output image and all geometry (default = 256)
- `bgcolor`: the background color (any color name [understood by PIL](https://pillow.readthedocs.io/en/stable/reference/ImageColor.html))
- `color`: the text color (default = "black")
- `transparent`: whether the image must have a transparent background (if `True`, then `bgcolor` is ignored)
- `koloda_simple`: controls the look of the Cyrillic *koloda* symbol (*x * 10^8^*)
- `leodr_simple`: controls the look of the Cyrillic *leodr* symbol (*x * 10^6^*)
- `titlo`: whether to crown the output with the titlo (horizontal tilde), as required by tradition
- `draw_exceptions`: whether exceptions should also be rendered as an image

Then call `draw()` either directly or using overloaded operators. For example, any of the lines below will produce the Cyrillic representation of the number 3000:
- `cn.draw(3000).show()`
- `cn(3000).show()`
- `cn[3000].show()`

To produce a random number representation, you can do simply `cn().show()`.

Of course, you can also do anything with the returned image -- save, transform, add filters etc. (check out the [PIL docs](https://pillow.readthedocs.io/en/stable/reference/)).

#### Web App
To run the **web app** on localhost (your computer), change the `RUNLOCAL` global variable in `index.py` to `True` and launch `index.py`. (`RUNLOCAL` set to `False` is kept for the non-local app available on Heroku [here](https://cyrnum.herokuapp.com/).)

![Screenshot of the web app](https://disk.yandex.ru/i/NnCnCBTj8tLqEg)

The web app lets you enter the number and configure the rendered image using GUI controls on a single page.  There is also a button to produce a random input number below the main input field.

The public version is available on Heroku [here](https://cyrnum.herokuapp.com/).

## [RU]

### Отображение чисел в кириллической записи. См. статью в Википедии [здесь](https://ru.wikipedia.org/wiki/Система_записи_чисел_кириллицей).

Приложение, написанное на чистом python, с двумя интерфейсами (консольный и веб) для конвертации любых целых чисел от *1* до  *10^9^ - 1* в [кириллическую систему](https://ru.wikipedia.org/wiki/Система_записи_чисел_кириллицей).

Движок приложения -- класс `Cyrnum` в файле `cyrnum.py`. Основной метод -- `draw()` принимает единственный аргумент -- целое число и возвращает битмап (картинку) в формате PIL этого числа, записанного кириллицей с учетом параметров отображения, передаваемых в конструктор класса. Например, `draw(2021)` сгенерирует такое изображение:

![2021](https://disk.yandex.ru/i/H8uYHTGV_yLbMg)

#### Консольный интерфейс
Для работы приложения **из консоли** запустите `cyrnummain.py` (см. примеры в этом файле). Сначала создаем объект `Cyrnum`:
```python
cn = Cyrnum(256, # размер шрифта
            color='black', # цвет текста черный
            transparent=False, # непрозрачный фон (по умолчанию - белый)
            draw_exceptions=True, # выводить ошибки в виде изображения
            titlo=True) # отображать титло над знаками
```

Параметры конструктора класса, влияющие на отображение:
- `fontsize`: размер шрифта, влияющий на итоговый размер картинки и всей геометрии (по умолчанию = 256)
- `bgcolor`: цвет / заливка фона (в формате [PIL](https://pillow.readthedocs.io/en/stable/reference/ImageColor.html))
- `color`: цвет текста (по умолчанию = "black", т.е. черный)
- `transparent`: прозрачный ли фон (если `True`, параметр `bgcolor` игнорируется)
- `koloda_simple`: вариант отображения знака *колода* (*x * 10^8^*)
- `leodr_simple`: вариант отображения знака *леодр* (*x * 10^6^*)
- `titlo`: отображение знака *титло* над числом (как того требует кириллическая система)
- `draw_exceptions`: выводить ли ошибки в виде изображения

Далее вызовите метод `draw()` либо напрямую, либо при помощи перегруженных операторов. Например, любая из строк ниже сгенерирует отображение числа 3000:
- `cn.draw(3000).show()`
- `cn(3000).show()`
- `cn[3000].show()`

Для отображения случайного числа можно просто вызвать `cn().show()`.

Конечно, с полученным изображением можно делать далее все, что хотите -- сохранить, трансформировать, применить фильтры и т.п. (см. [документацию PIL](https://pillow.readthedocs.io/en/stable/reference/)).

#### Веб-интерфейс
Для запуска **веб-приложения** на локальном хосте (вашем компьютере), установите значение глобальной переменной `RUNLOCAL` в файле `index.py` на `True` и запустите `index.py`. (`RUNLOCAL = False` установлено по умолчанию для [приложения на Heroku](https://cyrnum.herokuapp.com/).)

![Скриншот веб-приложения](https://disk.yandex.ru/i/NnCnCBTj8tLqEg)

Веб-приложение позволяет генерировать изображения при помощи элементов управления, расположенных на одной странице.  Также есть кнопка для генерации случайного числа под полем ввода числа.

Публичная версия приложения на Heroku [по ссылке](https://cyrnum.herokuapp.com/).