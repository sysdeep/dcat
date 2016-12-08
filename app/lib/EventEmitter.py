#!/usr/bin/env python
# -*- coding: utf-8 -*-


#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
EventEmitter object similar to the EventEmitter from Node.js.

"""


from collections import defaultdict



class EventEmitter(object):
	"""The EventEmitter class.


	"""
	def __init__(self):
		self.__events = defaultdict(list)

	def eon(self, event, f=None):
		"""Registers the function ``f`` to the event name ``event``.
		"""
		self.__events[event].append(f)

		#
		# def _on(f):
		#     # Fire 'new_listener' *before* adding the new listener!
		#     self.emit('new_listener', event, f)
		#
		#     # Add the necessary function
		#     self._events[event].append(f)
		#
		#     # Return original function so removal works
		#     return f

		# if f is None:
		#     return _on
		# else:
		#     return _on(f)

	def emit(self, event, *args, **kwargs):
		"""Emit ``event``, passing ``*args`` to each attached function. Returns
		``True`` if any functions are attached to ``event``; otherwise returns
		``False``.

		Example:

			ee.emit('data', '00101001')

		Assuming ``data`` is an attached function, this will call
		``data('00101001')'``.

		"""
		# handled = False

		# Pass the args to each function in the events dict
		for f in self.__events[event]:
			f(*args, **kwargs)
			# handled = True

		# if not handled and event == 'error':
		# 	raise Exception("Uncaught 'error' event.")
		#
		# return handled

	# def once(self, event, f=None):
	# 	"""The same as ``ee.on``, except that the listener is automatically
	# 	removed after being called.
	# 	"""
	# 	def _once(f):
	# 		def g(*args, **kwargs):
	# 			f(*args, **kwargs)
	# 			self.remove_listener(event, g)
	# 		return g
	#
	# 	if f is None:
	# 		return lambda f: self.on(event, _once(f))
	# 	else:
	# 		self.on(event, _once(f))

	def eoff(self, event, f):
		"""Removes the function ``f`` from ``event``.

		Requires that ``f`` is not closed over by ``ee.on``. (In other words,
		it is, unfortunately, not possible to use this with the decorator
		style is.)

		"""
		self.__events[event].remove(f)

	def eoffa(self, event=None):
		"""Remove all listeners attached to ``event``.
		"""
		if event is not None:
			self.__events[event] = []
		else:
			self.__events = None
			self.__events = defaultdict(list)

	def listeners(self, event):
		"""Returns the list of all listeners registered to the ``event``.
		"""
		return self.__events[event]



if __name__ == "__main__":


	ee = EventEmitter()




	def cb1(message):
		print("cb1", message)

	def cb2(message):
		print("cb2", message)


	ee.eon("qqq", cb1)
	ee.eon("qqq", cb2)

	ee.emit("qqq", "hello")




	# cb2 = None

	ee.eoff("qqq", cb2)

	ee.emit("qqq", "hello")





