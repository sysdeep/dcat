#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""модуль миграций"""
from app import log
from app.lib import fdate
from . import sql


def up1_to_2(connection):
	log.info("миграция 1 -> 2")

	cursor = connection.cursor()

	#--- system - добавление строки с датой обновления
	SQL = """INSERT INTO system(key, value) VALUES("updated",?)"""
	cursor.execute(SQL, (fdate.sql_date(),))
	
	#--- volumes - добавление колонки с датой обновления
	SQL = """ALTER TABLE volumes ADD COLUMN updated DATETIME"""
	cursor.execute(SQL)
	









def up2_to_3(connection):
	log.info("миграция 2 -> 3")
	
	cursor = connection.cursor()

	#--- system - добавление строки с описанием
	SQL = """INSERT INTO system(key, value) VALUES("description",?)"""
	cursor.execute(SQL, ("---",))

	#--- volumes - добавление колонки с описанием
	SQL = """ALTER TABLE volumes ADD COLUMN description TEXT"""
	cursor.execute(SQL)







def up3_to_4(connection):
	log.info("миграция 3 -> 4")

	cursor = connection.cursor()

	cursor.execute(sql.CREATE_FILES_INDEX_UUID)				# создание индекса files uuid
	cursor.execute(sql.CREATE_FILES_INDEX_PARENT_ID)		# создание индекса files parent_id




