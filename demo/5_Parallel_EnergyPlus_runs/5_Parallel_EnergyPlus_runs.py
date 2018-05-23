# -*- coding: utf-8 -*-

from multiprocessing import Pool
import os
import datetime
import shutil


def run_expand_objects(idf_fp):
    """Runs the ExpandObjects program
    
    Places the exapnded idf in the same folder as the 'idf_fp' file,
        with the name os.path.basename('df_fp')+'exp.idf'
    
    Arguments:
        idf_fp (str): the absolute filepath of the idf file - including the extension
    
    """
    new_fp=idf_fp[:-4]+'exp.idf'
    shutil.copyfile(idf_fp,r'C:\EnergyPlusV8-9-0\in.idf')
    now=datetime.datetime.now()
    os.system(r'C:\EnergyPlusV8-9-0\ExpandObjects')
    exp_fp=r'C:\EnergyPlusV8-9-0\expanded.idf'
    if os.path.isfile(exp_fp):
        unix_ts=os.path.getmtime(exp_fp)
        t=datetime.datetime.fromtimestamp(unix_ts)
        if t>now:
            shutil.copyfile(exp_fp,new_fp)
            return new_fp
    shutil.copyfile(idf_fp,new_fp)
    return new_fp
    

def run_energyplus(epexe_fp,
                   out_fp,
                   idf_fp,
                   epw_fp,
                   ):
        """Runs the EnergyPlus software
        
        Arguments:
            - epexe_fp (str): the absolute filepath of the 'energyplus.exe' file - excluding the extension
            - out_fp (str): the absolute filepath of the output folder
            - idf_fp (str): the absolute filepath of the idf file - including the extension
            - epw_fp (str): the absolute filepath of the epw file - including the extension
        
        """
        
        #CREATES THE 'OUT' FOLDER IF IT DOESN'T EXIST
        if not os.path.isdir(out_fp):
            os.mkdir(out_fp)
            
        #MANUALLY RUNS THE ExpandObjects PROGRAM
        idf_fp_new=run_expand_objects(idf_fp)
        
        #SETS THE OUTPUT PREFIX
        output_prefix=os.path.splitext(os.path.basename(idf_fp))[0]
        
        #RUN ENERGYPLUS VIA SUBPROCESS.POPEN
        l=[epexe_fp,
           '-r',
           '-c',
           '-d',out_fp,
           '-p',output_prefix,
           '-w',epw_fp,
           idf_fp_new]
        
        st=' '.join(l)
        
        os.system(st)
        
        return
        
    
def run_idf(idf_fp):
    """Runs EnergyPlus based on the idf filepath provided
    
    Places the resultsin the same folder as the idf file
    
    Arguments:
        idf_fp (str): the absolute filepath of the idf file - including the extension
        
    
    """
    epexe_fp=r'C:\EnergyPlusV8-9-0\EnergyPlus'
    out_fp=os.path.dirname(idf_fp)
    epw_fp=r'C:\EnergyPlusV8-9-0\WeatherData\USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw'
    run_energyplus(epexe_fp,
                   out_fp,
                   idf_fp,
                   epw_fp
                  )

if __name__ == '__main__': # ... needed for Pool...
    
    l=[os.path.join('sim','1ZoneUncontrolled_0.idf'),
       os.path.join('sim','1ZoneUncontrolled_90.idf'),
       os.path.join('sim','1ZoneUncontrolled_180.idf'),
       os.path.join('sim','1ZoneUncontrolled_270.idf')]
    
    now=datetime.datetime.now()
    print('START_TIME',now.strftime('%Y-%m-%d %H:%M:%S'))
    
    with Pool(4) as p: #the number here is the number of threads
        p.map(run_idf,l)
                
    for i in l:
        fp=i[:-4]+'out.csv'
        unix_ts=os.path.getmtime(fp)
        t=datetime.datetime.fromtimestamp(unix_ts)
        print(os.path.basename(i), t.strftime('%Y-%m-%d %H:%M:%S'), 'SUCCESS' if t>now else 'FAIL')
