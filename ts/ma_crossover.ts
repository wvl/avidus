ma = sma(close,30)
Series('ma', ma)

---

if crossesOver(close, ma):
	buy()

if crossesOver(ma, close):
	sell()

