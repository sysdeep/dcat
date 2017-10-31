#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re



#--- Sort the given iterable in the way that humans expect.(https://stackoverflow.com/questions/2669059/how-to-sort-alpha-numeric-set-in-python)
convert = lambda text: int(text) if text.isdigit() else text
alphanum_key = lambda key: [convert(c) for c in re.split(r'([0-9]+)', key)]


#
#
# def sorted_nicely( l ):
#     """ Sort the given iterable in the way that humans expect."""
#     convert = lambda text: int(text) if text.isdigit() else text
#     alphanum_key = lambda key: [convert(c) for c in re.split(r'([0-9]+)', key)]
#     return sorted(l, key=alphanum_key)



#--- сортировка с учётом цифр - проблема, если 1 символ строка и число - ошибка
# abdig_sort = lambda var: [int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var.name)]