import matplotlib.pyplot as plt
from wordcloud import WordCloud
import math
import numpy as np
import random

def plot_NMF(model, feature_names, n_top_words, title, environment, analysis):
    
    fig, axes = plt.subplots(2, 4, figsize=(30, 15), sharex=True)
    axes = axes.flatten()
    for topic_idx, topic in enumerate(model.components_):
        top_features_ind = topic.argsort()[-n_top_words -1:-1]
        top_features = [feature_names[i] for i in top_features_ind]
        weights = topic[top_features_ind]

        ax = axes[topic_idx]
        ax.barh(top_features, weights, height=0.7, edgecolor = '#000000', color = '#808080')
        ax.set_title(f"Cluster {topic_idx +1}", fontdict={"fontsize": 25})
        ax.invert_yaxis()
        ax.tick_params(axis="both", which="major", labelsize=20)
        for i in "top right left".split():
            ax.spines[i].set_visible(False)
        fig.suptitle(title, fontsize=40)
        

    plt.subplots_adjust(top=0.90, bottom=0.05, wspace=0.90, hspace=0.3)
    fig.savefig(f'./images/key_{environment}_{analysis}.jpg', bbox_inches='tight', dpi=150)
    plt.show()
    
#https://github.com/derekgreene/topic-model-tutorial/blob/master/3%20-%20Parameter%20Selection%20for%20NMF.ipynb
def plot_wordcloud(model, feature_names, n_top_words, title, environment, analysis):

    fig, axes = plt.subplots(2, 4, figsize=(60, 30), sharex=True)
    axes = axes.flatten()

    for topic_idx, topic in enumerate(model.components_):
        top_features_ind = topic.argsort()[-n_top_words - 1:-1]
        top_features = [feature_names[i] for i in top_features_ind]
        weights = topic[top_features_ind]

        wordcloud_text = ' '.join([f'{word}:{weight}' for word, weight in zip(top_features, weights)])
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(wordcloud_text)

        ax = axes[topic_idx]
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.set_title(f"Cluster {topic_idx + 1}", fontdict={"fontsize": 25})
        ax.axis('off')

    fig.suptitle(title, fontsize=40)
    plt.subplots_adjust(top=0.9, bottom=0.05, wspace=0.9, hspace=0.3)
    fig.savefig(f'./images/cloud_{environment}_{analysis}.jpg', bbox_inches='tight', dpi=150)
    plt.show()