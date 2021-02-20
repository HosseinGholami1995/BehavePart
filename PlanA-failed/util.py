import pandas as pd
import time
import pickle
from fastdtw import fastdtw

with open("Model_param.txt", "rb") as fp:
        Model_param = pickle.load(fp)

    
def Get_function():
    #exported from Behave part II
    windowF={
            226/2:[Harsh_Turn_Right,Harsh_Turn_Left,Harsh_acceleration],
            126/2:[Harsh_ChangeLine_Right,Harsh_ChangeLine_Left],
            186/2:[Harsh_Break]
           }
    return windowF


def read_data(num):
    with open("Data/data_list_per_driver", "rb") as fp:
        Sensory_data = pickle.load(fp)
    return Sensory_data[num]
    

# A thread that produces data 
def mQuarter(num):
    return round(num/40)
def ADC_Reader_Windowing(id_,que , df):
    pointer=-1
    X=dict()
    for name in list(que.keys()):
        X.update({name:pd.DataFrame()})
    while True:
        pointer+=1
        #shart khrooj
        if pointer==len(df):
            break;
        #mikhone har satr ro in hammon adc hast
        el=df.iloc[pointer]
        #michine to list 
        for name in X:
            X[name]=X[name].append(el)
        #check mikone list por shode ya na va be andaze 1/4 aval mirize door
        for name in X:
            xi=X[name]
            if len(xi)==name:
                que[name].put(xi)        
                X[name]=xi[mQuarter(name):]
    time.sleep(1)
    
    Data='{"driver_id":'+str(id_)+',"end"}'
    print(Data)
    

def Event_Handler(id_,que_input,function_pack):
    i=-1
    time.sleep(3)
    Data='{"driver_id":'+str(id_)+',"started"}'
    print(Data)
    
    while True: 
        i+=1
        # Get some data 
        data = que_input.get()
        # Process the data
        for func in function_pack:
            if func(data):
                Data='{"driver_id":'+str(id_)+',"timestamp":"'+str(data.index[-1])+'","event":"'+str(func.__name__)+'"}'
                print(Data)
  
        # Indicate completion 
        que_input.task_done()
        # print('.',end='')


        


def Harsh_Turn_Right(input_df,Model_param=Model_param['curva_direita_agressiva']):
    r1=4
    x1=fastdtw(input_df,Model_param[r1][1])[0]
    if x1<=Model_param[r1][0]:
        return True
    else:
        r2=1
        x2=fastdtw(input_df,Model_param[r2][1])[0]
        if x2<=Model_param[r2][0]:
            r3=5
            x3=fastdtw(input_df,Model_param[r3][1])[0]
            if x3<=Model_param[r3][0]:
                return True
            else:
                return False
        else:
            r3=6
            x3=fastdtw(input_df,Model_param[r3][1])[0]
            if x3<=Model_param[r3][0]:
                return True
            else:
                return False

def Harsh_Turn_Left(input_df,Model_param=Model_param['curva_esquerda_agressiva']):
    r1=4
    x1=fastdtw(input_df,Model_param[r1][1])[0]
    if x1<=Model_param[r1][0]:
        return True
    else:
        r2=5
        x2=fastdtw(input_df,Model_param[r2][1])[0]
        if x2<=Model_param[r2][0]:
            r3=9
            x3=fastdtw(input_df,Model_param[r3][1])[0]
            if x3<=Model_param[r3][0]:
                return True
            else:
                return False
        else:
            r3=8
            x3=fastdtw(input_df,Model_param[r3][1])[0]
            if x3<=Model_param[r3][0]:
                return True
            else:
                return False
def Harsh_acceleration(input_df,Model_param=Model_param['aceleracao_agressiva']):
    r1=4
    x1=fastdtw(input_df,Model_param[r1][1])[0]
    if x1<=Model_param[r1][0]:
        return True
    else:
        r2=3
        x2=fastdtw(input_df,Model_param[r2][1])[0]
        if x2<=Model_param[r2][0]:
            return True
        else:
            r3=1
            x3=fastdtw(input_df,Model_param[r3][1])[0]
            if x3<=Model_param[r3][0]:
                return True
            else:
                return False
def Harsh_ChangeLine_Right(input_df,Model_param=Model_param['troca_faixa_direita_agressiva']):
    r1=1
    x1=fastdtw(input_df,Model_param[r1][1])[0]
    if x1<=323.87:
        return True
    else:
        r2=0
        x2=fastdtw(input_df,Model_param[r2][1])[0]
        if x2<=Model_param[r2][0]:
            r3=1
            x3=fastdtw(input_df,Model_param[r3][1])[0]
            if x3<=Model_param[r3][0]:
                return True
            else:
                return False
        else:
            return False
def Harsh_ChangeLine_Left(input_df,Model_param=Model_param['troca_faixa_esquerda_agressiva']):
    r1=3
    x1=fastdtw(input_df,Model_param[r1][1])[0]
    if x1<=Model_param[r1][0]:
        r2=1
        x2=fastdtw(input_df,Model_param[r2][1])[0]
        if x2<=511.02:
            r3=0
            x3=fastdtw(input_df,Model_param[r3][1])[0]
            if x3<=Model_param[r3][0]:
                return True
            else:
                return False
        else:
            return True
    else:

        r2=1
        x2=fastdtw(input_df,Model_param[r2][1])[0]
        if x2<=837.11:
            r3=1
            x3=fastdtw(input_df,Model_param[r3][1])[0]
            if x3<=408.96:
                return True
            else:
                return False
        else:
            r3=2
            x3=fastdtw(input_df,Model_param[r3][1])[0]
            if x3<=Model_param[r3][0]:
                return True
            else:
                return False
def Harsh_Break(input_df,Model_param=Model_param['freada_agressiva']):
    r1=3
    x1=fastdtw(input_df,Model_param[r1][1])[0]
    if x1<=Model_param[r1][0]:
            return True
    else:
        r2=2
        x2=fastdtw(input_df,Model_param[r2][1])[0]
        if x2<=Model_param[r2][0]:
            return True
        else:
            r3=6
            x3=fastdtw(input_df,Model_param[r3][1])[0]
            if x3<=Model_param[r3][0]:
                return True
            else:
                return False
import winsound
def end ():
    for i in range (3):
        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 500  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)
        frequency = 500  # Set Frequency To 2500 Hertz
        duration = 500  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)
        frequency = 1000  # Set Frequency To 2500 Hertz
        duration = 500  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)
    frequency = 1000  # Set Frequency To 2500 Hertz
    duration = 5000  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)
