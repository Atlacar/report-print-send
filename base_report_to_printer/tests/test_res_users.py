# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import AccessError
from odoo.tests import common


class TestResUsers(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.user_vals = {"name": "Test", "login": "login"}

    def new_record(self):
        return self.env["res.users"].create(self.user_vals)

    def test_available_action_types_excludes_user_default(self):
        """It should not contain `user_default` in avail actions"""
        self.user_vals["printing_action"] = "user_default"
        with self.assertRaises(ValueError):
            self.new_record()

    def test_available_action_types_includes_something_else(self):
        """It should still contain other valid keys"""
        self.user_vals["printing_action"] = "server"
        self.assertTrue(self.new_record())

    def test_user_can_write_own_printing_preferences(self):
        """A plain internal user may set their own printing preferences"""
        user = self.new_record()
        printer = self.env["printing.printer"].create(
            {"name": "Printer", "system_name": "Sys Name", "uri": "URI"}
        )
        user.with_user(user).write(
            {"printing_action": "server", "printing_printer_id": printer.id}
        )
        self.assertEqual(user.printing_action, "server")
        self.assertEqual(user.printing_printer_id, printer)
        with self.assertRaises(AccessError):
            user.with_user(user).write({"login": "other_login"})

    def test_onchange_printer_tray_id_empty(self):
        user = self.env["res.users"].new(
            {
                "printer_input_tray_id": False,
                "printer_output_tray_id": False,
            }
        )
        user.onchange_printing_printer_id()
        self.assertFalse(user.printer_input_tray_id)
        self.assertFalse(user.printer_output_tray_id)
