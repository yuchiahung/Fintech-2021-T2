from datetime import datetime, timedelta
import pandas as pd
from matplotlib import cm
from matplotlib.colors import ListedColormap
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np

def plot_wordcloud(data, n_words=100, date = None):
    """ Wordcloud of news of the week """
    if date:
        a_week_ago = date - timedelta(days=7)
        data['time'] = pd.to_datetime(data['time'], unit='ms')  
        data_week = data[data.time > a_week_ago]
        text = ' '.join(data_week['header'] + ' ' + data_week['content'])
    else: 
        text = ' '.join(data['header'] + ' ' + data['content'])
    # read stopwords
    with open('stopwords_en.txt') as f:
        stopwords = [line.rstrip() for line in f]
    # Generate color map
    oceanBig = cm.get_cmap('ocean', 512)
    newcmp = ListedColormap(oceanBig(np.linspace(0, 0.85, 256)))
    # Generate a word cloud image
    wordcloud = WordCloud(width=800, height=150, background_color='white', 
                          colormap=newcmp, stopwords=stopwords, max_words=n_words).generate(text)
    # Display the generated image
    fig = plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    return fig