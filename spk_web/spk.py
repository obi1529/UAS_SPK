from settings import MEREK_SCALE, PROCESSOR_SCALE, VERSI_OS_SCALE

class BaseMethod():
    def __init__(self, data_dict, **setCriteria):

        self.database = data_dict

        # 1-7 (Kriteria)
        self.raw_weight = {
            'merek': 6,
            'ram': 5,
            'processor': 4,
            'versi_os': 1,
            'battery': 3,
            'harga': 7,
            'layar': 2
        }

        if setCriteria:
            for item in setCriteria.items():
                temp1 = setCriteria[item[0]] # Backup value (int)
                temp2 = {v: k for k, v in setCriteria.items()}[item[1]] # Reverse key-value dan backup value (str)

                setCriteria[item[0]] = item[1] # Replace dan restore value (int)
                setCriteria[temp2] = temp1 # Replace dan restore value (str)

    # Perhitungan Bobot
    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {c: round(w/total_weight, 2) for c,w in self.raw_weight.items()}

    # Data dari CSV
    @property
    def data(self):
        return [{
            'id': smartphone['id'],
            'merek': MEREK_SCALE["".join([x for x in MEREK_SCALE.keys() if x.lower() in smartphone['merek'].lower()])],
            'ram': smartphone['ram'],
            'processor': PROCESSOR_SCALE[smartphone['processor']],
            'versi_os': VERSI_OS_SCALE[smartphone['versi_os']],
            'battery': smartphone['battery'],
            'harga': smartphone['harga'],
            'layar': smartphone['layar']
        } for smartphone in self.database]

    # Tahap Normalisasi
    @property
    def normalized_data(self):
        # x/max [benefit]
        # min/x [cost]

        # Bikin List buat diisi CSV
        merek = [] # max
        ram = [] # max
        processor = [] # max
        versi_os = [] # max
        battery = [] # max
        harga = [] # min
        layar = [] # max

        # Tambah data dari CSV ke List
        for data in self.data:
            merek.append(data['merek'])
            ram.append(data['ram'])
            processor.append(data['processor'])
            versi_os.append(data['versi_os'])
            battery.append(data['battery'])
            harga.append(data['harga'])
            layar.append(data['layar'])

        # Nilai tertinggi dan terendah
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
    def __init__(self, dataDict, setCriteria:dict):
        super().__init__(data_dict=dataDict, **setCriteria)

    @property
    def calculate(self):
        weight = self.weight

        # Perhitungan WP
        result = {row['id']:
            round(
                row['merek'] ** weight['merek'] *
                row['ram'] ** weight['ram'] *
                row['processor'] ** weight['processor'] *
                row['versi_os'] ** weight['versi_os'] *
                row['battery'] ** weight['battery'] *
                row['harga'] ** (-weight['harga']) *
                row['layar'] ** weight['layar']
                , 3
            )

            for row in self.normalized_data}

        # Sorting
        totalResult = sum(result.values())
        for resultKey in result.keys():
            result[resultKey] = round(result[resultKey]/totalResult, 3)

        # Hasil WP
        return dict(sorted(result.items(), key=lambda id:id[1], reverse=True))

class SimpleAdditiveWeighting(BaseMethod):
    def __init__(self, dataDict, setCriteria:dict):
        super().__init__(data_dict=dataDict, **setCriteria)

    @property
    def calculate(self):
        weight = self.weight

        # Perhitungan SAW
        result =  {row['id']:
            round(
                row['merek'] * weight['merek'] +
                row['ram'] * weight['ram'] +
                row['processor'] * weight['processor'] +
                row['versi_os'] * weight['versi_os'] +
                row['battery'] * weight['battery'] +
                row['harga'] * weight['harga'] +
                row['layar'] * weight['layar']
                , 3
            )
            for row in self.normalized_data
        }

        # Sorting dan Hasilnya
        return dict(sorted(result.items(), key=lambda id:id[1], reverse=True))
