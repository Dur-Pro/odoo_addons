from odoo import fields, models, api


class HrEmployee(models.Model):
    """Add the group hr.group_hr_user to the fields added in hr_attendance/models/hr_employee.py to match the
    recommendation at hr/models/hr_employee.py:22"""
    _inherit = "hr.employee"

    attendance_ids = fields.One2many(
        'hr.attendance', 'employee_id', groups="hr_attendance.group_hr_attendance_user,hr.group_hr_user",
        help='list of attendances for the employee')
    last_attendance_id = fields.Many2one(
        'hr.attendance', compute='_compute_last_attendance_id', store=True,
        groups="hr_attendance.group_hr_attendance_kiosk,hr_attendance.group_hr_attendance,hr.group_hr_user")
    last_check_in = fields.Datetime(
        related='last_attendance_id.check_in', store=True,
        groups="hr_attendance.group_hr_attendance_user,hr.group_hr_user")
    last_check_out = fields.Datetime(
        related='last_attendance_id.check_out', store=True,
        groups="hr_attendance.group_hr_attendance_user,hr.group_hr_user")
    attendance_state = fields.Selection(
        string="Attendance Status", compute='_compute_attendance_state',
        selection=[('checked_out', "Checked out"), ('checked_in', "Checked in")],
        groups="hr_attendance.group_hr_attendance_kiosk,hr_attendance.group_hr_attendance,hr.group_hr_user")
    hours_last_month = fields.Float(
        compute='_compute_hours_last_month', groups="hr_attendance.group_hr_attendance_user,hr.group_hr_user")
    hours_today = fields.Float(
        compute='_compute_hours_today',
        groups="hr_attendance.group_hr_attendance_kiosk,hr_attendance.group_hr_attendance,hr.group_hr_user")
    hours_last_month_display = fields.Char(
        compute='_compute_hours_last_month', groups="hr_attendance.group_hr_attendance_user,hr.group_hr_user")
    overtime_ids = fields.One2many(
        'hr.attendance.overtime', 'employee_id', groups="hr_attendance.group_hr_attendance_user,hr.group_hr_user")
    total_overtime = fields.Float(
        compute='_compute_total_overtime', compute_sudo=True,
        groups="hr_attendance.group_hr_attendance_kiosk,hr_attendance.group_hr_attendance,hr.group_hr_user")
