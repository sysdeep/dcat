#!/usr/bin/env python3
# -*- coding: utf-8 -*-




DATA = {
    "parents"   : {}
}





def get_parent(db, parent_id):
    """получить объект из кэша или из базы"""
    if parent_id in DATA["parents"]:
        parent = DATA["parents"][parent_id]
        return parent
    else:
        parent = db.get_file(parent_id)
        DATA["parents"][parent_id] = parent
        return parent




def find_parent(db, fnode, parent_id):
    """рекурсивный поиск родителей"""

    #--- родителя нет - завершаем
    if parent_id == "0":
        pass
        
    else:
        #--- находим родителя
        parent = get_parent(db, parent_id)

        #--- сохраняем его
        fnode.parents.append(parent)

        #--- запускаем новый поиск
        find_parent(db, fnode, parent.parent_id)



def find_top_items(db, fnodes):
    """выполняем рекурсивный поиск для наиденных элементов"""
    
    
    #--- очищаем кэш
    DATA["parents"] = {}
    

    #--- для каждого элемента создаём путь
    for fnode in fnodes:

        find_parent(db, fnode, fnode.parent_id)


    #--- очищаем кэш
    DATA["parents"] = {}

    return fnodes