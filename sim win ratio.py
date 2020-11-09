# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 12:00:03 2020

@author: CHAO
"""

import pandas as pd
import numpy as np
from scipy.stats import binom,gamma,norm


def loop1(runs=100):
    for num in range(sublist.index(subcount)*runs,(sublist.index(subcount)+1)*runs):
    
        deatht=binom.rvs(1,0.108,size=subcount)
        rehospt=binom.rvs(1,0.33,size=subcount)
        kccqt=gamma.rvs(a=2.21,scale=15.2,size=subcount)
        gfrt=gamma.rvs(a=3.17,scale=17.96,size=subcount)
    
        deathc=binom.rvs(1,0.13,size=subcount)
        rehospc=binom.rvs(1,0.402,size=subcount)
        kccqc=gamma.rvs(a=1.6,scale=18,size=subcount)
        gfrc=gamma.rvs(a=2.65,scale=20,size=subcount)

        trt=pd.DataFrame({'pid_trt':np.arange(subcount),'evt4_trt':deatht,'evt3_trt':rehospt,'evt2_trt':kccqt,'evt1_trt':gfrt})
        
        con=pd.DataFrame({'pid_con':np.arange(subcount,2*subcount),'evt4_con':deathc,'evt3_con':rehospc,'evt2_con':kccqc,'evt1_con':gfrc})
        
    
        con['key']=1
        trt['key']=1
      
      #### Join the two groups
        trtcon = pd.merge(left=con,right=trt,on='key')
        trtcon.drop(columns=['key'],inplace=True)
      
      
      
      #### Control patient won, per Endpoint 4
        trtcon['a'] =  ((trtcon['evt4_trt'] == 1) & (trtcon['evt4_con'] < 1) ) *1
      
      #### Treatment patient won, per Endpoint 4
        trtcon['b']=  ((trtcon['evt4_trt'] < 1 )& (trtcon['evt4_con'] == 1 )) *1
      
      #### Control patient won, per Endpoint 3
        trtcon['c'] =  ((trtcon['evt3_trt'] == 1 )&( trtcon['evt3_con'] < 1 ) )*1
      
      #### Treatment patient won, per Endpoint 3
        trtcon['d'] =  ((trtcon['evt3_trt'] < 1 )& (trtcon['evt3_con'] == 1 ) )*1
      
      
      #### Control patient won, per Endpoint 2
        trtcon['e'] =  pd.Series( np.where(trtcon['evt2_trt']  < trtcon['evt2_con'] -5,1,0))
      
      
      #### Treatment patient won, per Endpoint 2
        trtcon['f'] = pd.Series( np.where(trtcon['evt2_con']  < trtcon['evt2_trt'] -5,1,0)) 
      
      
      #### Control patient won, per Endpoint 2
        trtcon['g'] =  pd.Series( np.where(trtcon['evt1_con']-trtcon['evt1_trt'] >5 ,1,0))
      
      #### Treatment patient won, per Endpoint 2
        trtcon['h'] =  pd.Series( np.where(trtcon['evt1_trt']-trtcon['evt1_con'] >5 ,1,0))
    
      
      
      
      #### prioritize
     
       
        trtcon['c']=-(trtcon['a']+trtcon['b']==1)*trtcon['c']
        trtcon['d']=-(trtcon['a']+trtcon['b']==1)*trtcon['d']    
        
        trtcon['e']=-(trtcon['a']+trtcon['b']+trtcon['c']+trtcon['d']==1)*trtcon['e']
        trtcon['f']=-(trtcon['a']+trtcon['b']+trtcon['c']+trtcon['d']==1)*trtcon['f']    
        
        trtcon['g']=-(trtcon['a']+trtcon['b']+trtcon['c']+trtcon['d']+trtcon['e']+trtcon['f']==1)*trtcon['g']
        trtcon['h']=-(trtcon['a']+trtcon['b']+trtcon['c']+trtcon['d']+trtcon['e']+trtcon['f']==1)*trtcon['h']    
        
     
      #############################################################################################
      #### Stratum-specific win ratios
      #############################################################################################
    
        na = sum(trtcon['a'])
        nb = sum(trtcon['b'])
        nc = sum(trtcon['c'])
        nd = sum(trtcon['d'])
        ne = sum(trtcon['e'])
        nf = sum(trtcon['f'])
        ng = sum(trtcon['g'])
        nh = sum(trtcon['h'])
      
      
      
      ### number of wins per stratum
        win_con = na+nc+ne+ng
        win_trt= nb+nd+nf+nh
      
      ### stratum-specific win ratio
        WR = win_trt/win_con
      
      ### number of patients per stratum
        N_trt = len(trt)
        N_con = len(con)
      
      
      #### theta K0/L0
        theta_KL_0 = (win_trt + win_con)/(2*len(trtcon))
      
      #############################################################################################
      #### variances and covariances per stratum
      #############################################################################################
      
      ### Kernel function K and L
        trtcon['K'] = trtcon['b']+trtcon['d']+trtcon['f']+trtcon['h']
        trtcon['L'] = trtcon['a']+trtcon['c']+trtcon['e']+trtcon['g']
        
        KL=trtcon
      
        sum_k_trt = pd.DataFrame(KL.groupby('pid_trt').agg(func=sum)['K'])
        sum_k_trt.reset_index(level=0,inplace=True)
      
        sum_k_con = pd.DataFrame( KL.groupby('pid_con').agg(func=sum)['K'])
        sum_k_con.reset_index(level=0,inplace=True)
      
        sum_L_trt = pd.DataFrame(KL.groupby('pid_trt').agg(func=sum)['L'])
        sum_L_trt.reset_index(level=0,inplace=True)
      
        sum_L_con =  pd.DataFrame(KL.groupby('pid_con').agg(func=sum)['L'])
        sum_L_con.reset_index(level=0,inplace=True)
      
      
        sum_k_trt.rename(columns={'K':'sum_k_trt'},inplace=True)
        sum_k_con.rename(columns={'K':'sum_k_con'},inplace=True)
        sum_L_trt.rename(columns={'L':'sum_L_trt'},inplace=True)
        sum_L_con.rename(columns={'L':'sum_L_con'},inplace=True)
    
      
        KL = pd.merge(KL, sum_k_trt, on= 'pid_trt')
        KL = pd.merge(KL, sum_k_con,on= 'pid_con')
        KL = pd.merge(KL, sum_L_trt,on=  'pid_trt')
        KL = pd.merge(KL, sum_L_con, on= 'pid_con')
      
    
     
        KL['theta_KL_0']=theta_KL_0
      
      
        sig2_trt1 = N_trt*N_con*sum((KL['K']-theta_KL_0)*(KL['sum_k_trt'] - KL['K'] - (N_con - 1)*theta_KL_0 ))/(N_con-1)
        sig2_trt2 = N_con*N_trt*sum((KL['K']-theta_KL_0)*(KL['sum_k_con'] - KL['K'] - (N_trt - 1)*theta_KL_0 ))/(N_trt-1)
      
      
        sig2_con1 = N_con*N_trt*sum((KL['L']-theta_KL_0)*(KL['sum_L_con' ]- KL['L'] - (N_trt - 1)*theta_KL_0 ))/(N_trt-1)
        sig2_con2 = N_trt*N_con*sum((KL['L']-theta_KL_0)*(KL['sum_L_trt'] - KL['L'] - (N_con - 1)*theta_KL_0 ))/(N_con-1)
      
        sig_trt_con1 =  N_con*N_trt*sum((KL['K']-theta_KL_0)*(KL['sum_L_trt'] - KL['L'] - (N_con - 1)*theta_KL_0 ))/(N_con-1)
        sig_trt_con2 = N_trt*N_con*sum((KL['K']-theta_KL_0)*(KL['sum_L_con'] - KL['L'] - (N_trt - 1)*theta_KL_0 ))/(N_trt-1)
      
    
    
    
        sig2_trt = sig2_trt1/N_trt + sig2_trt2/N_con
        sig2_con = sig2_con1/N_con + sig2_con2/N_trt
        sig_trt_con = sig_trt_con1/N_trt + sig_trt_con2/N_con
      
      
      #############################################################################################
      #### Stratified win ratio
      #############################################################################################
      
      ## Total sample size per stratum
        N = N_trt + N_con
      
      ### Stratified win ratio wit Mantel-Haenszel-type wights
        WR = win_trt/win_con
      
      #############################################################################################
      #### Homogeneity test per Cochran (1954)
      #############################################################################################
      
      ### Variance estimate of log (win ratio) per stratum
        var = 4*(sig2_trt + sig2_con - 2*sig_trt_con)/((win_trt + win_con)*(win_trt + win_con))
      
        wr_z= abs(np.log(win_trt/win_con)/np.sqrt(var));
      
        wr_p=1-norm.cdf(wr_z)
    
        store.iloc[num,0]=wr_z
        store.iloc[num,1]=wr_p
        store.iloc[num,2]=subcount
        
        
        
        
        
        

sublist=[*range(320,330,5)]

runs=40000        
store=pd.DataFrame(np.zeros((len(sublist)*runs,3)))

for subcount in sublist:
    loop1(runs=40000)



sim1.rename(columns={'0':0,'1':1,'2':2},inplace=True)
finn_total=pd.concat([store,sim1])

finn_total.rename(columns={0:'wr_z',1:'wr_p',2:'subcount'},inplace=True)




# for num in range(10000):
    
    
#     deatht=binom.rvs(1,0.108,size=subcount)
#     rehospt=binom.rvs(1,0.33,size=subcount)
#     kccqt=gamma.rvs(a=2.21,scale=15.2,size=subcount)
#     gfrt=gamma.rvs(a=3.31,scale=17.59,size=subcount)

#     deathc=binom.rvs(1,0.13,size=subcount)
#     rehospc=binom.rvs(1,0.402,size=subcount)
#     kccqc=gamma.rvs(a=1.6,scale=18,size=subcount)
#     gfrc=gamma.rvs(a=2.65,scale=20,size=subcount)

#     trt=pd.DataFrame({'pid_trt':np.arange(subcount),'evt4_trt':deatht,'evt3_trt':rehospt,'evt2_trt':kccqt,'evt1_trt':gfrt})
    
#     con=pd.DataFrame({'pid_con':np.arange(subcount,2*subcount),'evt4_con':deathc,'evt3_con':rehospc,'evt2_con':kccqc,'evt1_con':gfrc})
    

#     con['key']=1
#     trt['key']=1
  
#   #### Join the two groups
#     trtcon = pd.merge(left=con,right=trt,on='key')
#     trtcon.drop(columns=['key'],inplace=True)
  
  
  
#   #### Control patient won, per Endpoint 4
#     trtcon['a'] =  ((trtcon['evt4_trt'] == 1) & (trtcon['evt4_con'] < 1) ) *1
  
#   #### Treatment patient won, per Endpoint 4
#     trtcon['b']=  ((trtcon['evt4_trt'] < 1 )& (trtcon['evt4_con'] == 1 )) *1
  
#   #### Control patient won, per Endpoint 3
#     trtcon['c'] =  ((trtcon['evt3_trt'] == 1 )&( trtcon['evt3_con'] < 1 ) )*1
  
#   #### Treatment patient won, per Endpoint 3
#     trtcon['d'] =  ((trtcon['evt3_trt'] < 1 )& (trtcon['evt3_con'] == 1 ) )*1
  
  
#   #### Control patient won, per Endpoint 2
#     trtcon['e'] =  pd.Series( np.where(trtcon['evt2_trt']  < trtcon['evt2_con'] -5,1,0))
  
  
#   #### Treatment patient won, per Endpoint 2
#     trtcon['f'] = pd.Series( np.where(trtcon['evt2_con']  < trtcon['evt2_trt'] -5,1,0)) 
  
  
#   #### Control patient won, per Endpoint 2
#     trtcon['g'] =  pd.Series( np.where(trtcon['evt1_con']-trtcon['evt1_trt'] >5 ,1,0))
  
#   #### Treatment patient won, per Endpoint 2
#     trtcon['h'] =  pd.Series( np.where(trtcon['evt1_trt']-trtcon['evt1_con'] >5 ,1,0))

  
  
  
#   #### prioritize
 
   
#     trtcon['c']=-(trtcon['a']+trtcon['b']==1)*trtcon['c']
#     trtcon['d']=-(trtcon['a']+trtcon['b']==1)*trtcon['d']    
    
#     trtcon['e']=-(trtcon['a']+trtcon['b']+trtcon['c']+trtcon['d']==1)*trtcon['e']
#     trtcon['f']=-(trtcon['a']+trtcon['b']+trtcon['c']+trtcon['d']==1)*trtcon['f']    
    
#     trtcon['g']=-(trtcon['a']+trtcon['b']+trtcon['c']+trtcon['d']+trtcon['e']+trtcon['f']==1)*trtcon['g']
#     trtcon['h']=-(trtcon['a']+trtcon['b']+trtcon['c']+trtcon['d']+trtcon['e']+trtcon['f']==1)*trtcon['h']    
    
 
#   #############################################################################################
#   #### Stratum-specific win ratios
#   #############################################################################################

#     na = sum(trtcon['a'])
#     nb = sum(trtcon['b'])
#     nc = sum(trtcon['c'])
#     nd = sum(trtcon['d'])
#     ne = sum(trtcon['e'])
#     nf = sum(trtcon['f'])
#     ng = sum(trtcon['g'])
#     nh = sum(trtcon['h'])
  
  
  
#   ### number of wins per stratum
#     win_con = na+nc+ne+ng
#     win_trt= nb+nd+nf+nh
  
#   ### stratum-specific win ratio
#     WR = win_trt/win_con
  
#   ### number of patients per stratum
#     N_trt = len(trt)
#     N_con = len(con)
  
  
#   #### theta K0/L0
#     theta_KL_0 = (win_trt + win_con)/(2*len(trtcon))
  
#   #############################################################################################
#   #### variances and covariances per stratum
#   #############################################################################################
  
#   ### Kernel function K and L
#     trtcon['K'] = trtcon['b']+trtcon['d']+trtcon['f']+trtcon['h']
#     trtcon['L'] = trtcon['a']+trtcon['c']+trtcon['e']+trtcon['g']
    
#     KL=trtcon
  
#     sum_k_trt = pd.DataFrame(KL.groupby('pid_trt').agg(func=sum)['K'])
#     sum_k_trt.reset_index(level=0,inplace=True)
  
#     sum_k_con = pd.DataFrame( KL.groupby('pid_con').agg(func=sum)['K'])
#     sum_k_con.reset_index(level=0,inplace=True)
  
#     sum_L_trt = pd.DataFrame(KL.groupby('pid_trt').agg(func=sum)['L'])
#     sum_L_trt.reset_index(level=0,inplace=True)
  
#     sum_L_con =  pd.DataFrame(KL.groupby('pid_con').agg(func=sum)['L'])
#     sum_L_con.reset_index(level=0,inplace=True)
  
  
#     sum_k_trt.rename(columns={'K':'sum_k_trt'},inplace=True)
#     sum_k_con.rename(columns={'K':'sum_k_con'},inplace=True)
#     sum_L_trt.rename(columns={'L':'sum_L_trt'},inplace=True)
#     sum_L_con.rename(columns={'L':'sum_L_con'},inplace=True)

  
#     KL = pd.merge(KL, sum_k_trt, on= 'pid_trt')
#     KL = pd.merge(KL, sum_k_con,on= 'pid_con')
#     KL = pd.merge(KL, sum_L_trt,on=  'pid_trt')
#     KL = pd.merge(KL, sum_L_con, on= 'pid_con')
  

 
#     KL['theta_KL_0']=theta_KL_0
  
  
#     sig2_trt1 = N_trt*N_con*sum((KL['K']-theta_KL_0)*(KL['sum_k_trt'] - KL['K'] - (N_con - 1)*theta_KL_0 ))/(N_con-1)
#     sig2_trt2 = N_con*N_trt*sum((KL['K']-theta_KL_0)*(KL['sum_k_con'] - KL['K'] - (N_trt - 1)*theta_KL_0 ))/(N_trt-1)
  
  
#     sig2_con1 = N_con*N_trt*sum((KL['L']-theta_KL_0)*(KL['sum_L_con' ]- KL['L'] - (N_trt - 1)*theta_KL_0 ))/(N_trt-1)
#     sig2_con2 = N_trt*N_con*sum((KL['L']-theta_KL_0)*(KL['sum_L_trt'] - KL['L'] - (N_con - 1)*theta_KL_0 ))/(N_con-1)
  
#     sig_trt_con1 =  N_con*N_trt*sum((KL['K']-theta_KL_0)*(KL['sum_L_trt'] - KL['L'] - (N_con - 1)*theta_KL_0 ))/(N_con-1)
#     sig_trt_con2 = N_trt*N_con*sum((KL['K']-theta_KL_0)*(KL['sum_L_con'] - KL['L'] - (N_trt - 1)*theta_KL_0 ))/(N_trt-1)
  



#     sig2_trt = sig2_trt1/N_trt + sig2_trt2/N_con
#     sig2_con = sig2_con1/N_con + sig2_con2/N_trt
#     sig_trt_con = sig_trt_con1/N_trt + sig_trt_con2/N_con
  
  
#   #############################################################################################
#   #### Stratified win ratio
#   #############################################################################################
  
#   ## Total sample size per stratum
#     N = N_trt + N_con
  
#   ### Stratified win ratio wit Mantel-Haenszel-type wights
#     WR = win_trt/win_con
  
#   #############################################################################################
#   #### Homogeneity test per Cochran (1954)
#   #############################################################################################
  
#   ### Variance estimate of log (win ratio) per stratum
#     var = 4*(sig2_trt + sig2_con - 2*sig_trt_con)/((win_trt + win_con)*(win_trt + win_con))
  
#     wr_z= abs(np.log(win_trt/win_con)/np.sqrt(var));
  
#     wr_p=1-norm.cdf(wr_z)

#     store.iloc[num,0]=wr_z
#     store.iloc[num,1]=wr_p
#     store.iloc[num,2]=subcount