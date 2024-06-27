from odoo import models, fields, api
import random
import string


class ResPartner(models.Model):
    _inherit = 'res.partner'


    user_type = fields.Selection([
        ('lecture', 'Lecture'),
        ('student', 'Student')
    ], required=True)
    date_of_birth = fields.Date(string='Date of Birth')
    experience = fields.Integer('Years of Experience')
    token = fields.Char(string='Token', readonly=True)

    @api.model
    def create(self, vals):
        vals['token'] = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        return super(ResPartner, self).create(vals)
