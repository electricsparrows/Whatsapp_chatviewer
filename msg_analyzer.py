# import nltk
# from nltk.corpus import stopwords
import numpy as np
from datetime import datetime as dt
import pandas as pd
import scipy
import seaborn as sbn
import db
import matplotlib.pyplot as plt

msg1 = "i witnessed ur situation and saw nothing except trembling"

msg2 = "I don't think so. Don't think it's doable"

stop_words = {"u", "do", "i", "ur", "and"}

# probably split into sentences first
# word_tokens = nltk.word_tokenize(msg1)
# filtered = [w for w in word_tokens if not w in stop_words]
# tagged = nltk.pos_tag(filtered)



def get_nouns(tagged_list):
    noun_tags = ['NN', 'NNS', 'NNP', 'NNPS']
    return [w for w in tagged_list if w[1] in noun_tags]


# set of functions which take a list of message records --> returns some sort of visualization
# - noun set cloud
# - activity over time of day (probably takes date as an input)


# tokenizer: string --> list of tokens

# part of Speech tagger: list of tokens --> list of two-tuples

# get noun set

# get verb set

def get_unigrams(text):
    return text.split()


def get_bigrams(text):
    bag = get_unigrams(text)
    res = []
    # pop off the first two and append
    while len(bag) != 0:
        if len(bag) > 1:
            res.append(" ".join(bag[:2]))
            bag.pop(0)
            bag.pop(0)
        else:
            res.append(bag.pop())
    return res


def gen_activity_chart(year):
    cal_data = db.get_message_count_by_dateyear(year)
    # convert date column into datetime objects and extracts DoW and week_num as columns --
    cal_data = np.array([[*fetch_dow_and_week_num(dt.strptime(k,"%Y-%m-%d")), v] for k,v in cal_data.items()])
    df = pd.DataFrame(cal_data, columns =["DoW", "Week_num", "message_count"])
    ptable = df.pivot("DoW", "Week_num", "message_count").fillna(0)       # replace NaN with 0
    sbn.set(rc={"figure.figsize": (30, 10)})                              # w= 30, h=10
    ax = sbn.heatmap(ptable, cmap="Reds", robust=True,
                     yticklabels=["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"],
                     linewidths=1)
    return ax


def fetch_dow_and_week_num(datetime_obj):
    days_of_week = {"Sunday": 1, "Monday": 2, "Tuesday": 3, "Wednesday": 4,
                    "Thursday": 5, "Friday": 6, "Saturday": 7}
    day = days_of_week[datetime_obj.strftime("%A")]
    week_num = int(datetime_obj.strftime("%U"))      # week starting sunday
    return day, week_num


def main():
    gen_activity_chart(2017)
    plt.show()


if __name__ == "__main__":
    main()