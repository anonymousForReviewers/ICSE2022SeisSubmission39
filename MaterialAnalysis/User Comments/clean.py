import pandas as pd
import sys, os
import numpy as np

def clean_updates():
    src_df = pd.read_excel('./apps.xlsx')
    src_df = src_df[src_df.legal != 0]
    app_names = src_df['软件名']
    updates = os.listdir('./updates_raw')
    for name in app_names:
        files = [file for file in updates if name + '.' in file]
        if len(files) != 1:
            print('wow', name)
        df = pd.read_excel('./updates_raw/' + files[0], header = None) 
        df = pd.DataFrame(np.array(df[0]).reshape(len(df[0]) // 4, 4), columns = ['Version', 'Date', 'App', 'Val']) 
        df.to_excel('./updates/' + files[0], index = False)
    app_names_new = src_df['Option']
    for name in app_names_new:
        if type(name) != str:
            continue
        files = [file for file in updates if name + '.' in file]
        if len(files) != 1:
            print('wow', name)
        df = pd.read_excel('./updates_raw/' + files[0], header = None) 
        df = pd.DataFrame(np.array(df[0]).reshape(len(df[0]) // 4, 4), columns = ['Version', 'Date', 'App', 'Val']) 
        df.to_excel('./updates/' + files[0], index = False)



def clean_comments():
    s_left, s_right = ['华为', 'VIVO', 'OPPO'], ['小米', '魅族']
    src_df = pd.read_excel('./apps.xlsx')
    src_df = src_df[src_df.legal != 0]
    app_names = src_df['软件名']

    c_left, c_right = os.listdir('./comments_raw_1'), os.listdir('./comments_raw_2')
    for name in app_names:
        # if name != '搜狗搜索':
        #     continue
        new_df = pd.DataFrame({'Src': [], 'Time' : [], 'Rank' : [], 'Adaptation' : [], 'Val' : []})
        files = [file for file in c_left if name + '_' in file or name + '大字版_' in file or name + '亲情版_' in file]
        if len(files) == 0:
            print('wow', name)
        for s_name in s_left:
            for file in files:
                # print(file, s_name)
                try:
                    df = pd.read_excel('./comments_raw_1/' + file, sheet_name = s_name, header = None)    
                except:
                    print('wow', file, s_name)
                    continue
                print('success', file, s_name)
                df = df.drop([0, 1])     
                df[1] = s_name
                df = df.rename(columns={0: 'Time', 1: 'Src', 2: 'Rank', 3: 'Val', 4: 'Adaptation'})   
                # print(df)  
                if '大字版_' in file or '亲情版_' in file:
                    df['Adaptation'] = 1
                else:
                    df['Adaptation'] = 0
                new_df = new_df.append(df, ignore_index = True)     
        files = [file for file in c_right if name + '_' in file or name + '大字版_' in file]
        if len(files) == 0:
            print('wow', name)
        for s_name in s_right:
            for file in files:
                # print(file, s_name)
                try:
                    df = pd.read_excel('./comments_raw_2/' + file, sheet_name = s_name, header = None)    
                except:
                    print('wow', file, s_name)
                    continue
                print('success', file, s_name)
                df = df.drop([0, 1])     
                df[1] = s_name
                df = df.rename(columns={0: 'Time', 1: 'Src', 2: 'Rank', 3: 'Val', 4: 'Adaptation'})   
                # print(df)    
                if '大字版_' in file or '亲情版_' in file:
                    df['Adaptation'] = 1
                else:
                    df['Adaptation'] = 0
                new_df = new_df.append(df, ignore_index = True)     

        new_df.to_csv('./comments/' + name + '.csv', index = False)
        # print(new_df)
        # return 

if __name__ == '__main__':
    clean_comments()
    # clean_updates()
