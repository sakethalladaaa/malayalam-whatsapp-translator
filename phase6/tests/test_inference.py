from phase6.inference import create_engine, transliterate


def test_roman_malayalam_transliteration():
    engine = create_engine()
    output = transliterate("vegam vaa", engine=engine)

    assert output
    assert any("\u0D00" <= char <= "\u0D7F" for char in output)
