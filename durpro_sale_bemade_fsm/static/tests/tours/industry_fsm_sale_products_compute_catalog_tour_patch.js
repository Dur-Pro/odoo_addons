/** @odoo-module **/
import { registry } from "@web/core/registry";
import { patch } from "@web/core/utils/patch";

/*
Patch the last step in the industry_fsm_sale tour that makes sure there is a "Quotations" breadcrumb. We have
renamed the action "Quotations" to "Sales Orders" in the durpro_sale module.
 */
patch(registry.category("web_tour.tours").get("industry_fsm_sale_products_compute_catalog_tour"),
    {
        steps() {
            const originalSteps = super.steps();
            originalSteps.splice(-1, 1, {
                trigger: '.breadcrumb-item :contains("Sales Orders")',
                content: 'Go back to the quotations',
                isCheck: true,
            });
            return originalSteps;
        }
});
