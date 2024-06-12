from db import getdata
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt


def gen_datetime_range(y, m, d):
    start = dt.datetime(y, m, d, 0, 0)
    end = dt.datetime(y, m, d, 23, 59)
    dates = [dt.datetime.strftime(start + dt.timedelta(seconds=60*i), "%H:%M") for i in range(1439)]
    return dates


def get_values(y, m, d):
    # generate all HH:MM ticks in a 24 period
    ticks = gen_datetime_range(y, m, d)
    occurrences = getdata(y, m, d)
    out = {}
    for tick in ticks:
        out[tick] = 0
        for t in occurrences:
            if t == tick:
                out[tick] += 1
    return out


def get_dataframe(y, m, d):
    data = get_values(y, m, d)
    values = [x for x in data.values()]
    df = pd.DataFrame(values, columns=['values'])
    dates = [dt.datetime(y,m,d) + dt.timedelta(seconds=60 * i) for i in range(1439)]
    df['ticks'] = dates
    return df


def gen_plot():
    pass


if __name__ == "__main__":
    df = get_dataframe(2020, 12, 17)
    #print(df)
    # plt.figure(figsize=(60, 10))

    sns.set(rc={"figure.figsize": (15, 5)})
    fig = plt.figure()
    fig.suptitle('Timestamp bunching - 2016/03/13 from testfile01.txt', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax = sns.scatterplot(data=df, x=df['ticks'], y=df['values'])
    ax.set(xlabel = 'Time', ylabel = 'msg_count')
    xtlabels = ['00:00', '02:00', '04:00', '06:00', '08:00', '10:00', '12:00',
                '14:00', '16:00', '18:00', '20:00', '22:00', '23:59']
    ax.set_xticklabels(xtlabels)
    plt.show()