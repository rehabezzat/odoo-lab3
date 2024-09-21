{
    "name": "Hospitals App",
    "summary": "Hospital Management System",
    "description": """Module for managing hospital patients""",
    "author": "Mazen Saad",
    "category": "",
    "version": "17.0.0.1.0",
    "depends": ['base'],
    "application": True,
    "data": [
        'security/ir.model.access.csv',
        'views/hospitals_menus.xml',
        'views/patient_view.xml',
        'views/department_view.xml',
        'views/doctor_view.xml',
        'wizard/add_history_wizard_view.xml',
    ]
}