import datetime


def dateTransform(data):
    temp = datetime.datetime.strftime(data, '%Y-%m-%d')
    return datetime.datetime.strptime(temp, '%Y-%m-%d').date()
