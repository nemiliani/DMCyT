import pandas
import scipy
import argparse
import scipy.cluster.hierarchy as sch
import scipy.spatial.distance as sdm
import pylab

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='Hierarchic clustering app')
    parser.add_argument('-f', '--data_file', type=str, help='data file')
    parser.add_argument('-d', '--dendrogram_file', type=str, help='dendrogram png file name')
    parser.add_argument('-c', '--columns', nargs='+', type=str)
    args = parser.parse_args()

    df = pandas.read_csv(args.data_file, header=0)
    #['RA_J2000','DE_J2000','dist']
    data = df.as_matrix(columns=args.columns)
    distance_matrix = sdm.pdist(data)
    y = sch.linkage(distance_matrix, method='average')

    pylab.figure()
    sch.dendrogram(y)
    pylab.savefig(args.dendrogram_file)
