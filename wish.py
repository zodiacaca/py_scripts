
from requests_html import HTMLSession

file1 = open('.txt', 'r')
wish1 = []


for line in file1:
  l = line[:-1] # last line
  wish1.append(l)
file1.close()

file2 = open('.txt', 'r')
wish2 = []

for line in file2:
  l = line[:-1] # last line
  wish2.append(l)
file2.close()

wish3 = []

for w1 in wish1:
  try:
    wish2.index(w1)
  except ValueError:
    wish3.append("https://store.steampowered.com/app/" + w1)

session = HTMLSession()

for w in wish3:
  r = session.get(w)
  t = r.html.find('title', first=True).text
  if t == "Sign In":
    print(w)
  else:
    print(t)
