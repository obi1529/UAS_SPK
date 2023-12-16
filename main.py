from http import HTTPStatus

from flask import Flask, request, abort
from flask_restful import Resource, Api 

from models import Database

app = Flask(__name__)
api = Api(app)


class ApiSmartphone(Resource):
    def get_paginated_result(self, url, list, args):
        page_size = int(args.get('page_size', 10))
        page = int(args.get('page', 1))
        page_count = int((len(list) + page_size - 1) / page_size)
        start = (page - 1) * page_size
        end = min(start + page_size, len(list))

        if page < page_count:
            next = f'{url}?page={page+1}&page_size={page_size}'
        else:
            next=None
        if page > 1:
            prev = f'{url}?page={page-1}&page_size={page_size}'
        else:
            prev = None

        if page > page_count or page < 1:
            abort(404, description = f'Halaman {page} tidak ditemukan.') 
        return  {
            'page': page,
            'page_size': page_size,
            'next': next,
            'prev': prev,
            'Results': list[start:end]
        }

    def get(self):
        db = Database()
        return self.get_paginated_result('smartphone/', db.database_data, request.args), HTTPStatus.OK.value


class Recommendation(Resource):

    def post(self):
        criteria = request.get_json()
        validCriteria = ['mode', 'merek', 'ram', 'processor', 'versi_os', 'battery', 'harga', 'layar']
        db = Database()

        if not criteria:
            return 'Kriteria kosong!', HTTPStatus.BAD_REQUEST.value

        if not all([v in validCriteria for v in criteria]):
            return 'Kriteria tidak ditemukan!', HTTPStatus.NOT_FOUND.value

        alternatives = db.get_recs(criteria)

        if not alternatives:
            return 'Mode tidak ditemukan!', HTTPStatus.NOT_FOUND.value

        results = [{"Merek": db.database_data_dict[rec[0]], "Score": rec[1]} for rec in alternatives.items()]

        return {
            'Alternatives': results
        }, HTTPStatus.OK.value


api.add_resource(ApiSmartphone, '/obi')
api.add_resource(Recommendation, '/spk')

if __name__ == '__main__':
    app.run(port='5005', debug=True)
