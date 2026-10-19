# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
"""19.0 -> 20.0: access rules moved from ir.model.access to ir.access.

Odoo 20 loads security/ir.access.csv (model ir.access) with the same external
ids. The loader refuses to reuse an external id that still points to the
removed model ("found record of different model"); OpenUpgrade's base
migration drops them already, this keeps a plain update of an already
migrated database working too. Idempotent.
"""

import logging

_logger = logging.getLogger(__name__)

MODULE = "base_report_to_printer_cups"


def migrate(cr, version):
    cr.execute(
        "DELETE FROM ir_model_data"
        " WHERE module = %s AND model IN ('ir.model.access', 'ir.rule')",
        [MODULE],
    )
    if cr.rowcount:
        _logger.info(
            "%s: dropped %s legacy ir.model.access external ids", MODULE, cr.rowcount
        )
