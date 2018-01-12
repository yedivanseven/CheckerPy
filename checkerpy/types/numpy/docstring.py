DOC_HEADER = 'Checks if the dtype of a numpy array or scalar is {}.'
DOC_BODY = ('\n\n'
            'Parameters\n'
            '----------\n'
            'value\n'
            '    The numpy array or scalar to check the dtype of.\n'
            'name : str, optional\n'
            '    Name of the variable to check the dtype of.\n'
            '    Defaults to None.\n'
            '\n'
            'Returns\n'
            '-------\n'
            'value\n'
            '    The `value` passed in.\n'
            '\n'
            'Attributes\n'
            '----------\n'
            'dtypes : tuple(dtype)\n'
            '    The dtype(s) to check for.\n'
            '\n'
            'Methods\n'
            '-------\n'
            'JustNdArray(array, name) : ndarray\n'
            '    Checks if the (optionally named) argument is a numpy array\n'
            '    before passing it (and its `name`, if provided) on to the\n'
            '    actual dtype checker.\n'
            'o(callable) : CompositionOf\n'
            '    Daisy-chains the dtype checker to another `callable`,\n'
            '    returning the functional composition of both.\n'
            '\n'
            'Raises\n'
            '------\n'
            'DtypeError\n'
            '    If the variable passed to the dtype checker is not a numpy\n'
            '    array or scalar.\n'
            'WrongTypeError\n'
            '    If the dtype of the numpy array or scalar is not among the\n'
            '    allowed dtypes.\n'
            '\n'
            'See also\n'
            '--------\n'
            'JustDtype, CompositionOf')
