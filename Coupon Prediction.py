# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 17:38:10 2015

@author: atulgoel

Algorithm for finding test coupon similarity with train coupons

"""
import pandas as pd
import numpy as np
from scipy.spatial.distance import cosine
coupon=pd.read_csv("C:\\Users\\z078739\\Downloads\\Coupon Prediction\\combined_coupons_test_train.csv")
coupon['USABLE_DATE_MON'].fillna(1,inplace=True)
coupon['USABLE_DATE_TUE'].fillna(1,inplace=True)
coupon['USABLE_DATE_WED'].fillna(1,inplace=True)
coupon['USABLE_DATE_THU'].fillna(1,inplace=True)
coupon['USABLE_DATE_FRI'].fillna(1,inplace=True)
coupon['USABLE_DATE_SAT'].fillna(1,inplace=True)
coupon['USABLE_DATE_SUN'].fillna(1,inplace=True)
coupon['USABLE_DATE_HOLIDAY'].fillna(1,inplace=True)
coupon['USABLE_DATE_BEFORE_HOLIDAY'].fillna(1,inplace=True)
coupon=pd.concat([coupon,pd.get_dummies(coupon['CAPSULE_TEXT'])],axis=1)
coupon=pd.concat([coupon,pd.get_dummies(coupon['large_area_name'])],axis=1)
coupon=pd.concat([coupon,pd.get_dummies(coupon['ken_name'])],axis=1)
coupon=pd.concat([coupon,pd.get_dummies(coupon['small_area_name'])],axis=1)
coupon=coupon.drop(['CAPSULE_TEXT','GENRE_NAME','CATALOG_PRICE','DISPFROM','DISPEND','VALIDFROM','VALIDEND','VALIDPERIOD','large_area_name','ken_name','small_area_name','COUPON_ID_hash'],1)
#coupon1=coupon.ix[0:1000,:]
data=coupon.values
m,k=data.shape
mat=np.zeros((m,m))
for i in xrange(m):
    for j in xrange(m):
        if i!=j:
            mat[i][j]=1-cosine(data[i,:],data[j,:])
        else:
            mat[i][j]=0
check=pd.DataFrame(mat)
check.to_csv("C:\\Users\\z078739\\Downloads\\Coupon Prediction\\couponsimcheckfinal.csv",sep="\t",index=False)
#check1=check.ix[0:4000,:]
#check1.to_csv("C:\\Users\\z078739\\Downloads\\Coupon Prediction\\couponsimcheckfinaltrun.csv",sep="\t",index=False)
a=[i for i in range(311)]
data=pd.read_csv("C:\\Users\\z078739\\Downloads\\Coupon Prediction\\couponsimcheckfinal.csv",usecols=a,sep="\t")
sort_index=data.apply(np.argsort,axis=0)
final=sort_index.tail(30)
final.to_csv("C:\Users\z078739\Downloads\coupon prediction\couponsim.csv",sep="\t",index=False)


