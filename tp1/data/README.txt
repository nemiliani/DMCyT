JERARQUICO SOBRE SYMBAD 
-----------------------

tratando de hacer algo loco que me indique que tipos de 
distancias hay, como un histograma. Pinto!

* Empese por un cluster jerarquico para poder estimar con k
conviene empesar, un numero logico parece ser 5 mas menos 1.

$ python cluster_hierarchical.py -f symbad_augmented.csv -d dendro_only_dist_avg.png -c dist

* Tambien hice uno ageragado las columnas de recta y declinacion
pero no se ve de forma tan clara el K a usar

$ python cluster_hierarchical.py -f symbad_augmented.csv -d dendro_all_cols_avg.png -c dist RA_J2000 DE_J2000

* Tambien hice uno solo con las columnas de recta y declicnacion
pero no se ve de forma tan clara el K a usar

$ python cluster_hierarchical.py -f symbad_augmented.csv -d dendro_ra_de_avg.png -c RA_J2000 DE_J2000


JERARQUICO SOBRE HIPPARCOS
--------------------------

Hice el jerarquico sobre hipparcos, parece ser que entre 4 y 7
esta el numero logico de culsters

$ python cluster_hierarchical.py -f ../data/hipparcos.csv -d dendro_hip_ra-de.png -c RA_J2000 DE_J2000

K-MEANS
-------

Usando K = 5 verificar que silohuette no cambia al elegir de forma random:

$ python cluster_kmeans.py -f ../data/hipparcos.csv -p plot.png -k 5 -j 6 -r 0 -i random -c RA_J2000 DE_J2000 Plx pmRA pmDE Vmag B-V
Name        : kmeans
Time        : 0.26s
Inhertia    : 8438540
silhouette  : 0.645

$ python cluster_kmeans.py -f ../data/hipparcos.csv -p plot.png -k 5 -j 6 -r 42 -i random -c RA_J2000 DE_J2000 Plx pmRA pmDE Vmag B-V
Name        : kmeans
Time        : 0.26s
Inhertia    : 8438540
silhouette  : 0.645

$ python cluster_kmeans.py -f ../data/hipparcos.csv -p plot.png -k 5 -j 6 -r 85562 -i random -c RA_J2000 DE_J2000 Plx pmRA pmDE Vmag B-V
Name        : kmeans
Time        : 0.16s
Inhertia    : 8438945
silhouette  : 0.644

--> Parece ser estable



---------------------
corro script.sh en base a :

hipparcos_silhouette.png
hipparcos_metrics.csv

me quedo con el cluster 1 menos las que ya marcamos como hyades para proponer
esto se hace a manopla con el excel ordenando por cluster y is_hyades

y queda en data/hipparcos.candidates.csv

Esta lista se le resta a tycho y se genera

y queda en data/tycho.no.hipparcos.candidates.csv

usando remove_from_tycho

Luego hice kmeans usando este ultimo data/tycho.no.hipparcos.candidates.csv

python cluster_kmeans.py -f ../data/tycho.no.hipparcos.candidates.csv -p run/graphs/tycho_scatter.png -k 6 -j 6 -r 85562 -i random -c RA_J2000_24 DE_J2000 pmRA pmDE BT VT V B-V -o run/tycho.kmeans.csv -s run/graphs/tycho_silhouette.png -m run/tycho_metrics.csv

y usando :

run/graphs/tycho_silhouette.png
run/tycho_metrics.csv

me quedo con el cluster 3

menos las que ya marcamos como hyades para proponer
esto se hace a manopla con el excel ordenando por cluster y is_hyades

y queda en data/tycho.candidates.csv
