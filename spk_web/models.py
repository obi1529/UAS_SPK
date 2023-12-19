import numpy
import pandas
from spk import WeightedProduct, SimpleAdditiveWeighting

class Database():
    def __init__(self) -> None:
        self.database = pandas.read_csv('database/spk_obi_agustian.csv')
        self.smartphone = numpy.array(self.database)

    @property
    def database_data(self):
        data = []
        for phone in self.smartphone:
            data.append({
                'id': phone[0],
                'Merek': phone[1],
                'ram': phone[2],
                'processor': phone[3],
                'versi_os': phone[4],
                'battery': phone[5],
                'harga': phone[6],
                'layar': phone[7]
            })
        return data

    @property
    def database_data_dict(self):
        data = {}
        for phone in self.smartphone:
            data[phone[0]] = phone[1] 
        return data

    def get_recs(self, criteria:dict):
        if 'mode' not in criteria: criteria['mode'] = 'wp'
        mode = criteria['mode']
        if mode == "wp":
            del criteria['mode']
            wp = WeightedProduct(self.database.to_dict(orient="records"), criteria)
            return wp.calculate
        elif mode == "saw":
            del criteria['mode']
            saw = SimpleAdditiveWeighting(self.database.to_dict(orient="records"), criteria)
            return saw.calculate
        else: return False

