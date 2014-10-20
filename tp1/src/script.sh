#!/bin/bash
echo 'clean up ....'
# clean up
rm -rf run
mkdir -p run/graphs

echo 'matching stars ....'
# match the starts from symbad against hipparcos
python match_stars.py
mv symbad_augmented.csv run/match_hyades.csv
mv distance_dstribution.png run/graphs
# apply the cut
echo 'we keep the first 88 percent ...'
python get_sublist.py -f run/match_hyades.csv -p 88 -o run/match_88.percent.csv
echo 'run/match_88.percent.csv'

# start tagging starts considered as hya in tycho and hipparcos
echo 'tagging known hyades ...'
python mark_hyades.py -i ../data/hipparcos.no.nan.csv -s run/match_88.percent.csv -o run/hipparcos.tag.csv
python mark_hyades.py -i ../data/tycho.csv -s run/match_88.percent.csv -o run/tycho.tag.csv

# run hierarchical clusters
echo 'running hierarchical clustering on hipparcos'
python cluster_hierarchical.py -f ../data/hipparcos.no.nan.csv -d run/graphs/hipparcos_dendro_ra-de.png -c RA_J2000 DE_J2000
echo 'running hierarchical clustering on tycho'
# XXX : uncomment
#python cluster_hierarchical.py -f ../data/tycho.csv -d run/graphs/tycho_dendro_ra-de.png -c RA_J2000_24 DE_J2000

# run kmean clusters
echo 'running Kmeans clustering on hipparcos, k = 4'
python cluster_kmeans.py -f run/hipparcos.tag.csv -p run/graphs/hipparcos_scatter.png -k 4 -j 6 -r 85562 -i random -c RA_J2000 DE_J2000 Plx pmRA pmDE Vmag B-V -o run/hipparcos.kmeans.csv -s run/graphs/hipparcos_silhouette.png -m run/hipparcos_metrics.csv -v run/graphs/tycho_sil_vs_cluster.png

echo 'based on your analysis provide a hipparcos based candidate list using run/hipparcos.kmeans.csv'


#echo 'running Kmeans clustering on tycho, k = 4'
python cluster_kmeans.py -f ../data/tycho.no.hipparcos.candidates.csv -p run/graphs/tycho_scatter.png -k 4 -j 6 -r 85562 -i random -c RA_J2000_24 DE_J2000 pmRA pmDE BT VT V B-V -o run/tycho.kmeans.csv -s run/graphs/tycho_silhouette.png -m run/tycho_metrics.csv #-v run/graphs/tycho_sil_vs_cluster.png
