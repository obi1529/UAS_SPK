import sys

from colorama import Fore, Style
from models import Base, Smartphone
from engine import engine

from sqlalchemy import select
from sqlalchemy.orm import Session
from settings import MEREK_SCALE, PROCESSOR_SCALE, VERSI_OS_SCALE

session = Session(engine)

def create_table():
    Base.metadata.create_all(engine)
    print(f'{Fore.GREEN}[Success]: {Style.RESET_ALL}Database has created!')

class BaseMethod():

    def __init__(self):
        # 1-5 (Kriteria)
        self.raw_weight = {
            'merek': 3,
            'ram': 5,
            'processor': 4,
            'versi_os': 1,
            'battery': 3,
            'harga': 4,
            'layar': 2
        }

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {c: round(w/total_weight, 2) for c,w in self.raw_weight.items()}

    @property
    def data(self):
        query = select(Smartphone)
        return [{
            'id': smartphone.id,
            'merek': MEREK_SCALE["".join([x for x in MEREK_SCALE.keys() if x.lower() in smartphone.merek.lower()])],
            'ram': smartphone.ram,
            'processor': PROCESSOR_SCALE[smartphone.processor],
            'versi_os': VERSI_OS_SCALE[smartphone.versi_os],
            'battery': smartphone.battery,
            'harga': smartphone.harga,
            'layar': smartphone.layar
        } for smartphone in session.scalars(query)]

    @property
    def normalized_data(self):
        # x/max [benefit]
        # min/x [cost]

        merek = [] # max
        ram = [] # max
        processor = [] # max
        versi_os = [] # max
        battery = [] # max
        harga = [] # min
        layar = [] # max

        for data in self.data:
            merek.append(data['merek'])
            ram.append(data['ram'])
            processor.append(data['processor'])
            versi_os.append(data['versi_os'])
            battery.append(data['battery'])
            harga.append(data['harga'])
            layar.append(data['layar'])

        max_merek = max(merek)
        max_ram = max(ram)
        max_processor = max(processor)
        max_versi_os = max(versi_os)
        max_battery = max(battery)
        min_harga = min(harga)
        max_layar = max(layar)

        return [{
            'id': data['id'],
            'merek': data['merek']/max_merek, # benefit
            'ram': data['ram']/max_ram, # benefit
            'processor': data['processor']/max_processor, # benefit
            'versi_os': data['versi_os']/max_versi_os, # benefit
            'battery': data['processor']/max_battery, # benefit
            'harga': min_harga/data['harga'], # cost
            'layar': data['layar']/max_layar # benefit
        } for data in self.data]
 

class WeightedProduct(BaseMethod):
    @property
    def calculate(self):
        weight = self.weight
        # calculate data and weight[WP]
        result = {row['id']:
            round(
                row['merek'] ** weight['merek'] *
                row['ram'] ** weight['ram'] *
                row['processor'] ** weight['processor'] *
                row['versi_os'] ** weight['versi_os'] *
                row['battery'] ** weight['battery'] *
                row['harga'] ** (-weight['harga']) *
                row['layar'] ** weight['layar']
                , 2
            )

            for row in self.normalized_data}
        #sorting
        # return result
        return dict(sorted(result.items(), key=lambda x:x[1]))

class SimpleAdditiveWeighting(BaseMethod):
    
    @property
    def calculate(self):
        weight = self.weight
        # calculate data and weight
        result =  {row['id']:
            round(
                row['merek'] * weight['merek'] +
                row['ram'] * weight['ram'] +
                row['processor'] * weight['processor'] +
                row['versi_os'] * weight['versi_os'] +
                row['battery'] * weight['battery'] +
                row['harga'] * weight['harga'] +
                row['layar'] * weight['layar']
                , 2
            )
            for row in self.normalized_data
        }
        # sorting
        return dict(sorted(result.items(), key=lambda x:x[1]))

def run_saw():
    saw = SimpleAdditiveWeighting()
    print('result:', saw.calculate)

def run_wp():
    wp = WeightedProduct()
    print('result:', wp.calculate)

if len(sys.argv)>1:
    arg = sys.argv[1]

    if arg == 'create_table':
        create_table()
    elif arg == 'saw':
        run_saw()
    elif arg =='wp':
        run_wp()
    else:
        print('command not found')
