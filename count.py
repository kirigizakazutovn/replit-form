from collections import Counter
from json import loads

from replit import db

votes = {}

for vote in db.values():
  vote = loads(vote)
  for key, item in vote.items():
    if key not in votes:
      votes[key] = Counter({ item:1 })
    else:
      votes[key][item] += 1

for key, value in votes.items():
  print(key)
  print(value.most_common(2))
  print()
