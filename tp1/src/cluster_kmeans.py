import pandas
import argparse
import matplotlib.pyplot as plt
import numpy as np

import sklearn.cluster as skc
from sklearn import metrics
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA

from time import time


def bench_k_means(estimator, name, data):
    t0 = time()
    estimator.fit(data)
    print 'Name             : %s'  % name 
    print 'Time             : %.2fs' % (time() - t0)
    print 'Inhertia         : %i' % estimator.inertia_
    print 'total silhouette : %.3f' % \
            metrics.silhouette_score(data, estimator.labels_,
                                      metric='euclidean',
                                      sample_size=len(data))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Hierarchic clustering app')
    parser.add_argument('-f', '--data_file', type=str, help='data file')
    parser.add_argument('-p', '--scatter_file', type=str, 
                                help='output png file name for cluster scatter')
    parser.add_argument('-s', '--silhouette_file', type=str, default='sil.png',
                                help='output png file name for silhouette hists')
    parser.add_argument('-v', '--sil_vs_cluster', type=str, default=None,
                                help='output png file name for silhouette vs cluster')
    parser.add_argument('-k', '--n_clusters', type=int, help='number of clusters')
    parser.add_argument('-j', '--n_jobs', type=int, help='number of jobs for parallelization')
    parser.add_argument('-r', '--random_state', type=int, 
                                          help='the generator used to initialize the centers')
    parser.add_argument('-i', '--init', type=str, choices=['k-means++', 'random'], 
                          default='random', help='initialization method')
    parser.add_argument('-c', '--columns', nargs='+', type=str)
    parser.add_argument('-o', '--output_file', type=str, default='out.csv')
    parser.add_argument('-m', '--cluster_metrics_file', type=str, default='cluster_metrics.csv')
    args = parser.parse_args()

    df = pandas.read_csv(args.data_file, header=0)
    non_scaled_data = df.as_matrix(columns=args.columns)
    data = scale(non_scaled_data)
    km = skc.KMeans(n_clusters=args.n_clusters, 
               init=args.init,
               n_jobs=args.n_jobs,
               random_state=args.random_state)
    bench_k_means(km, 'kmeans', data)

    # which cluster has more hyades stars ?
    y = km.predict(data)
    # add to the data frame a cluster column
    df['cluster'] = y
    # add to the data frame a silhouette column
    df['silhouette'] = metrics.silhouette_samples(
                        data, 
                        km.labels_,
                        metric='euclidean')
    sdf = df.sort(['cluster','is_hyades'], ascending=[1, 1])
    sdf.to_csv(args.output_file)
    # lets print hyades amount
    print ''
    print '------------------------------------'
    with open(args.cluster_metrics_file, 'w') as f:
        f.write('cluster,total samples,total hyades,hyades density,silh. mean,silh. max,' \
                'silh. min, silh. median\n')
        for i in range(args.n_clusters):
            tdf = sdf[sdf.loc[:, 'cluster'] == i]
            hyades_count = len(tdf[tdf.loc[:,'is_hyades'] == 1])
            # get silohutte per cluster
            line = '%d,%d,%d,%.2f,%.5f,%.5f,%.5f,%.5f\n' % (
                    i, len(tdf), hyades_count, (float(hyades_count) / len(tdf)), 
                    tdf['silhouette'].mean(), tdf['silhouette'].max(), 
                    tdf['silhouette'].min(), tdf['silhouette'].median())
            f.write(line)
            plt.subplot(args.n_clusters, 1, i)
            plt.hist(list(tdf['silhouette']), normed=0,
                        histtype='bar', rwidth=0.5, orientation='horizontal')
            plt.ylabel('sil. clus. %d' % i)
        plt.savefig(args.silhouette_file, dpi=1000)

    #visualize it
    reduced_data = PCA(n_components=2).fit_transform(data)
    kmeans = skc.KMeans(n_clusters=args.n_clusters, 
               init=args.init,
               n_jobs=args.n_jobs,
               random_state=args.random_state)
    kmeans.fit(reduced_data)

    # Step size of the mesh. Decrease to increase the quality of the VQ.
    h = 1     # point in the mesh [x_min, m_max]x[y_min, y_max].

    # Plot the decision boundary. For that, we will assign a color to each
    x_min, x_max = reduced_data[:, 0].min() + 1, reduced_data[:, 0].max() - 1
    y_min, y_max = reduced_data[:, 1].min() + 1, reduced_data[:, 1].max() - 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    # Obtain labels for each point in mesh. Use last trained model.
    Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure(1)
    plt.clf()
    plt.imshow(Z, interpolation='nearest',
               extent=(xx.min(), xx.max(), yy.min(), yy.max()),
               cmap=plt.cm.Paired,
               aspect='auto', origin='lower')

    plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
    # Plot the centroids as a white X
    centroids = kmeans.cluster_centers_
    plt.scatter(centroids[:, 0], centroids[:, 1],
                marker='x', s=169, linewidths=3,
                color='w', zorder=10)
    plt.title('K-means clustering on the digits dataset (PCA-reduced data)\n'
              'Centroids are marked with white cross')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xticks(())
    plt.yticks(())
    plt.savefig(args.scatter_file)
    plt.close()

    if args.sil_vs_cluster :
        plt.figure(2)
        s = []
        k = range(2,20)
        for i in k:
            print '.', 
            kmeans_model = skc.KMeans(n_clusters=i, 
                   init=args.init,
                   n_jobs=args.n_jobs,
                   random_state=args.random_state).fit(data)
            s.append(metrics.silhouette_score(
                    data,  kmeans_model.labels_, metric='euclidean'))
        print ''
        plt.plot(k, s)
        plt.ylabel("Total Sihlouette score")
        plt.xlabel("Number of clusters clusters")
        plt.savefig(args.sil_vs_cluster)
        plt.close()
