import postgresql
import numpy as np

class DataBase:
    def __init__(self):
        self.db = postgresql.open('pq://elyha7:5791855A@localhost:5432/elyha7')
    def add_to_db(self,vec,name,check = True):
        """
            Adds new vector to db.
            Params:
                vec - float32 array of size 512
                name - full name of person to add
                check - whether to check if person already in db before insert
        """
        if check:
            if self.find_closest(vec)[0] == 1:
                return (-1,'user already in db')
        ins = self.db.prepare("INSERT INTO users (name, vector) VALUES ($1, $2)")
        ins(name,vec)
        return (1,'added successfully')
    def find_closest(self,unknown_vec,threshold = 0.35):
        """
            Find name of a person with closest vector if vector distance is more than threshold.
            Params:
                unknown_vec - float32 array of size 512 with new vector to compare
                threshold - minimal cosine distance between vecs for match.
            Returns:
                (error code,message), message - name of a person or unknown, error code - int
        """
        names = self.db.query("SELECT trim(name) from users")
        if len(names) <1:
            return (-2,'empty db')
        vecs = np.array(self.db.query("SELECT vector from users"))
        if len(names)>1:
            vecs = np.squeeze(vecs)
        distances = [np.dot(i,unknown_vec.T) for i in vecs]
        print(len(distances))
        if np.max(distances)>threshold:
            match = (1,names[np.argmax(distances)][0])
        else:
            match = (-3,'unknown')
        return match
    def clear_db(self):
        try:
            self.db.query("TRUNCATE table users")
            return (1,'db cleared')
        except:
            return (-1,'cant clear db')