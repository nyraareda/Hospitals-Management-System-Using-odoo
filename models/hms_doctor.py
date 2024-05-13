from odoo import models, fields

class Doctors(models.Model):
    _name = 'hms.doctor'
    _description = 'Doctors Information'

    first_name = fields.Char(string='First Name')
    last_name = fields.Char(string='Last Name')
    image = fields.Image(string='Image')
    department_id = fields.Many2one('hms.department', string='Department')
    department_capacity = fields.Integer(related='department_id.capacity')
    patient_id = fields.Many2one('hms.patient', string='Patient')