from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class HmsPatient(models.Model):
    _name = 'hms.patient'
    _description = 'Hospital Management System Patient'
    
    # Existing fields
    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    birthdate = fields.Date(string='Birthdate')
    history = fields.Html(string='History')
    cr_ratio = fields.Float(string='CR Ratio')
    blood_type = fields.Selection([
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-')
    ])
    pcr = fields.Boolean(string='PCR')
    image = fields.Image(string='Image')
    address = fields.Text(string='Address')
    age = fields.Integer(string='Age',compute='_compute_age',store=True)
    email = fields.Char(string='Email', required=True)
    department_id = fields.Many2one('hms.department', string='Department')
    department_capacity = fields.Integer(related='department_id.capacity')
    doctor_ids = fields.Many2many('hms.doctor', string='Doctors', readonly=True)
    customer_id = fields.Many2one('res.partner', string='Related Customer', ondelete='restrict')

    
    # New fields
    log_history_ids = fields.One2many(comodel_name='hms.log_history', inverse_name='patient_id', string='Log History')

    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], string='State', default='undetermined')
    
    @api.model
    def create(self, vals):
        patient = super(HmsPatient, self).create(vals)
        description = f"Patient {patient.first_name} {patient.last_name} created"
        patient.log_history_ids.create({
            'patient_id': patient.id,
            'description': description
        })
        return patient
    
    def write(self, vals):
        for patient in self:
            if 'state' in vals and vals['state'] != patient.state:
                description = f"State changed to {vals['state'].capitalize()}"
                patient.log_history_ids.create({
                    'patient_id': patient.id,
                    'description': description
                })
        return super(HmsPatient, self).write(vals)
    

    @api.depends('birthdate')
    def _compute_age(self):
        for rec in self:
            if rec.birthdate:
                today = date.today()
                rec.age = today.year - rec.birthdate.year - (
                (today.month, today.day) < (rec.birthdate.month, rec.birthdate.day))
            else:
                rec.age = 0


    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {
                "warning": {
                    "title": "Warning",
                    "message": "PCR is checked by default for patients with age less than 30",
                }
            }


    # @api.constrains('age')
    # def _check_age(self):
    #     if self.age <=0:
    #         raise ValidationError("Age should be more than zero")
    
    @api.constrains('email')
    def _check_valid_email(self):
        for record in self:
            if record.email:
                email_parts = record.email.split('@')
                if len(email_parts) != 2 or '.' not in email_parts[1] or email_parts[1].find('.') < 1:
                    raise ValidationError("Please enter a valid email address.")
                existing_patient = self.search([('email', '=', record.email), ('id', '!=', record.id)])
                if existing_patient:
                    raise ValidationError("Email address must be unique.")
