#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 12:02:53 2020

@author: jtellier

This script was created by Joshua Tellier of Purdue University on 4/13/2020 in order
to fulfill the requirments for lab 11 for ABE65100. 
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as pt #necessary module

def ReadData( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    raw data read from that file in a Pandas DataFrame.  The DataFrame index
    should be the year, month and day of the observation.  DataFrame headers
    should be "agency_cd", "site_no", "Date", "Discharge", "Quality". The 
    "Date" column should be used as the DataFrame index. The pandas read_csv
    function will automatically replace missing values with np.NaN, but needs
    help identifying other flags used by the USGS to indicate no data is 
    availabiel.  Function returns the completed DataFrame, and a dictionary 
    designed to contain all missing value counts that is initialized with
    days missing between the first and last date of the file."""
    global DataDF
    global MissingValues
    # define column names
    colNames = ['agency_cd', 'site_no', 'Date', 'Discharge', 'Quality']

    # open and read the file
    DataDF = pd.read_csv(fileName, header=1, names=colNames,  
                         delimiter=r"\s+",parse_dates=[2], comment='#',
                         na_values=['Eqp'])
    DataDF = DataDF.set_index('Date')
    
    # quantify the number of missing values
    for i in range(0,len(DataDF)-1): #checks for any values below zero, then replaces it with nan if outside the range
        if 0 > DataDF['Discharge'].iloc[i]:
            DataDF['Discharge'].iloc[i]=np.nan
    
    MissingValues = DataDF["Discharge"].isna().sum() #counts number of nan's
    
    return( DataDF, MissingValues )

def ClipData( DataDF, startDate, endDate ):
    """This function clips the given time series dataframe to a given range 
    of dates. Function returns the clipped dataframe and and the number of 
    missing values."""
    DataDF = DataDF.loc[startDate:endDate] #indexing for a specific date range (we use .loc because the dates are already the index)
    MissingValues = DataDF["Discharge"].isna().sum() #recalculating the number of missing values after trimming the dataset
    return( DataDF, MissingValues )
    
def GetMonthlyFlow(DataDF):
    """This function calculates monthly descriptive statistics and metrics 
    for the given streamflow time series.  Values are returned as a dataframe
    of monthly values for each year."""
    colnames = ['site_no','Mean Flow']
    monthdata=DataDF.resample('MS').mean()
    MoDataDF = pd.DataFrame(0, index=monthdata.index,columns=colnames)
    MoDataDF['site_no']=DataDF.resample('MS')['site_no'].mean()
    MoDataDF['Mean Flow']=DataDF.resample('MS')['Discharge'].mean()
    return ( MoDataDF )


def GetMonthlyAverageFlow(MoDataDF):
    """This function calculates annual average monthly values for all 
    statistics and metrics.  The routine returns an array of mean values 
    for each metric in the original dataframe."""
    colnames = ['site_no','Mean Flow']
    MonthlyAverages = pd.DataFrame(0, index=[1,2,3,4,5,6,7,8,9,10,11,12],columns=colnames) #create the empty dataframe
    MonthlyAverages.iloc[0,0]=MoDataDF['site_no'][::12].mean() #this gets messy, but essentially its taking the mean every 12 months (to keep the same month along all years)
    MonthlyAverages.iloc[1,0]=MoDataDF['site_no'][::12].mean()
    MonthlyAverages.iloc[2,0]=MoDataDF['site_no'][::12].mean()
    MonthlyAverages.iloc[3,0]=MoDataDF['site_no'][::12].mean()
    MonthlyAverages.iloc[4,0]=MoDataDF['site_no'][::12].mean()
    MonthlyAverages.iloc[5,0]=MoDataDF['site_no'][::12].mean()
    MonthlyAverages.iloc[6,0]=MoDataDF['site_no'][::12].mean()
    MonthlyAverages.iloc[7,0]=MoDataDF['site_no'][::12].mean()
    MonthlyAverages.iloc[8,0]=MoDataDF['site_no'][::12].mean()
    MonthlyAverages.iloc[9,0]=MoDataDF['site_no'][::12].mean()
    MonthlyAverages.iloc[10,0]=MoDataDF['site_no'][::12].mean()
    MonthlyAverages.iloc[11,0]=MoDataDF['site_no'][::12].mean()
    
    MonthlyAverages.iloc[0,1]=MoDataDF['Mean Flow'][3::12].mean() #take the mean of this metric sampling every 12 months, starting with the fourth month (0-indexed, and the dataset starts in october so this represents January)
    MonthlyAverages.iloc[1,1]=MoDataDF['Mean Flow'][4::12].mean() #mean of this metric subsampling every 12 months, starting with the 5th month in the dataset (February)
    MonthlyAverages.iloc[2,1]=MoDataDF['Mean Flow'][5::12].mean()
    MonthlyAverages.iloc[3,1]=MoDataDF['Mean Flow'][6::12].mean()
    MonthlyAverages.iloc[4,1]=MoDataDF['Mean Flow'][7::12].mean()
    MonthlyAverages.iloc[5,1]=MoDataDF['Mean Flow'][8::12].mean()
    MonthlyAverages.iloc[6,1]=MoDataDF['Mean Flow'][9::12].mean()
    MonthlyAverages.iloc[7,1]=MoDataDF['Mean Flow'][10::12].mean()
    MonthlyAverages.iloc[8,1]=MoDataDF['Mean Flow'][11::12].mean()
    MonthlyAverages.iloc[9,1]=MoDataDF['Mean Flow'][::12].mean()
    MonthlyAverages.iloc[10,1]=MoDataDF['Mean Flow'][1::12].mean()
    MonthlyAverages.iloc[11,1]=MoDataDF['Mean Flow'][2::12].mean()

    return( MonthlyAverages )


def ReadMetrics( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    the metrics from the assignment on descriptive statistics and 
    environmental metrics.  Works for both annual and monthly metrics. 
    Date column should be used as the index for the new dataframe.  Function 
    returns the completed DataFrame."""
    # open and read the file
    DataDF = pd.read_csv(fileName, header=0,  
                         delimiter=',',parse_dates=[1], comment='#')
    DataDF = DataDF.set_index('Date')
    return( DataDF )


# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.
# put the main routines from your code after this conditional check.

if __name__ == '__main__':

    # define full river names as a dictionary so that abbreviations are not used in figures
    riverName = { "Wildcat": "Wildcat Creek",
                  "Tippe": "Tippecanoe River" }
 
    #importing required datasets
    ReadData('TippecanoeRiver_Discharge_03331500_19431001-20200315.txt') #function from lab 10
    RawTippe, MissingValues = ClipData(DataDF,'1969-10-01','2019-09-30') #function from lab 10
    tippemonth = GetMonthlyFlow(RawTippe) #function from lab 10, this one is needed to process data for figure 3
    tippemonth = GetMonthlyAverageFlow(tippemonth) #function from lab 10, this one is needed to make figure 3
    ReadData('WildcatCreek_Discharge_03335000_19540601-20200315.txt')
    RawWild, MissingValues = ClipData(DataDF, '1969-10-01','2019-09-30')
    wildmonth = GetMonthlyFlow(RawWild)
    wildmonth = GetMonthlyAverageFlow(wildmonth)
    Annual = ReadMetrics('Annual_Metrics.csv') #using the new function I defined
    Month = ReadMetrics('Monthly_Metrics.csv')

    ## === Figures === ##

    #Daily stream flow for last 5 years
    Tippe5 = RawTippe['2014-10-01':'2019-09-30'] #clip data to the date range we want
    Wild5 = RawWild['2014-10-01':'2019-09-30']
    pt.figure(figsize=(16,10)) #custom size for better resolution
    pt.subplot(211)
    pt.plot(Tippe5.index,Tippe5['Discharge'], 'black',label = 'Tippecanoe')
    pt.ylabel('Discharge (cfs)')
    pt.legend(loc='upper right')
    pt.subplot(212)
    pt.plot(Wild5.index,Wild5['Discharge'], 'red',label = 'Wildcat')
    pt.xlabel('Date')
    pt.ylabel('Discharge (cfs)')
    pt.legend(loc='upper right') #adding legend
    pt.savefig('5yrflow.png')
    pt.close()

    #Annual coeff var, TQmean, and R-B index
    fig = pt.figure(figsize=(16,10)) #custom size for better resolution
    pt.subplot(311)
    pt.plot(Annual.index[Annual['Station'] == 'Tippe'],Annual['Coeff Var'][Annual['Station'] == 'Tippe'], 'black', linestyle='None',marker='.', label='Tippecanoe') #this uses filtered plotting, so we only plot the tippecanoe values
    pt.plot(Annual.index[Annual['Station'] == 'Wildcat'],Annual['Coeff Var'][Annual['Station'] == 'Wildcat'], 'red', linestyle='None',marker='x',label='Wildcat') #this uses filtered plotting, so we only plot the wildcat values
    pt.legend(loc='upper right')
    ax = pt.gca() #assigning the axis to an object so we can mess with it
    ax.axes.xaxis.set_ticklabels([]) #removing tick labels so they only appear on the BOTTOM subplot, for clarity and cleanliness
    ax.xaxis.grid(which='major',color='gray',linewidth=0.5,linestyle='--',alpha=0.5) #adding vertical lines for ease of interpretation
    pt.ylabel('Coeff. Var.')
    pt.text(-1,200,'A)') #add label to subplot
    pt.subplot(312)
    pt.plot(Annual.index[Annual['Station'] == 'Tippe'],Annual['TQmean'][Annual['Station'] == 'Tippe'], 'black', linestyle='None',marker='.')
    pt.plot(Annual.index[Annual['Station'] == 'Wildcat'],Annual['TQmean'][Annual['Station'] == 'Wildcat'], 'red', linestyle='None',marker='x')
    ax = pt.gca() #same as before
    ax.axes.xaxis.set_ticklabels([])
    ax.xaxis.grid(which='major',color='gray',linewidth=0.5,linestyle='--',alpha=0.5)
    pt.ylabel('TQmean')
    pt.text(-1,0.5,'B)')
    pt.subplot(313)
    pt.plot(Annual.index[Annual['Station'] == 'Tippe'],Annual['R-B Index'][Annual['Station'] == 'Tippe'], 'black', linestyle='None',marker='.')
    pt.plot(Annual.index[Annual['Station'] == 'Wildcat'],Annual['R-B Index'][Annual['Station'] == 'Wildcat'], 'red', linestyle='None',marker='x')
    ax = pt.gca() #this time, we will be creating the x-axis
    ax.set_xticklabels(np.arange(1969,2019,1)) #set integer year values
    ax.tick_params(axis='x',labelrotation=40) #rotate them to be visible and legible
    ax.xaxis.grid(which='major',color='gray',linewidth=0.5,linestyle='--',alpha=0.5)
    pt.ylabel('R-B Index')
    pt.text(-1,0.32,'C)')
    pt.savefig('annualstats.png')
    pt.close()

    #Average annual monthly flow
    fig = pt.figure(figsize=(16,10)) #custom figure size for better resolution
    pt.plot(tippemonth.index,tippemonth['Mean Flow'],'black',linestyle='None',marker='.',label='Tippecanoe')
    pt.plot(wildmonth.index,wildmonth['Mean Flow'],'red', linestyle='None',marker='x',label='Wildcat')
    pt.xticks(np.arange(1,13,1)) #custom x ticks to denote month of year
    pt.legend(loc='upper right')
    pt.xlabel('Month of Year')
    pt.ylabel('Discharge (cfs)')
    pt.savefig('averagemonthlyflow.png')
    pt.close()
    
    #period of annual peak flow events
    wild = Annual[Annual['Station']=='Wildcat']
    tippe = Annual[Annual['Station'] == 'Tippe']
    tpeaksort = tippe.sort_values('Peak Flow', ascending = False) #sorting values based on the peak flow parameter in DESCENDING order
    tpeaksort['Rank'] = np.arange(1,51,1) #assigning the proper rank to each value
    tpeaksort['Exceedence'] = tpeaksort['Rank']/51 #calculating exceedence probability
    wpeaksort = wild.sort_values('Peak Flow', ascending = False)
    wpeaksort['Rank'] = np.arange(1,51,1)
    wpeaksort['Exceedence'] = wpeaksort['Rank']/51
    fig = pt.figure(figsize=(12,10))
    pt.plot(tpeaksort['Exceedence'],tpeaksort['Peak Flow'], 'black', linestyle='None',marker='.', label = 'Tippecanoe') #adding our custom exceedence values to a plot
    pt.plot(wpeaksort['Exceedence'],wpeaksort['Peak Flow'], 'red', linestyle='None',marker='x', label = 'Wildcat')
    ax = pt.gca()
    ax.set_xlim(1,0) #reversing x-axis
    pt.xlabel('Exceedence Probability')
    pt.ylabel('Discharge (cfs)')
    pt.legend(loc='lower right')
    ax.yaxis.grid(which='major',color='gray',linewidth=0.5,linestyle='--',alpha=0.5) #horizontal lines for ease of interpretation
    pt.savefig('exceedence.png')
    pt.close()