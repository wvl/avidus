mac,sig = macd(close)
Series('mac', mac)
Series('sig', sig)

---# Start system

if crossesOver(sig, mac):
	buy()

if crossesOver(mac, sig):
	exitLong()
