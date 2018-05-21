# -*- coding: utf-8 -*-

from multiprocessing import Pool
import os
import datetime

def run_energyplus(epexe_fp,
                   out_fp,
                   idf_fp,
                   epw_fp,
                   output_prefix='eplus',
                   display=True
                   ):
        """Runs the EnergyPlus software
        
        Arguments:
            - epexe_fp (str): the absolute filepath of the 'energyplus.exe' file - excluding the extension
            - out_fp (str): the absolute filepath of the output folder
            - idf_fp (str): the absolute filepath of the idf file - including the extension
            - epw_fp (str): the absolute filepath of the epw file - including the extension
            - display(boolean):
        
        """
        
        #CREATES THE 'OUT' FOLDER IF IT DOESN'T EXIST
        if not os.path.isdir(out_fp):
            os.mkdir(out_fp)
            
        #DELETES THE 'eplusout.expidf' FILE IN 'out_fp' IF IT'S PRESENT
        #    this is needed to force the recreation of this file...
        expidf_fp=os.path.join(out_fp,output_prefix+'out.expidf')
        if os.path.isfile(expidf_fp):
            os.remove(expidf_fp) 
            
        #RUN ENERGYPLUS VIA SUBPROCESS.POPEN
        l=[epexe_fp,
           '-x',
           '-r',
           '-c',
           '-d',out_fp,
           '-p',output_prefix,
           '-w',epw_fp,
           idf_fp]
        
        st=' '.join(l)
        
        os.system(st)
        
        return
        
    
def run_idf(idf_fp):
    "Runs EnergyPlus based on the idf filepath provided"
    epexe_fp=r'C:\EnergyPlusV8-9-0\EnergyPlus'
    out_fp=os.path.abspath('sim')
    idf_fp=os.path.join(out_fp,idf_fp)
    epw_fp=r'C:\EnergyPlusV8-9-0\WeatherData\USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw'
    output_prefix=os.path.splitext(os.path.basename(idf_fp))[0]
    run_energyplus(epexe_fp,
                   out_fp,
                   idf_fp,
                   epw_fp,
                   output_prefix
                  )


if __name__ == '__main__': # ... needed for Pool...
    
    l=['1ZoneUncontrolled_0.idf',
       '1ZoneUncontrolled_90.idf',
       '1ZoneUncontrolled_180.idf',
       '1ZoneUncontrolled_270.idf']

    now=datetime.datetime.now()
    print('START_TIME',now.strftime('%Y-%m-%d %H:%M:%S'))
    
    with Pool(2) as p: #the number here is the number of threads
        p.map(run_idf,l)
        
#SOMETIMES AN IDF DOESN'T RUN
#   It's not clear why this happens
#   Different idfs don't run at different times
#   This can be picked up by viewing the modified times of the .csv files (see below)
#   One solution would be to identify the failures and rerun them...
        
    for i in l:
        fp=os.path.join('sim',i[:-4]+'out.csv')
        unix_ts=os.path.getmtime(fp)
        t=datetime.datetime.fromtimestamp(unix_ts)
        print(i, t.strftime('%Y-%m-%d %H:%M:%S'), 'SUCCESS' if t>now else 'FAIL')
