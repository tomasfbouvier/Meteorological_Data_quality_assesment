import sys

sys.path.insert(0, '..')



from scipy.stats import gaussian_kde
import pandas as pd

from preprocessing.create_sets import create_sets
import numpy as np
from tests.test_base_class import Test

try:
    stations_correlations= pd.read_csv('../data_files/stations_correlations.csv')
except:
    print('station correlations file doesn´t exist')


class STCT(Test):
    
    
    #pbounds={}
    
    to_save=['confusion_matrix', 'params', 'correlated_stations','sum_r','tuning_status', 'acc', 'acc_train']
    def create_probability(self,target_station, df_name=None):   
        
        x1, f1= create_sets(self.station, df_name)
        x2, f2= create_sets(target_station, df_name)
        
        diff=[]
        
        for x in x1:
            diff.append(abs(f2(x)-f1(x)))
        return gaussian_kde(diff)

    def fit(self, thr=0.1):
        """
        Parametersx)
            
        ----------
            - station: station id from which to build the test
            - thr: score below which a station is labelled as outlier
            - df: dataframe used in the pdf computation
            
        Output
        -------
            - evaluate point: closure function that calculates the tests result
            - correlated staj mahalttions: ID list of the stations used for the computation 
        """
        
        #df= pd.read_pickle("/home/tobou/Desktop/Meteorological_Data_quality_assesment/df_gen/df_train.presspkl")
        #stations= df['station'].unique()[:]
        self.pbounds = {'p0': (-1., 1.)}
        #print(self.pbounds)
        r_thr=1.

        correlated_stations=[]
        
        i=0
        while(len(correlated_stations)<6):
            correlated_stations= stations_correlations[stations_correlations['station1']==self.station][stations_correlations['r']>=r_thr]['station2'].to_list()
            
            r_thr-=1e-4
            i+=1
            if(i>1000):
            #print(r_thr)
            #if( len(correlated_stations)>8):
                break


        
        correlated_stations.remove(self.station)
        
        self.correlated_stations= dict.fromkeys(correlated_stations)
        
        for target_station in self.correlated_stations.keys():
            try:
                
                self.correlated_stations[target_station] = {
                    'pdf' : self.create_probability(target_station,'train'),
                    'f' : None,
                    'r': stations_correlations[stations_correlations['station1']==self.station][stations_correlations['station2']==target_station]['r'].values[0]}
                self.pbounds[str(target_station)]=(-1., 1.)
            except:
                self.correlated_stations[target_station] = None
                pass
        
        #self.correlated_stations= {k: self.correlated_stations[k] for k in 
        #                           self.correlated_stations if not 
        #                           np.isnan(self.correlated_stations[k])}

        #if(len(correlated_stations)<2):
        #    raise Exception("no enough correlated stations")
        
        
        aux_dict={k:v for k, v in self.correlated_stations.items() if v }
        self.correlated_stations.clear(); self.correlated_stations.update(aux_dict)
        
        del(aux_dict)
        
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
        Parameters5press
        ----------press
            - (x,y): point coordinates in the time series of the station being analyzed
            - thr: score below which a station is labelled as outlier
  press
        Output
        -------
            - Boolean: test result (True/False)
        """
        output_prob=params['p0']; sum_r= self.sum_r.copy()
        for target_station in self.correlated_stations:
            #_, f2= create_sets(correlated_stations[i], df)
            diff=self.correlated_stations[target_station]['f'](x)

            if(np.isnan(diff)):
                sum_r-=self.correlated_stations[target_station]['r']
                continue
            else:
                diff=abs(diff-y)


            #output_prob+= self.correlated_stations[target_station]['pdf'].integrate_box_1d(diff, np.inf)*self.correlated_stations[target_station]['r']
            output_prob+= self.correlated_stations[target_station]['pdf'].evaluate(diff)*params[str(target_station)]#self.correlated_stations[target_station]['r']
        #print(output_prob) 
        if(sum_r>0):
            if np.sign(output_prob)>0.:
                return True
            else:
                return False
            #output_prob/= sum_r
            #print(output_prob)
            #if (output_prob<params['p0']):
            #    return True
            #else:
            #    return False
            
        else:
            raise Exception("test inconclusive")

       # return output_prob
              

#test=STCT.init_cached('',6096.0)
#test.fit('train')
if __name__=="__main__":
    """
    test.optimize(3.5)
    """
    #test.save_cached('../data_files/Press/test_pkls_3_5/STCT')
    #test.prepare_points('train')
    """
    test.optimize(3.5)
    
    xs, f= create_sets(6104.0, 'deploy')
    test.prepare_points('deploy')
    print(test.calculate_acc(xs, f(xs), test.params, 3.5, 1000))
    """
    """
    #test.save_cached('sdfsdfsdf')
    test.save_cached('../data_files/temp/test_pkls_2_5/STCT')
    """
    import matplotlib.pyplot as plt
    def create_probability(my_station,target_station, df_name=None):   
    
           x1, f1= create_sets(my_station, df_name)
           x2, f2= create_sets(target_station, df_name)
    
           diff=[]
    
           for x in x1:
               diff.append(abs(f2(x)-f1(x)))
           return gaussian_kde(diff), diff
    
    plt.figure(figsize=(10,5))
    
    x=np.linspace(0., 15.0, 1000)
    kde, diffs=create_probability(6096.0, 6052.0, 'train')
    plt.hist(diffs, bins=30, alpha=0.8, density=True, color='b', label="strong correlation")
    plt.plot(x,kde(x), color='b')
    kde, diffs=create_probability(6096.0, 6190.0, 'train')
    plt.hist(diffs, bins=30, alpha=0.8, density=True, color='y',  label="weak correlation")
    plt.plot(x,kde(x), c='y')
    plt.xlim(0, 15)
    plt.xlabel("$|f(t)- g(t)|$", {'fontsize':14})
    plt.ylabel("$P(|f(t)- g(t)|)$", {'fontsize':14})
    plt.legend(loc="best", fontsize=14)
    plt.tight_layout()
    plt.savefig("../Images/KDE_weak_strong.png", dpi=300.)
    #test= STCT.init_cached('../data_files/Press/test_pkls_3_5/STCT',4310.0)