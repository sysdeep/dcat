#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Bits & Bytes related humanization."""

suffixes = {
	'decimal': ('kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'),
	'binary': ('KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB')
}


def naturalsize(value, binary=False, format='%.1f'):
	"""Format a number of byteslike a human readable filesize (eg. 10 kB).  By
	default, decimal suffixes (kB, MB) are used.  Passing binary=true will use
	binary suffixes (KiB, MiB) are used and the base will be 2**10 instead of
	10**3.  If ``gnu`` is True, the binary argument is ignored and GNU-style
	(ls -sh style) prefixes are used (K, M) with the 2**10 definition.
	Non-gnu modes are compatible with jinja2's ``filesizeformat`` filter."""

	if binary:
		suffix = suffixes['binary']
	else:
		suffix = suffixes['decimal']

	base = 1024 if binary else 1000
	bytes = float(value)

	if bytes < base:
		return '%d b' % bytes


	for i, s in enumerate(suffix):
		unit = base ** (i + 2)
		if bytes < unit:
			return (format + ' %s') % ((base * bytes / unit), s)



if __name__ == "__main__":


	value = 100
	print(naturalsize(value))
	print(naturalsize(value, True))