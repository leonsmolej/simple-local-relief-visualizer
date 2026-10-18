from SLRM import glavna_rutina, input_rutine

if __name__=="__main__":
    
    input_func=input_rutine()

    glavna_rutina(*input_func)