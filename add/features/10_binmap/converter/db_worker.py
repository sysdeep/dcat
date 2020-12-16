

from . import models


def get_volumes(connection) -> list:
	"""получить список всех томов"""
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM volumes;")
	rows = cursor.fetchall()
	result = models.make_vnodes(rows)
	return result

def get_volume_files(connection, volume_id) -> list:
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM files WHERE volume_id=?", (volume_id, ))
	rows = cursor.fetchall()
	result = models.make_fnodes(rows)
	return result