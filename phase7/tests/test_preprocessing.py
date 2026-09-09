from phase7.preprocessing import normalize_malayalam


def test_empty_input_returns_empty_string():
    assert normalize_malayalam("") == ""
    assert normalize_malayalam("   ") == ""


def test_existing_malayalam_is_preserved_when_no_rule_matches():
    text = "നാളെ രാവിലെ വരുമോ?"
    assert normalize_malayalam(text) == text


def test_evidence_backed_surface_forms_are_normalized():
    assert normalize_malayalam("നിനക്ക് ഇന്നു സുഖമാണോ?") == "നിനക്ക് ഇന്ന് സുഖമാണോ?"
    assert normalize_malayalam("ഒന്നു കാത്തിരിക്കൂ") == "ഒന്ന് കാത്തിരിക്കൂ"
    assert normalize_malayalam("എന്നെ ഒരു കോൾ ചെയ്യു") == "എന്നെ ഒരു കോൾ ചെയ്യൂ"
    assert normalize_malayalam("ഞാൻ ലേറ്റർ വിളിക്കം") == "ഞാൻ ലേറ്റർ വിളിക്കാം"


def test_cheyyu_rule_does_not_modify_longer_words():
    assert normalize_malayalam("എന്ത ചെയ്യുന്നെ?") == "എന്ത ചെയ്യുന്നെ?"
    assert normalize_malayalam("നീ എന്നെ ഹെൽപ്പ് ചെയ്യുമോ?") == "നീ എന്നെ ഹെൽപ്പ് ചെയ്യുമോ?"


def test_multiple_safe_rules_can_apply_in_one_sentence():
    text = "ഞാൻ ഇന്നു വന്ന് ഒന്നു പറയാം"
    assert normalize_malayalam(text) == "ഞാൻ ഇന്ന് വന്ന് ഒന്ന് പറയാം"
