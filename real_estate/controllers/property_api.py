from odoo import http
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)

class ControllerName(http.Controller):

    @http.route('/api/v2/property', type='http', auth='none', csrf=False)
    def add_new_property(self , **kw):
        args = request.httprequest.data.decode() # from byte string to unicode
        print(args, "type", type(args))
        vals = json.loads(args)
        res = request.env['estate.property'].sudo().create(vals)
        if res:
            return request.make_json_response(data={
                "message": "Data loaded successfully"
            }, 
                                              headers=None, 
                                              cookies=None, 
                                              status=200)
    
    @http.route('/api/v1/property', type='http', auth='none', csrf=False, methods=['POST'])
    def create_record(self, **kw):
        try:
            raw_data = request.httprequest.data.decode('utf-8')
            _logger.info('Raw request data: %s', raw_data)
    
            vals = json.loads(raw_data)
    
            if not vals:
                return request.make_json_response(
                    data={
                        'error': 'No data received',
                        'status': 'fail'
                    },
                    status=400
                )
    
            record = request.env['estate.property'].sudo().create(vals)
    
            return request.make_json_response(
                data={
                    'message': 'Property created successfully',
                    'id': record.id,
                    'status': 'success'
                },
                status=201
            )
    
        except json.JSONDecodeError as e:
            _logger.error('JSON decode error: %s', str(e))
            return request.make_json_response(
                data={
                    'error': 'Invalid JSON format',
                    'status': 'fail'
                },
                status=400
            )
        except Exception as e:
            _logger.exception('Unexpected error: %s', str(e))
            return request.make_json_response(
                data={
                    'error': 'An unexpected error occurred',
                    'details': str(e),
                    'status': 'fail'
                },
                status=500
            )
        
    # Add pagination and some opt
    @http.route('/api/v1/property', type='http', auth='none', csrf=False, methods=['GET'])
    def get_records(self, **kw):
        try:
            domain = []  # Add domain filters if needed
            records = request.env['estate.property'].sudo().search(domain)
            result = records.read(["name", "expected_price", "state", "active"])
            return request.make_json_response({
                'status': 'success',
                'count': len(result),
                'data': result
            })
        except Exception as e:
            _logger.exception('GET error: %s', str(e))
            return request.make_json_response({
                'error': 'Unexpected error',
                'details': str(e)
            }, 500)
        
    @http.route('/api/v1/property/<int:record_id>', type='http', auth='none', csrf=False, methods=['PUT'])
    def update_record(self, record_id, **kw):
        try:
            data = request.httprequest.data.decode('utf-8')
            vals = json.loads(data)
            record = request.env['estate.property'].sudo().browse(record_id)
            if not record.exists():
                return request.make_json_response({'error': 'Record not found'}, 404)
            record.write(vals)
            return request.make_json_response({'message': 'Updated successfully', 'id': record.id})
        except Exception as e:
            request._logger.exception('PUT error: %s', str(e))
            return request.make_json_response({'error': 'Update failed', 'details': str(e)}, 500)
        
    @http.route('/api/v1/model/<int:record_id>', type='http', auth='none', csrf=False, methods=['DELETE'])
    def delete_record(self, record_id, **kw):
        try:
            record = request.env['estate.property'].sudo().browse(record_id)
            if not record.exists():
                return request.make_json_response({'error': 'Record not found'}, 404)
            record.unlink()
            return request.make_json_response({'message': 'Record deleted', 'id': record_id})
        except Exception as e:
            request._logger.exception('DELETE error: %s', str(e))
            return request.make_json_response({'error': 'Deletion failed', 'details': str(e)}, 500)
        
    
    # import logging
    # _logger = logging.getLogger(__name__)
    
    @http.route('/api/v1/property/<int:record_id>', type='http', auth='none', csrf=False, methods=['GET'])
    def get_one_record(self, record_id, **kw):
        try:
            model = 'estate.property'
            record = request.env['estate.property'].sudo().browse(record_id)
    
            if not record.exists():
                return request.make_json_response({
                    'error': 'Record not found',
                    'status': 'fail'
                }, 404)
    
            data = record.read(['field1', 'field2'])[0]
    
            return request.make_json_response({
                'status': 'success',
                'data': data
            }, 200)
    
        except Exception as e:
            _logger.exception('Failed to fetch record: %s', str(e))
            return request.make_json_response({
                'error': 'An unexpected error occurred',
                'details': str(e),
                'status': 'fail'
            }, 500)