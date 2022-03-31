
from scipy.stats import gaussian_kde

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
        print('no stations in the range ')
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

            diff=y-f2s[i](x)
            
            try:
                output_prob += pdfs[i].evaluate(diff)*(r[i])
            except:
                r=np.delete(r, i)
            
        output_prob/=sum(r)
        # I DON'T KNOW IF THIS IS THE PROBABILITY THAT MAKES SENSE 
        
        if (output_prob<thr):
            return True
        else:
            return False
    
    return evaluate_point, correlated_stations

