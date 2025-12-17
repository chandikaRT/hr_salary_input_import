{
    'name': 'HR Salary Inputs Import',
    'version': '1.0',
    'summary': 'Import other inputs into salary slips from Excel',
    'description': 'Upload Excel files to add allowances and deductions to salary slips with preview and lock imported lines',
    'category': 'Human Resources/Payroll',
    'author': 'Chandika Rathnayake',
    'depends': ['hr_payroll'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu_views.xml',
        'views/salary_input_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
