import settings
import pandas
import numpy
import os
import itertools

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
        
        # set the position at the space grid for hiparcos and symbad catalog
        self.stars = pandas.DataFrame(
                   numpy.zeros((len(self.hipparcos),2)), columns=['rec','dec'])
        self.stars['rec'] = numpy.floor(
            (self.hipparcos['RA_J2000'] - self.ra_min) / self.ra_sp) + 1
        self.stars['dec'] = numpy.floor(
            (self.hipparcos['DE_J2000'] - self.de_min) / self.de_sp) + 1
        
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
        exstar = star_rac
        eystar = star_dec
        xstar_vec = pandas.DataFrame((exstar + vecx))[exstar + vecx > 0]
        ystar_vec = pandas.DataFrame((eystar + vecy))[eystar + vecy > 0]
        star_vec = SpaceGrid.expand_grid({'rec': xstar_vec, 'dec': ystar_vec})
        # extract a df with the stars in the query zone

if __name__=='__main__':

    # read all csv files
    symbad = pandas.read_csv(
        os.path.join(settings.DATA_PATH, 'symbad.csv'), header=0)
    hipparcos = pandas.read_csv(
        os.path.join(settings.DATA_PATH, 'hipparcos.csv'), header=0)
    sym2hip = pandas.read_csv(
        os.path.join(settings.DATA_PATH, 'sym2hip.csv'), header=0)
    
    # create the space grid
    sg = SpaceGrid(hipparcos, symbad, intervals=50)
    
    for i in range(0, len(symbad)):
        sg.get_neighbours(symbad['rac'][i], symbad['dec'][i])

