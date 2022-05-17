import sys

sys.path.insert(0, '..')



from scipy.stats import gaussian_kde
import pandas as pd
import scipy.signal as signal
from preprocessing.create_sets import create_sets
import numpy as np

df=  pd.read_pickle("/home/tobou/Desktop/Meteorological_Data_quality_assesment/df_gen/df.pkl")  
def correlate_signals(station1, station2, num=100000):  
    """
    Parameters
    ----------
        - (station1,station2): pair of stations for which the correlation score is to be computed
        - num: length of the arrays created by interpolation of the stations time-series. Default=100000 points.    
    Otuputs
    -------
        - lags
    """

    
    x1, f1= create_sets(station1)
    x2, f2= create_sets(station2)
    
    xrange=np.linspace(max(min(x1),min(x2)), min(max(x1),max(x2)), num)
    
    a= f1(xrange)
    b= f2(xrange)

    a= (a - np.mean(a)) / (np.std(a) * num)
    b= (b - np.mean(b)) / (np.std(b) * num)
    corr = signal.correlate(a,b)
    corr*=len(a) #Does this make sense?
    #lags = signal.correlation_lags(len(a), len(b))
    
    return corr

stations=df['station'].unique()

try:
    stations_correlations= np.loadtxt('../tests/stations_correlations.csv')
except:
    print('recalculating stations_correlations')
    stations_correlations= np.zeros((len(stations),len(stations)))
    for i in range(len(stations)):
       for j in range(len(stations)):
           
           stations_correlations[i,j]= max(correlate_signals(stations[i],stations[j], 10000)
    )
def create_probability(station,target_station, df=df):
    
    x1, f1= create_sets(station, df)
    x2, f2= create_sets(target_station, df)
    
    diff=[]
    
    for x in x1:
        diff.append(f2(x)-f1(x))
    return gaussian_kde(diff)

def build_pdfs(station,  thr=0.1, df=df):
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
    
    stations= df['station'].unique()[:]
    
    
    station_index= np.where(stations == station)[0][0]
    r_thr=1.
    correlated_stations= []
    
    r=[]

    while(r_thr>0.9 and len(correlated_stations)<11):
        correlated_stations= stations[stations_correlations[station_index,:]>r_thr]
        r= stations_correlations[station_index,stations_correlations[station_index,:]>r_thr]
        
        r_thr-=1e-5
        
    correlated_stations=np.delete(correlated_stations, np.where(correlated_stations == station) )
    r=np.delete(r, np.where(r == 1.) )
    
    pdfs=[]
    f2s=[]
    for target_station in correlated_stations:
        try:
            pdfs.append(create_probability(station,target_station,df))
            f2s.append(create_sets(target_station, df)[1])
            
        except:
            pdfs.append(None)
    
    if(len(correlated_stations)==0):
        print('no stations in the range')
    def evaluate_point(x, y, thr, r=r):
        """
        Parameters
        ----------
            - (x,y): point coordinates in the time series of the station being analyzed
            - thr: score below which a station is labelled as outlier
            - r: correlation scores list
  
        Output
        -------
            - Boolean: test result (True/False)
        """
        output_prob=0.
        for i in range(len(correlated_stations)):
            #_, f2= create_sets(correlated_stations[i], df)

            diff=f2s[i](x)-y
            
            try:
                output_prob += pdfs[i].evaluate(diff)*(r[i])**2
            except:
                r=np.delete(r, i)
            
        output_prob/=sum(r)
        # I DON'T KNOW IF THIS IS THE PROBABILITY THAT MAKES SENSE 
        
       # return output_prob
              
        if (output_prob<thr):
            return True
        else:
            return False
        
    return evaluate_point

