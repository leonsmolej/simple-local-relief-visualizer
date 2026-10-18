import rasterio as rio
import numpy as np
import os
from scipy.ndimage import gaussian_filter
import glob
import time



def dobi_pathe_fajlov(dem_path_folder):
    fajl_types=["tif", "tiff", "TIF", "TIFF"]
    dem_fajli_path=[]
    for i in fajl_types:
        dem_fajli_path=sorted(set(dem_fajli_path+glob.glob(f"{dem_path_folder}/*.{i}")))
    return dem_fajli_path



def naredi_slrm(dem_path_fajli, range, vmin, vmax, dem_path_folder):

    ime_fajla=os.path.basename(dem_path_fajli)

    dem_path = os.path.normpath(dem_path_fajli)

    with rio.open(dem_path) as src:
        dem=src.read(1)
        #print(src.height)
        #print(src.width)
        vel_celice=src.res[0]
        #print(vel_celice)
        meta=src.meta.copy()

    print("")
    print(f"Obdelujem: {ime_fajla}")
    izravnan_dem=gaussian_filter(dem,float(range))

    slrm=dem-izravnan_dem

    slrm=np.clip(slrm,float(vmin), float(vmax))

    #print(slrm.shape[1])
    #print(slrm)
    #show(slrm, cmap="gray")
    
    os.makedirs(f"{dem_path_folder}/Rezultati_SLRM", exist_ok=True)

    with rio.open(fr"{dem_path_folder}/Rezultati_SLRM/SLRM_{ime_fajla}","w", **meta) as dst:
            dst.write(slrm, 1)



def glavna_rutina(dem_path_folder, pix_range, v_min, v_max):
    dem_fajli_path=dobi_pathe_fajlov(dem_path_folder)
    for i in dem_fajli_path:
        naredi_slrm(i,pix_range,v_min,v_max, dem_path_folder)
    print("")
    print(f"Končal. Rezultati so v mapi {dem_path_folder}/Rezultati_SLRM")
    print("")



def input_rutine():

    dem_path_folder=input("Vnesi pot do mape z DEM-i: ")
    print("")


    while True:
        range=input("Vnesi radij za Gaussov filter v pikslih. \n(za manjše strukture priporočljivo 20, za večje 40, odvisno sicer tudi od resolucije DEM-a): ")
        try:
            if 0<= float(range) <=500:
                break
            else:
                print()
                time.sleep(0.5)
                print("Vnešena je bila napačna vrednost. (Vrednost naj bo med 0 in 500)")
                time.sleep(0.5)
                print()
        except ValueError:
            print()
            time.sleep(0.5)
            print("Vnešena je bila napačna vrednost. (Vrednost naj bo med 0 in 500)")
            time.sleep(0.5)
            print() 
    print("")


    while True:
        v_min=input("Vnesi minimalno vrednost za raztegnitev vrednosti pri vizualizaciji. \n(priporočljivo -1.5: ").replace(",",".")
        try:
            if -10<= float(v_min) <= 0:
                break
            else:
                print()
                time.sleep(0.5)
                print("Vnešena je bila napačna vrednost. (Vrednost naj bo med -10 in 0)")
                time.sleep(0.5)
                print()
        except ValueError:
            print()
            time.sleep(0.5)
            print("Vnešena je bila napačna vrednost. (Vrednost naj bo med -10 in 0)")
            time.sleep(0.5)
            print()
    print("")


    while True:
        v_max=input("Vnesi maksimalno vrednost za raztegnitev vrednosti pri vizualizaciji. \n(priporočljivo 1.5: ").replace(",",".")
        try:
            if 0<= float(v_max) <=10:
                break
            else:
                print()
                time.sleep(0.5)
                print("Vnešena je bila napačna vrednost. (Vrednost naj bo med 0 in 10)")
                time.sleep(0.5)
                print()
        except ValueError:
            print()
            time.sleep(0.5)
            print("Vnešena je bila napačna vrednost. (Vrednost naj bo med 0 in 10)")
            time.sleep(0.5)
            print()
    print("")
    
    return(dem_path_folder,range, v_min, v_max)

