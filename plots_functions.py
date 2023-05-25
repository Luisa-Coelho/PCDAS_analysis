import matplotlib.pyplot as plt
from wordcloud import WordCloud
import math

def plot_NMF(model, feature_names, n_top_words, title, environment, analysis):
    fig, axes = plt.subplots(2, 4, figsize=(30, 15), sharex=True)
    axes = axes.flatten()
    for topic_idx, topic in enumerate(model.components_):
        top_features_ind = topic.argsort()[-n_top_words -1:-1]
        top_features = [feature_names[i] for i in top_features_ind]
        weights = topic[top_features_ind]

        ax = axes[topic_idx]
        ax.barh(top_features, weights, height=0.7, edgecolor = '#000000', color = '#808080')
        ax.set_title(f"Cluster {topic_idx +1}", fontdict={"fontsize": 30})
        ax.invert_yaxis()
        ax.tick_params(axis="both", which="major", labelsize=20)
        for i in "top right left".split():
            ax.spines[i].set_visible(False)
        fig.suptitle(title, fontsize=40)
        

    plt.subplots_adjust(top=0.90, bottom=0.05, wspace=0.90, hspace=0.3)
    fig.savefig(f'./key_{environment}_{analysis}.jpg', bbox_inches='tight', dpi=150)
    plt.show()
    

def plot_wordcloud(model, n_plots, n_words_each, environment, analysis):
    
    if n_plots%2 != 0:
        n_plots = math.ceil(n_plots/2)
    fig, axes = plt.subplots(2, n_plots, figsize=(30, 15), sharex=True)
    axes = axes.flatten()
    for topic_idx, topic in enumerate(model.components_):
        top_features_ind = topic.argsort()[-n_words_each -1:-1]
        #top_features = [feature_names[i] for i in top_features_ind]
        weights = topic[top_features_ind]
        # lower max_font_size
       # wordcloud = WordCloud(max_font_size=40).generate(text)
       # plt.figure()
       # plt.imshow(wordcloud, interpolation="bilinear")
       # plt.axis("off")
                
    plt.subplots_adjust(top=0.90, bottom=0.05, wspace=0.90, hspace=0.3)
    fig.savefig(f'./key_{environment}_{analysis}.jpg', bbox_inches='tight', dpi=150)
    plt.show()