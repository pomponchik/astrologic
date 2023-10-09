from astrologic import switcher


def test_simple_switch():
    @switcher(a=False, b=True)
    def function():
        lst = []

        lst.append('begin')
        if a:
            lst.append('block a')
        if b:
            lst.append('block b')
        lst.append('end')
        
        return lst

    assert function() == ['begin', 'block b', 'end']
