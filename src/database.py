from flask_sqlalchemy import SQLAlchemy
from random import randint
db = SQLAlchemy()

class Queue:

    def __init__(self):
        self._queue = []
        # depending on the _mode, the queue has to behave like a FIFO or LIFO
        self._mode = 'FIFO'
    
    def _generateId(self):
        return randint(0, 99999999)

    def enqueue(self, person):
        person["id"] = self._generateId()
        self._queue.append(person)


    def dequeue(self):
                
                remove = self._queue.pop(0)
                return remove
                

    def get_queue(self):      
                return self._queue
    

    def delete_queue(self, name):
          for x in range(len(self._queue)):
            if self._queue[x]["name"] == name:       
                self._queue.pop(x)



    def size(self):
        return len(self._queue)
    



    
