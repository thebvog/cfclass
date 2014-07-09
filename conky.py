import cfclass
import sys
import os
import datetime



def to_int(name, value):
    try:
        return int(value)
    except ValueError:
        print(name + ' = ' + str(value) + ' must be integer')
        sys.exit(0)

# main object of CodeForces API
cf = cfclass.CodeForces()

# parameters
top = -1
hr = False
colors = False
special_chars = [
    {'from': '$', 'to': '\$'},
    {'from': '#', 'to': '\#'},
    {'from': '\n', 'to': ' '},
    {'from': '\r', 'to': ' '}
]
contest_colors = {
    'BEFORE': '${color #ff7373}',
    'RUNNING': '${color #ffee59}',
    'PENDING_SYSTEM_TEST': '${color #ffee59}',
    'SYSTEM_TEST': '${color #ffee59}',
    'FINISHED': '${color #6fff6e}'
}
argc = len(sys.argv)
for i in range(1, argc):
    if (sys.argv[i] == '--top') and (i < argc - 1):
        top = to_int('--top', sys.argv[i + 1])
    if sys.argv[i] == '--hr':
        hr = True
    if sys.argv[i] == '--colors':
        colors = True

# select main response function
for i in range(1, len(sys.argv)):
    if sys.argv[i] == '--next-contest-list':
        result = cf.getContestList()
        for contest in result:
            if contest['phase'] != 'BEFORE':
                continue

            # filter special characters
            for char in special_chars:
                contest['name'] = contest['name'].replace(char['from'], char['to'])

            # add time
            if colors:
                line = '%d %s%s $color' % (contest['id'], contest_colors[contest['phase']], contest['name'])
            else:
                line = '%d %s' % (contest['id'], contest['name'])
            date = datetime.datetime.fromtimestamp(
                    int(contest['startTimeSeconds'])
            ).strftime('%d.%m.%Y %H:%M:%S')
            line += os.linesep + '\t' + date

            # output
            print(line)

        if hr:
            print('$color$hr')

    if (sys.argv[i] == '--user-info') and (i < argc - 1):
        handles = sys.argv[i + 1]
        handles = handles.split(',')
        result = cf.getUserInfo(handles)
        for user in result:
            if colors:
                line = '${color %s} %s %s, %d' % (user['color'], user['rank'], user['handle'], user['rating'])
            else:
                line = '%s %s, %d' % (user['rank'], user['handle'], user['rating'])
            print(line)

        if hr:
            print('$color$hr')

    # debug default method
    if sys.argv[i] == '--debug':
        result = cf.getContestList(top=5)
        print(result)
