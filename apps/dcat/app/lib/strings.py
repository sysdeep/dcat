def cut_text(text, cut_len=80, dots="..."):
    """
		обрезка текста до заданной длины
		если указаны символы дополнения они включаются в результатирующий набор заданной длинны

		cut_text("hello", 6, "...")		->	hel...
		cut_text("hello", 6, "..")		->	hell..
		cut_text("hello", 6, "")		->	hello

		Args:
	    	text	[string] 	:	исходная с трока
	    	cut_len	[int]		: 	длина обрезки
	    	dots	[string]	: 	символы дополнения
	"""
    if len(text) + len(dots) > cut_len:
        text = text[0:(cut_len - len(dots))] + dots
    return text


if __name__ == "__main__":

    print(cut_text("hello", 6, ""))
