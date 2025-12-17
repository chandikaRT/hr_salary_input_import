from odoo import models, fields

class HrSalaryInputImport(models.Model):
    _name = 'hr.salary.input.import'
    _description = 'Temporary Salary Inputs from Excel'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    input_name = fields.Char(string='Input Name', required=True)
    amount = fields.Float(string='Amount', required=True)
    payslip_id = fields.Many2one('hr.payslip', string='Payslip')
    state = fields.Selection([('draft','Draft'), ('imported','Imported')], default='draft')

    def write(self, vals):
        # Make record read-only after imported
        if self.state == 'imported':
            raise ValueError("This record is read-only.")
        return super(HrSalaryInputImport, self).write(vals)
