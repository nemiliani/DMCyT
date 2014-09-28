import pandas
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='sorts symbad catalog by match distance and returns the first %% of registers')
    parser.add_argument('-p', '--percent', type=int, default=20, help='percent to be returned')
    parser.add_argument('-f', '--file', type=str, default='symbad_augmented.csv', help='symbad catalog file')
    parser.add_argument('-o', '--output', type=str, default='symbad_sublist.csv', help='output symbad catalog file')
    args = parser.parse_args()

    # get the list
    df = pandas.DataFrame.from_csv(args.file)
    # sort it by distance    
    df_sort = df.sort(['dist'],ascending=[1])
    max_dist = df_sort[['dist']].max()
    min_dist = df_sort[['dist']].min()
    print 'Min distance : %f' % min_dist    
    print 'Max distance : %f' % max_dist
    percent = [i for i in range(0, len(df_sort), int(len(df_sort) * .2))]
    percent[len(percent)-1] = len(df_sort) - 1
    percent = percent[1:]
    i = 20
    for p in percent:
        print '%d%% is under %f' % (i, df_sort.iloc[p]['dist'])
        i = i + 20

    df_p = df_sort.iloc[0:int(len(df_sort) * (args.percent / 100.0)),:]
    df_p.to_csv(args.output)
