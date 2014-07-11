import cfclass
import sys
import os
import datetime
import re



def to_int(name, value):
    try:
        return int(value)
    except ValueError:
        print(name + ' = ' + str(value) + ' must be integer')
        sys.exit(0)


def is_color(value):
    p = re.compile(r'[0-9a-f]{6}')
    return p.match(value)


# main object of CodeForces API
cf = cfclass.CodeForces()

# parameters
top = -1
hr = False
colors = False
division = 'all'
handles = []
special_chars = [
    {'from': '$', 'to': '\$'},
    {'from': '#', 'to': '\#'},
    {'from': '\n', 'to': ' '},
    {'from': '\r', 'to': ' '}
]
contest_color_names = [
    'BEFORE',
    'RUNNING',
    'PENDING_SYSTEM_TEST',
    'SYSTEM_TEST',
    'FINISHED'
]
contest_colors = {
    'BEFORE': '${color #ffa200}',
    'RUNNING': '${color #ffee59}',
    'PENDING_SYSTEM_TEST': '${color #ffee59}',
    'SYSTEM_TEST': '${color #ffee59}',
    'FINISHED': '${color #daff5c}'
}
submission_colors = {
    'AC': '${color 02af1b}',
    'WA': '${color a9100f}',
    'NO': '${color}'

}
argc = len(sys.argv)
for i in range(1, argc):
    param = sys.argv[i]
    value = None
    if i < argc - 1:
        value = sys.argv[i + 1]

    if param == '--top' and value:
        top = to_int('--top', value)

    if param == '--hr':
        hr = True

    if param == '--colors':
        colors = True

    if param == '--div1':
        division = 'div1'
    if param == '--div2':
        division = 'div2'

    if param == '--handles':
        handles = value.split(',')

    if param == '--contest-colors':
        if not value:
            continue
        value_list = value.split(',')
        for i in range(0, min(len(contest_color_names), len(value_list))):
            if not value_list[i] or not is_color(value_list[i]):
                continue
            contest_colors[contest_color_names[i]] = '${color #%s}' % (value_list[i])


# select main response function
for i in range(1, len(sys.argv)):
    param = sys.argv[i]
    value = None
    if i < argc - 1:
        value = sys.argv[i + 1]

    if param == '--next-contest-list':
        result = cf.getContestList()
        for contest in result:
            if contest['phase'] != 'BEFORE':
                continue

            if division == 'div1' and contest['name'].find('Div. 2') != -1:
                continue
            if division == 'div2' and contest['name'].find('Div. 1') != -1:
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

    if param == '--contest-list':
        result = cf.getContestList(top=top)
        for contest in result:
            if division == 'div1' and contest['name'].find('Div. 2') != -1:
                continue
            if division == 'div2' and contest['name'].find('Div. 1') != -1:
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

    if param == '--user-info' and value:
        handles = value
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

    if param == '--current-standings':
        result = cf.getContestList(top=4)
        if not handles:
            continue
        for contest in result:
            if contest['phase'] != 'RUNNING':
                continue

            if division == 'div1' and contest['name'].find('Div. 2') != -1:
                continue
            if division == 'div2' and contest['name'].find('Div. 1') != -1:
                continue

            # filter special characters
            for char in special_chars:
                contest['name'] = contest['name'].replace(char['from'], char['to'])

            standings = cf.getContestStandings(contestId=contest['id'], handles=handles)
            if not standings:
                continue
            if len(standings['rows']) == 0:
                continue

            # show title of contest
            if colors:
                line = '%d %s%s $color' % (contest['id'], contest_colors[contest['phase']], contest['name'])
            else:
                line = '%d %s' % (contest['id'], contest['name'])
            print(line)

            # calculate max handle len for align
            user_len = 0
            for row in standings['rows']:
                prefix = '%d %s' % (row['rank'], row['party']['members'][0]['handle'])
                user_len = max(user_len, len(prefix))
            user_len += 1

            # problems list
            line = ' ' * user_len
            for problem in standings['problems']:
                line += ' %s ' % (problem['index'])
            print(line)

            # lines with handles
            for row in standings['rows']:
                prefix = '%d %s' % (row['rank'], row['party']['members'][0]['handle'])
                line = prefix + ' ' * (user_len - len(prefix))
                if colors:
                    line = '${color}' + line
                for cell in row['problemResults']:
                    # cell content with sign & attempts
                    cell_str = ''
                    # color len in text for align
                    cell_color_len = 0
                    # if accepted
                    if cell['points'] == 0.0:
                        # show sign if attempts > 1
                        if cell['rejectedAttemptCount'] > 0:
                            if colors:
                                cell_str += submission_colors['WA']
                                cell_color_len = len(submission_colors['WA'])
                            cell_str += '-' + str(cell['rejectedAttemptCount'])
                        else:
                            if colors:
                                cell_str += submission_colors['NO']
                                cell_color_len = len(submission_colors['NO'])
                            cell_str += ' .'
                    # wa or no submissions
                    else:
                        if colors:
                            cell_str += submission_colors['AC']
                            cell_color_len = len(submission_colors['AC'])
                        # show sign if attempts > 1
                        if cell['rejectedAttemptCount'] > 0:
                            cell_str += '+' + str(cell['rejectedAttemptCount'])
                        else:
                            cell_str += ' +'
                    cell_str += (cell_color_len + 3 - len(cell_str)) * ' '
                    line += cell_str
                print(line)

            if hr:
                print('$color$hr')

    # debug default method
    if param == '--debug':
        result = cf.getContestStandings(374)
        print(result)
