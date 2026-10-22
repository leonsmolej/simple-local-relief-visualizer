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



def naredi_slrm(dem_path_fajli, radij, vmin, vmax, dem_path_folder):

    ime_fajla=os.path.basename(dem_path_fajli)

    dem_path = os.path.normpath(dem_path_fajli)

    with rio.open(dem_path) as src:
        dem=src.read(1)
        #print(src.height)
        #print(src.width)
        #vel_celice=src.res[0]
        #print(vel_celice)
        meta=src.meta.copy()
        no_data=src.nodata

    print("")
    print(f"Obdelujem: {ime_fajla}")

    dem=dem.astype(float)

    dem[dem == no_data] = np.nan

    dem[dem == -9999]=np.nan

    povprecna_vrednost=np.nanmean(dem)

    dem[np.isnan(dem)]=povprecna_vrednost


    izravnan_dem=gaussian_filter(dem,float(radij))

    slrm=dem-izravnan_dem

    slrm=np.clip(slrm,float(vmin), float(vmax))

    #print(slrm.shape[1])
    #print(slrm)
    #show(slrm, cmap="gray")
    
    os.makedirs(f"{dem_path_folder}/Rezultati_SLRM", exist_ok=True)

    with rio.open(fr"{dem_path_folder}/Rezultati_SLRM/SLRM_{ime_fajla}","w", **meta) as dst:
            dst.write(slrm, 1)



def input_rutine():

    parametri={}

    parametri["dem_path_folder"]=input("Vnesi pot do mape z DEM-i: ")
    print("")


    while True:
        parametri["radij"]=input("Vnesi radij za Gaussov filter v pikslih. \n(za manjše strukture priporočljivo 20, za večje 40, odvisno sicer tudi od resolucije DEM-a): ")
        try:
            if 0<= float(parametri["radij"]) <=500:
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
        parametri["v_min"]=input("Vnesi minimalno vrednost za raztegnitev vrednosti pri vizualizaciji. \n(priporočljivo -1.5: ").replace(",",".")
        try:
            if -10<= float(parametri["v_min"]) <= 0:
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
        parametri["v_max"]=input("Vnesi maksimalno vrednost za raztegnitev vrednosti pri vizualizaciji. \n(priporočljivo 1.5: ").replace(",",".")
        try:
            if 0<= float(parametri["v_max"]) <=10:
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
    
    return(parametri)


def SLRM_glavna_rutina():
    parametri=input_rutine()
    dem_fajli_path=dobi_pathe_fajlov(parametri["dem_path_folder"])
    for i in dem_fajli_path:
        naredi_slrm(i,parametri["radij"],parametri["v_min"],parametri["v_max"], parametri["dem_path_folder"])
    print("")
    dem_pot_mapa=parametri["dem_path_folder"]
    print(f"Končal. Rezultati so v mapi {dem_pot_mapa}/Rezultati_SLRM")
    print("")