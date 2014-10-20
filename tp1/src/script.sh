#!/bin/bash
echo 'clean up ....'
# clean up
rm -rf test
mkdir -p test/graphs

# Start tagging starts considered as hya in tycho and hipparcos
echo 'tagging known hyades ...'
python mark_hyades.py -i ../data/hipparcos.no.nan.csv -s ../data/symbad_augmented.csv -o test/hipparcos.tag.csv
python mark_hyades.py -i ../data/tycho.csv -s ../data/symbad_augmented.csv -o test/tycho.tag.csv

# run hierarchical clusters
echo 'running hierarchical clustering ...'
python cluster_hierarchical.py -f ../data/hipparcos.no.nan.csv -d test/graphs/hipparcos_dendro_ra-de.png -c RA_J2000 DE_J2000
python cluster_hierarchical.py -f ../data/tycho.csv -d test/graphs/tycho_dendro_ra-de.png -c RA_J2000_24 DE_J2000
