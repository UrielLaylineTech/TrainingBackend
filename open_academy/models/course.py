from odoo import models, fields, api

class course(models.Model):
    _name = 'open_academy.course'
    _description = "OpenAcademy Courses"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    
    
