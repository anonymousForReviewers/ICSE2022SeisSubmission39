import pandas as pd
import os, sys

key_word_strict = ['老年版', '老人版', '大字版', '亲情版']
key_word_loose = ['老年', '老人', '大字', '亲情']

def related(comment):
    global key_word_strict, key_word_loose
    if type(comment) != str:
        return False
    key_words = key_word_strict
    for word in key_words:
        if word in comment:
            return True
    return False

def extract_comments(appendix):
    names = os.listdir('./comments')
    new_df = pd.DataFrame({'App' : [], 'Src': [], 'Time' : [], 'Rank' : [], 'Adaptation': [], 'Val' : []})
    for name in names:
        if not name.endswith('.csv'):
            continue
        df = pd.read_csv('./comments/' + name)
        df['Old'] = df['Adaptation']
        df['Old'] = df['Old'] + df['Val'].apply(related)
        # print(df[df.Old == True])
        temp_df = df[df.Old > 0]
        temp_df = temp_df.drop('Old', axis = 1)
        temp_df['App'] = name[0:-4]
        new_df = new_df.append(temp_df)
    new_df.to_excel('./comments_related' + appendix + '.xlsx', index = False, encoding = 'utf-8')

if __name__ == '__main__':
    extract_comments('_strict')