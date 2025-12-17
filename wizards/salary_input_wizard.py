import base64
import io
import pandas as pd
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HrSalaryInputWizard(models.TransientModel):
    _name = 'hr.salary.input.wizard'
    _description = 'Upload Salary Inputs from Excel'

    excel_file = fields.Binary('Excel File', required=True)
    file_name = fields.Char('File Name')

    def action_preview(self):
        if not self.excel_file:
            raise UserError(_("Please upload an Excel file."))
        
        data = base64.b64decode(self.excel_file)
        df = pd.read_excel(io.BytesIO(data))

        # Required columns: employee_name, input_name, amount
        required_cols = ['employee_name','input_name','amount']
        if not all(col in df.columns for col in required_cols):
            raise UserError(_("Excel file must contain columns: %s") % ', '.join(required_cols))

        temp_records = []
        for index, row in df.iterrows():
            employee = self.env['hr.employee'].search([('name','=',row['employee_name'])], limit=1)
            if not employee:
                raise UserError(_("Employee with name '%s' not found.") % row['employee_name'])
            temp_records.append({
                'employee_id': employee.id,
                'input_name': row['input_name'],
                'amount': row['amount'],
            })

        # Clear previous temp records
        self.env['hr.salary.input.import'].search([]).unlink()
        self.env['hr.salary.input.import'].create(temp_records)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Preview Salary Inputs',
            'res_model': 'hr.salary.input.import',
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def action_import(self):
        temp_records = self.env['hr.salary.input.import'].search([('state','=','draft')])
        if not temp_records:
            raise UserError(_("No data to import."))

        for record in temp_records:
            payslip = self.env['hr.payslip'].search([
                ('employee_id','=',record.employee_id.id),
                ('state','=','draft')
            ], limit=1)
            if not payslip:
                continue

            # Update or create input line
            input_line = payslip.input_line_ids.filtered(lambda l: l.name == record.input_name)
            if input_line:
                input_line.write({'amount': record.amount})
            else:
                self.env['hr.payslip.input'].create({
                    'name': record.input_name,
                    'amount': record.amount,
                    'contract_id': payslip.contract_id.id,
                    'slip_id': payslip.id,
                })
            # Mark temp record as imported
            record.state = 'imported'
