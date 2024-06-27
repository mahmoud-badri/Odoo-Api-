from odoo import http, fields
from odoo.http import request
import re
import json
from datetime import datetime
import logging
from odoo.tools import html2plaintext



class PartnerAPI(http.Controller):

    @http.route('/register_partner', type='http', auth='none', methods=['POST'], csrf=False)
    def register_partner(self):
        try:
            raw_data = request.httprequest.data.decode()
            data = json.loads(raw_data)

            name = data.get('name')
            phone = data.get('phone')
            user_type = data.get('user_type')
            date_of_birth = data.get('date_of_birth', False)

            if not name:
                return request.make_json_response({
                    "error": "Name is required"
                }, status=400)
            if not phone or not re.match(r'^966\d{9}$', phone):
                return request.make_json_response({
                    "error": "Phone number is invalid. It must be 12 digits and start with 966"
                }, status=400)
            if not user_type or user_type not in ['lecture', 'student']:
                return request.make_json_response({
                    "error": 'User type must be either "lecture" or "student"'
                }, status=400)

            vals = {
                'name': name,
                'phone': phone,
                'user_type': user_type,
                'date_of_birth': date_of_birth,
            }

            try:
                partner = request.env['res.partner'].sudo().create(vals)
                return request.make_json_response({
                    "message": "Partner created successfully",
                    "token": partner.token
                }, status=200)
            except Exception as e:
                return request.make_json_response({
                    "error": str(e)
                }, status=500)

        except ValueError:
            return request.make_json_response({
                "error": "Invalid JSON data"
            }, status=400)
        except KeyError as e:
            return request.make_json_response({
                "error": f"Missing required field: {str(e)}"
            }, status=400)
        except Exception as error:
            return request.make_json_response({
                "error": f"An unexpected error occurred: {str(error)}"
            }, status=500)

    @http.route('/get_courses', type='http', auth='none', methods=['GET'], csrf=False)
    def get_courses(self):
        try:
            token = request.httprequest.headers.get('Token')
            if not token:
                return request.make_json_response({
                    "error": "Authorization token is required"
                }, status=401)

            partner = request.env['res.partner'].sudo().search([('token', '=', token)], limit=1)
            if not partner:
                return request.make_json_response({
                    "error": "Invalid token"
                }, status=401)

            courses = request.env['slide.channel'].sudo().search([])
            grouped_courses = {}

            for rec in courses:
                responsible = rec.user_id
                if responsible.id not in grouped_courses:
                    age = (
                                  datetime.now().date() - responsible.partner_id.date_of_birth).days // 365 if responsible.partner_id.date_of_birth else 0
                    grouped_courses[responsible.id] = {
                        'responsible_info': {
                            'name': responsible.name,
                            'age': age,
                            'years_of_experience': responsible.partner_id.experience
                        },
                        'courses': []
                    }

                course_info = {
                    'course_info': {
                        'id': rec.id,
                        'name': rec.name,
                        'description': html2plaintext(rec.description).strip(),
                        'total_views': rec.total_views,
                        'last_update': rec.write_date.strftime('%d/%m/%Y') if rec.write_date else '',
                        'img': rec.image_1920 and f"/web/image/slide.channel/{rec.id}/image_1920" or ''
                    },
                    'course_content': []
                }

                for content in rec.slide_ids:
                    course_info['course_content'].append({
                        'title': content.name,
                        'type': content.slide_type,
                        'url': content.url,
                        'duration': content.completion_time
                    })

                grouped_courses[responsible.id]['courses'].append(course_info)

            response_data = list(grouped_courses.values())
            return request.make_json_response(response_data, status=200)

        except Exception as error:
            return request.make_json_response({
                "error": f"An unexpected error occurred: {str(error)}"
            }, status=500)
