import sys

sys.path.insert(0, '..')



from scipy.stats import gaussian_kde
import pandas as pd

from preprocessing.create_sets import create_sets
import numpy as np
from tests.test_base_class import Test

try:
    stations_correlations= np.loadtxt('../data_files/test_properties/stations_correlations.csv')
except:
    print('station correlations file doesn´t exist')


class STCT(Test):
    
    pbounds = {'p0': (0., 1.)}
    
    def create_probability(self,target_station, df_name=None):   
        
        x1, f1= create_sets(self.station, df_name)
        x2, f2= create_sets(target_station, df_name)
        
        diff=[]
        
        for x in x1:
            diff.append(f2(x)-f1(x))
        return gaussian_kde(diff)

    def fit(self, thr=0.1):
        """
        Parameters
        ----------
            - station: station id from which to build the test
            - thr: score below which a station is labelled as outlier
            - df: dataframe used in the pdf computation
            
        Output
        -------
            - evaluate point: closure function that calculates the tests result
            - correlated stations: ID list of the stations used for the computation 
        """
        
        df= pd.read_pickle("/home/tobou/Desktop/Meteorological_Data_quality_assesment/df_gen/df_train.pkl")
        stations= df['station'].unique()[:]
        
        station_index= np.where(stations == self.station)[0][0]
        r_thr=1.
        
        correlated_stations=[]
    
        while(r_thr>0.9 and len(correlated_stations)<11):
            correlated_stations= stations[stations_correlations[station_index,:]>r_thr]

            r_thr-=1e-5
            
        correlated_stations=np.delete(correlated_stations, np.where(correlated_stations == self.station) )
        
        self.correlated_stations= dict.fromkeys(correlated_stations)
        
        for target_station in self.correlated_stations.keys():
            try:
                self.correlated_stations[target_station] = {
                    'pdf' : self.create_probability(target_station,'train'),
                    'f' : None,
                    'r': stations_correlations[np.where(stations == self.station)[0][0],np.where(stations == target_station)[0][0]]}
            except:
                pass
        self.sum_r= sum([aux['r'] for aux in self.correlated_stations.values() if aux])
        return

    def prepare_points(self, df_name):
        for target_station in self.correlated_stations.keys():
            try:
                self.correlated_stations[target_station]['f']= create_sets(target_station, df_name)[1]
            except:
                pass
        return   
    
    def evaluate(self, x, y, params):
        """
        Parameters
        ----------
            - (x,y): point coordinates in the time series of the station being analyzed
            - thr: score below which a station is labelled as outlier
  
        Output
        -------
            - Boolean: test result (True/False)
        """
        output_prob=0.
        for target_station in self.correlated_stations:
            #_, f2= create_sets(correlated_stations[i], df)

            diff=self.correlated_stations[target_station]['f'](x)-y

            try:
                output_prob+= self.correlated_stations[target_station]['pdf'].evaluate(diff)*self.correlated_stations[target_station]['r']
            except:
                pass
        output_prob/= self.sum_r
        
        # I DON'T KNOW IF THIS IS THE PROBABILITY THAT MAKES SENSE 
        
       # return output_prob
              
        if (output_prob<params['p0']):
            return True
        else:
            return False
        
        
"""
test= STCT(6096)
#%%
test.fit('train')
#test.build_pdfs('train')

#%%
test.optimize(1.5)
"""