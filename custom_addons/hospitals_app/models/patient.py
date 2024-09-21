from odoo import models, fields, api
from dateutil.relativedelta import  relativedelta


class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient'
    _rec_name = 'first_name'

    first_name = fields.Char()
    last_name = fields.Char()
    birth_date = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float(string='CR Ratio')
    blood_type = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O')
    ])
    pcr = fields.Boolean(string='PCR')
    image = fields.Binary()
    address = fields.Text()
    age = fields.Integer(compute='_compute_age')

    department_id = fields.Many2one('hms.department', domain="[('is_opened', '=', 'True')]")
    doctor_ids = fields.Many2many('hms.doctor', readonly=True)
    department_capacity = fields.Integer(related='department_id.capacity', readonly=True)
    log_history = fields.One2many('hms.patient.log', 'patient_id')


    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], default='undetermined')

    """
    crud
    1. create => create(self, vals)
    2. read => _search(self, args, offset=0, limit=None, order=None) -> odoo 17 -> use _
    3. update => write(self, vals)
    4. delete => unlink(self)
    """

    # @api.model
    # def create(self, vals):
    #     res = super(Patient, self).create(vals)
    #     print('inside create ')
    #     return res
    #
    # @api.model
    # def _search(self, args, offset=0, limit=None, order=None):
    #     res = super(Patient, self)._search(args)
    #     print('inside _search ')
    #     return  res
    #
    # def write(self, vals):
    #     res = super(Patient, self).write(vals)
    #     print('inside write ')
    #     return  res
    #
    # def unlink(self):
    #     res = super(Patient, self).unlink()
    #     print('inside unlink ')
    #     return  res

    """
    actions
    """
    def action_undetermined(self):
        # self.state = 'undetermined'
        self.write({'state': 'undetermined'})
        self.env['hms.patient.log'].create({
            'patient_id': self.id,
            'description': 'State changed to Undetermined'
        })

    def action_good(self):
        # self.state = 'good'
        self.write({'state': 'good'})
        self.env['hms.patient.log'].create({
            'patient_id': self.id,
            'description': 'State changed to Good'
        })

    def action_fair(self):
        # self.state = 'fair'
        self.write({'state': 'fair'})
        self.env['hms.patient.log'].create({
            'patient_id': self.id,
            'description': 'State changed to Fair'
        })

    def action_serious(self):
        # self.state = 'serious'
        self.write({'state': 'serious'})
        self.env['hms.patient.log'].create({
            'patient_id': self.id,
            'description': 'State changed to Serious'
        })

    """
    METHODS DECORATORS
    """
    @api.depends('birth_date')
    def _compute_age(self):
        for patient in self:
            if patient.birth_date:
                patient.age = relativedelta(fields.Date.today(), patient.birth_date).years
            else:
                patient.age = 0


    @api.onchange('pcr')
    def _onchange_pcr(self):
        print('self', self) #
        if self.pcr:
            self.cr_ratio = False
        else:
            self.cr_ratio = None

    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 30:
            self.pcr = True

        if self.age < 50:
            self.history = False


    """
    Wizard
    """
    def action_add_history_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hsm.add.history',
            'view_mode': 'form',
            'view_id': self.env.ref('hospitals_app.add_history_form_view').id,
            'target': 'new',
            'context': {'default_patient_id': self.id},
        }
        #
        # action = self.env['ir.actions.actions']._for_xml_id('hospitals_app.add_history_action')
        # action['context'] = {'default_patient_id': self.id}
        # return action
        #
        # action = self.env['ir.actions.actions']._for_xml_id('hospitals_app.add_history_action')
        # action['context'] = {
        #     'default_patient_id': self.id
        # }
        # return action


class PatientLog(models.Model):
    _name = 'hms.patient.log'
    _description = 'Patient Log'

    patient_id = fields.Many2one('hms.patient')
    # created_by = fields.Many2one('res.users', default=lambda self: self.env.user)
    date = fields.Datetime(default=fields.Datetime.now)
    description = fields.Text()

