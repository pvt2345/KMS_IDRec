import pandas as pd
class Database:
    def __init__(self):
        self.data = {}
        self.header = {}

    def create_table(self,table,columns=None):
        if table not in self.data:
            self.data[table]=[]
            self.header[table]=columns

    def insert(self,record,table='content'):
        if table not in self.data:
            self.data[table]=[]
            self.header[table]=None
        id = len(self.data[table])
        record = record.copy()
        record['id']=id
        self.data[table].append(record)
        return id

    def to_excel(self,write,sheet='content'):
        print('save data to excel')
        for table,data in self.data.items():
            #['id','parent','type','stt','tieu_de','content']
            dt = pd.DataFrame.from_records(data,index=self.header[table])
            dt.to_excel(write,sheet_name=table)
        # write.close()
        print('done')
    def select(self,table):
        if table in self.data:
            return self.data[table].copy()
        else:
            return []
    def get_reference(self,id,table):
        if not table in self.data:
            return None
        for dt in self.data[table]:
            if dt['id'] and id == int(dt['id']):
                d = dt.copy()
                # print(d)
                return d
        return None
    def save(self):
        pass
