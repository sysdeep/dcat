#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""модуль миграций"""
from app import log
from app.lib import fdate


def up1_to_2(connection):
	log.info("миграция 1 -> 2")

	#--- system - добавление строки с датой обновления
	SQL = """INSERT INTO system(key, value) VALUES("updated",?)"""
	cursor = connection.cursor()
	cursor.execute(SQL, (fdate.sql_date(),))
	
	#--- volumes - добавление колонки с датой обновления
	SQL = """ALTER TABLE volumes ADD COLUMN updated DATETIME"""
	cursor.execute(SQL)
	









def up2_to_3(connection):
	log.info("миграция 2 -> 3")
	
	cursor = connection.cursor()

	#--- volumes - добавление колонки с датой обновления
	SQL = """ALTER TABLE volumes ADD COLUMN description TEXT"""
	cursor.execute(SQL)


	