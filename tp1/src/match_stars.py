import settings
import pandas
import numpy
import os
import itertools
import math
import matplotlib.pyplot as plt
import pickle

class SpaceGrid(object):
   
    def __init__(self, hipparcos, symbad, intervals):
        self.hipparcos = hipparcos
        self.symbad = symbad
        self.ra_min = min(hipparcos['RA_J2000'])
        self.ra_max = max(hipparcos['RA_J2000'])
        self.de_min = min(hipparcos['DE_J2000'])
        self.de_max = max(hipparcos['DE_J2000'])
        self.intervals = intervals
        self.ra_dif = self.ra_max - self.ra_min
        self.de_dif = self.de_max - self.de_min
        self.ra_sp = self.ra_dif/(self.intervals-1)
        self.de_sp = self.de_dif/(self.intervals-1)
        
        # set the position at the space grid for hipparcos catalog
        self.stars = pandas.DataFrame(
                   numpy.zeros((len(self.hipparcos),2)), columns=['rec','dec'])
        self.stars['rec'] = numpy.floor(
            (self.hipparcos['RA_J2000'] - self.ra_min) / self.ra_sp) + 1
        self.stars['dec'] = numpy.floor(
            (self.hipparcos['DE_J2000'] - self.de_min) / self.de_sp) + 1
        
        # set the position at the space grid for symbad catalog
        self.symbad['rac'] = numpy.floor(
            (self.symbad['RA_J2000'] - self.ra_min) / self.ra_sp) + 1
        self.symbad['dec'] = numpy.floor(
            (self.symbad['DE_J2000'] - self.de_min) / self.de_sp) + 1
    
    @classmethod
    def expand_grid(cls, data_dict):
        rows = itertools.product(*data_dict.values())
        return pandas.DataFrame.from_records(rows, columns=data_dict.keys())


    def get_neighbours(self, star_rac, star_dec):
        '''
            get the closest stars to a symbad star
        '''
        vecx = numpy.array([-1,0,1])
        vecy = numpy.array([-1,0,1])
        exstar = int(star_rac)
        eystar = int(star_dec)
#        print 'x axis slots'
#        print exstar
#        print 'y axis slots'
#        print eystar
        xstar_vec = pandas.DataFrame((exstar + vecx))[exstar + vecx > 0]
        ystar_vec = pandas.DataFrame((eystar + vecy))[eystar + vecy > 0]
#        print list(xstar_vec.get(0))
#        print list(ystar_vec.get(0))
        star_vec = SpaceGrid.expand_grid({'rec': list(xstar_vec.get(0)), 'dec': list(ystar_vec.get(0))})
#        print 'grid x,y combination :'        
#        print star_vec        
        # extract a df with the stars in the query zone
        neighbours = self.hipparcos[
                (self.stars['rec'] == star_vec['rec'][0]) & 
                (self.stars['dec'] == star_vec['dec'][0])]
        for i in range(1, len(star_vec)):
            neighbours = neighbours.append(
                self.hipparcos[
                (self.stars['rec'] == star_vec['rec'][i]) & 
                (self.stars['dec'] == star_vec['dec'][i])])
        return neighbours

    def get_closest(self, star_rac, star_dec, neighbours):
        mindist = math.sqrt(
                        numpy.sum(
                            numpy.power(numpy.array([star_rac, star_dec]) - 
                                numpy.array([neighbours.iloc[0]['RA_J2000'], neighbours.iloc[0]['DE_J2000']]), 2)
                        ))
        closest = neighbours.iloc[0]
        for i in range(1, len(neighbours)):
            nvd = math.sqrt(
                        numpy.sum(
                            numpy.power(numpy.array([star_rac, star_dec]) - 
                                numpy.array([neighbours.iloc[i]['RA_J2000'], neighbours.iloc[i]['DE_J2000']]), 2)
                        ))
            if nvd < mindist :
                mindist = nvd
                closest = neighbours.iloc[i]        
        return { 'closest' : closest, 'mindist' : mindist}


if __name__=='__main__':

    # read all csv files
    symbad = pandas.read_csv(
        os.path.join(settings.DATA_PATH, 'symbad.csv'), header=0)
    hipparcos = pandas.read_csv(
        os.path.join(settings.DATA_PATH, 'hipparcos.csv'), header=0)
    sym2hip = pandas.read_csv(
        os.path.join(settings.DATA_PATH, 'sym2hip.csv'), header=0)
    
    # remove trailing space from ids
    symbad['identifier'] = symbad.apply(
                lambda x : x.get('identifier').strip(), axis=1)

    symbad['idHip'] = symbad.apply(
        lambda x : x.get('identifier') if x.get('identifier') in list(sym2hip['HD']) else None, axis=1)

    # create the space grid
    sg = SpaceGrid(hipparcos, symbad, intervals=50)
    symbad_dists = []
    symbad_closest = pandas.DataFrame(columns=['HIP', 'RA_J2000', 'DE_J2000', 'Plx', 
                                                    'pmRA', 'pmDE', 'Vmag', 'B_V'])
    for i in range(0, len(symbad)):
        neighbours = sg.get_neighbours(symbad['rac'][i], symbad['dec'][i])
        closest = sg.get_closest(symbad['RA_J2000'][i], symbad['DE_J2000'][i], neighbours)
        symbad_dists.append(closest['mindist'])
        symbad_closest.loc[i] = closest['closest']

    symbad_augmented = pandas.DataFrame(data=sg.symbad)
    symbad_augmented['dist'] = symbad_dists
    symbad_augmented['cercanaHip'] = symbad_closest['HIP']
    sym_no_dups = symbad_augmented.sort(columns='dist', axis=0).drop_duplicates(subset='cercanaHip')
    sym_no_dups.to_csv('symbad_augmented.csv')

    plt.figure()
    plt.hist(list(sym_no_dups['dist']), normed=0, histtype='bar', rwidth=0.8)
    plt.savefig('distance_dstribution.png')
