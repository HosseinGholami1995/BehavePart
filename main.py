from util import read_data , ADC_Reader_Windowing ,Event_Handler,Get_function
from threading import Thread 
from queue import Queue



class Node:
    que={   226*40:Queue(),
            186*40:Queue(),
            126*40:Queue()  }
        
    def __init__(self,driver_id):
        self.id=driver_id
    def start(self):
        id_=self.id        
        que=self.que
        df = read_data(id_)
        tp = Thread(target = ADC_Reader_Windowing, args =(id_,que , df ) )
        tp.start()
        for window in que:
            tc = Thread(target = Event_Handler, args =(id_,que[window],Get_function()[window])) 
            tc.start()

a=Node(31)
a.start()
# m=[(len(x),i) for i ,x in enumerate(Sensory_data)]
