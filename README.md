cfclass
=======

Python class for CodeForces API, mostly used in conky, but may be use in other ways

Run:

  conky.py [options]

Parameters:

  visual options:

  --hr              - output $hr after every block
  --colors          - make output more pretty, add ${color ...}, e.g. to change user rank
  --contest-color   - set up contest color, in next order BEFORE, RUNNING, PENDING_SYSTEM_TEST, SYSTEM_TEST, FINISHED.
  If you need skip some color, don`t change, just don`t write color, e.g #ffffff,,#ffffff,#ffa200

  blocks:

  --next-contest-list                   - show list of future contests with date
  --user-info handle,...,handle         - show user info for user in list
  --current-standings handle,...,handle - show list of current standings for user in list
  
  Sample .conky line (updated every 16 seconds):
  
${execpi 16  python ~/source/cfclass/conky.py --next-contest-list --hr --colors}
