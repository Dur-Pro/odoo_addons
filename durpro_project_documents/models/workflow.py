from odoo import models, fields, Command


class WorkflowActionRuleSign(models.Model):
    _inherit = 'documents.workflow.rule'

    def create_record(self, documents=None):
        res = super().create_record(documents=documents)
        # res will be either:
        #   - an action to view a list of sign.template in Kanban with the template
        #     ids in the domain at index [0][2] ... domain = [('id', 'in', template_ids)]
        #   - a client action with a single sign.template id in context as 'id'
        #   - None
        if res:
            if 'domain' in res:
                template_ids = res['domain'][0][2]
            else:
                template_ids = [res['context']['id']]
            ctx = self._context
            if 'project_id' in ctx:
                templates = self.env['sign.template'].browse(template_ids)
                project = self.env['project.project'].browse(ctx.get('project_id'))
                templates.project_id = project
        return res
