# tests/test_analyzer.py
from analyzer import analyze

def test_common_password():
    r = analyze("password")
    assert r["score"] < 10
    assert r["category"] == "Very Weak"

def test_entropy_effect():
    r1 = analyze("aaaaaa")   # low variety
    r2 = analyze("A3$kL9!pQ2#")  # high variety/length
    assert r2["score"] > r1["score"]
