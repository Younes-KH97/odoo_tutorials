from odoo import http
from odoo.http import request, Response
import json
import logging

_logger = logging.getLogger(__name__)

class ControllerName(http.Controller):
    
    @http.route('/api/v1/property', type='http', auth='none', csrf=False, methods=['POST'])
    def create_property(self):
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
    
            property = request.env['estate.property'].sudo().create(vals)
    
            return request.make_json_response(
                data={
                    'message': 'Property created successfully',
                    'id': property.id,
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
        
    @http.route('/api/v1/property', type='http', auth='none', csrf=False, methods=['GET'])
    def get_property(self):
        try:
            domain = [] 
            propertys = request.env['estate.property'].sudo().search(domain)
            result = propertys.read(["name", "expected_price", "state", "active"])
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
         
    
    @http.route('/api/v1/property/<int:property_id>', type='http', auth='none', csrf=False, methods=['GET'])
    def get_property(self, property_id):
        try:
            property = request.env['estate.property'].sudo().browse(property_id)
            if not property.exists():
                return Response(
                    json.dumps({'error': 'property not found'}),
                    status=404,
                    content_type='application/json'
                )

            data = {
                'name': property.name,
                'expected_price': property.expected_price,
                'state': property.state,
                'active': property.active,
                'date_availability': property.date_availability,
            }
            data = property.read()[0]


            return Response(
                json.dumps({'property': data}, default=str),
                status=200,
                content_type='application/json'
            )

        except Exception as e:
            _logger.exception('GET error: %s', str(e))
            return Response(
                json.dumps({'error': 'Failed to retrieve property', 'details': str(e)}),
                status=500,
                content_type='application/json'
            )
        
    @http.route('/api/v1/property/<int:property_id>', type='http', auth='none', csrf=False, methods=['PUT'])
    def update_property(self, property_id):
        try:
            args = request.httprequest.data.decode()
            values = json.loads(args)
            if not values:
                return Response(
                    json.dumps({'error': 'No input data provided'}),
                    status=400,
                    content_type='application/json'
                )
            property = request.env['estate.property'].sudo().browse(property_id)
            if not property.exists():
                return Response(
                    json.dumps({'error': 'property not found'}),
                    status=404,
                    content_type='application/json'
                )
    
            property.write(values)
    
            fields = ['id', 'name', 'state'] 
            data = property.read(fields)[0]
    
            return Response(
                json.dumps({'property': data}),
                status=200,
                content_type='application/json'
                )
    
        except Exception as e:
            _logger.exception('PUT error: %s', str(e))
            return Response(
                json.dumps({'error': 'Failed to update property', 'details': str(e)}),
                status=500,
                content_type='application/json'
            )

    @http.route('/api/v1/property/<int:property_id>', type='http', auth='none', csrf=False, methods=['DELETE'])
    def delete_property(self, property_id):
        try:
            property = request.env['estate.property'].sudo().browse(property_id)
            if not property.exists():
                return Response(
                    json.dumps({'error': 'property not found'}),
                    status=404,
                    content_type='application/json'
                )

            if property.state not in ('new', 'cancelled'):
                return Response(
                    json.dumps({'error': f'property with state {property.state} cannot be deleted'}),
                    status=400,
                    content_type='application/json'
                )

            property.unlink()
            return Response(
                json.dumps({'message': 'property deleted', 'id': property_id}),
                status=200,
                content_type='application/json'
            )

        except Exception as e:
            _logger.exception('DELETE error: %s', str(e))
            return Response(
                json.dumps({'error': 'Deletion failed', 'details': str(e)}),
                status=500,
                content_type='application/json'
            )


    @http.route('/api/v2/property', type='http', auth='none', csrf=False, methods=['POST'])
    def create_property(self, **kw):
        try:
            args = request.httprequest.data.decode()
            values = json.loads(args)
            if not values:
                return Response(
                    json.dumps({'error': 'No input data provided'}),
                    status=400,
                    content_type='application/json'
                )
            elif not values.get("name") or not values.get("expected_price") or not values.get("state"):
                return Response(
                    json.dumps({'error': 'name, expected_price,  state are required'}),
                               status=400,
                               content_type='application/json'
                            )
            else:
                property = request.env['estate.property'].sudo().create(values)

                data = {
                    'id': property.id,
                    'name': property.name,
                    'state': property.state,
                    # Add other fields as needed
                }

                return Response(
                    json.dumps({'property': data}),
                    status=201,
                    content_type='application/json'
                )

        except Exception as e:
            _logger.exception('POST error: %s', str(e))
            return Response(
                json.dumps({'error': 'Failed to create property', 'details': str(e)}),
                status=500,
                content_type='application/json'
            )

