cfclass
=======

Python class for CodeForces API, mostly used in conky, but may be use in other ways

Run:
  conky.py [options]

Parameters:
  visual options:
  --hr      - output $hr after every block
  --colors  - make output more pretty, add ${color ...}, e.g. to change user rank

  blocks:
  --next-contest-list           - show list of future contests with date
  --user-info handle,...,handle - show user info for user in list
  
  Sample .conky line (updated every 16 seconds):
${execpi 16  python ~/source/cfclass/conky.py --next-contest-list --hr --colors}
