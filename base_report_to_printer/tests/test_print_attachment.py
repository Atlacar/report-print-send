# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestPrintAttachment(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.printer = cls.env["printing.printer"].create(
            {"name": "Printer", "system_name": "Sys Name"}
        )
        cls.content = b"%PDF-1.4 attachment"
        cls.attachment = cls.env["ir.attachment"].create(
            {
                "name": "doc.pdf",
                "raw": cls.content,
                "mimetype": "application/pdf",
            }
        )

    def test_print_attachments_sends_raw_content(self):
        """The wizard prints the attachment bytes (ir.attachment.datas is gone)."""
        calls = []

        def capture(self, report, content, **kwargs):
            calls.append((content, kwargs))
            return True

        self.patch(type(self.printer), "print_document", capture)
        wizard = self.env["wizard.print.attachment"].create(
            {
                "printer_id": self.printer.id,
                "attachment_line_ids": [
                    (0, 0, {"attachment_id": self.attachment.id, "copies": 2})
                ],
            }
        )
        self.assertFalse(wizard.print_attachments())
        self.assertEqual(len(calls), 1)
        content, kwargs = calls[0]
        self.assertEqual(content, self.content)
        self.assertEqual(kwargs["format"], "pdf")
        self.assertEqual(kwargs["copies"], 2)
        self.assertEqual(kwargs["title"], "doc.pdf")
