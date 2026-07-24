from io import BytesIO
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

from reportlab.lib.styles import (
    getSampleStyleSheet,
)

from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.utils.pdf_footer import (    add_pdf_footer,)
class PDFRequisitionService:

    @staticmethod
    def generate_requisition_pdf(
        requisition,
        vehicle,
        technician,
        details,
        part_lookup,
    ):

        buffer = BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
        )

        styles = (
            getSampleStyleSheet()
        )

        elements = []

        elements.append(
            Paragraph(
                "PART REQUISITION",
                styles["Title"],
            )
        )

        elements.append(
            Spacer(1, 20)
        )
        status_color = colors.blue
        if requisition.status == "APPROVED":
            status_color = colors.green
        elif requisition.status == "ISSUED":
            status_color = colors.orange
        elif requisition.status == "CLOSED":
            status_color = colors.darkgreen

        header_data = [

            [
                "Requisition No",
                requisition.requisition_number,
            ],

            [
                "Date",
#                datetime.'requisition.requisition_date'.strftime(
#                                "%d-%b-%Y %H:%M"
#                            ),
                str(
                    requisition.requisition_date
                ),
            ],

            [
                "Vehicle",
                str(vehicle.rc_number)
                if vehicle
                else "-",
            ],

            [
                "Job Card",
                str(
                    requisition.job_card_id
                ),
            ],

            [
                "Technician",
                str(technician.full_name)
                if technician
                else "-",
            ],

            [
                "Status",
                Paragraph(
                    f'<font color="{status_color.hexval()}">{requisition.status}</font>',
                    styles["Normal"],
                )
#                requisition.status,
            ],
        ]

        header_table = Table(
            header_data,
            colWidths=[140, 350],
        )

        header_table.setStyle(
            TableStyle([
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black,
                ),

                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.lightgrey,
                ),
            ])
        )

        elements.append(
            header_table
        )

        elements.append(
            Spacer(1, 20)
        )

        elements.append(
            Paragraph(
                "Parts Requested",
                styles["Heading2"],
            )
        )

        part_rows = [[
            "Part Name",
            "Qty Required",
            "Qty Returned",
            "Required Serial",
            "Returned Serial",
        ]]

        total_required = 0
        total_returned = 0

        for detail in details:

            qty_required = float(
                detail.quantity_required or 0
            )

            qty_returned = float(
                detail.quantity_returned or 0
            )
            total_required += float(
                qty_required
            )

            total_returned += float(
                qty_returned
            )

            part_rows.append([
                part_lookup.get(
                    detail.part_id,
                    "-"
                ),
                f"{qty_required:.2f}",
                f"{qty_returned:.2f}",
                detail.required_serial_number
                or "-",
                detail.returned_serial_number
                or "-",
            ])

        part_table = Table(
            part_rows,
            colWidths=[
                130,
                80,
                80,
                110,
                110,
            ],
        )

        part_table.setStyle(
            TableStyle([

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black,
                ),

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey,
                ),

                (
                    "TEXTCOLOR",
                    (1, 1),
                    (1, -1),
                    colors.blue,
                ),

                (
                    "TEXTCOLOR",
                    (2, 1),
                    (2, -1),
                    colors.red,
                ),
            ])
        )

        elements.append(
            part_table
        )

        elements.append(
            Spacer(1, 20)
        )

        summary_rows = [

            [
                "Total Qty Required",
                f"{total_required:.2f}",
            ],

            [
                "Total Qty Returned",
                f"{total_returned:.2f}",
            ],
        ]

        summary_table = Table(
            summary_rows,
            colWidths=[180, 120],
        )

        summary_table.setStyle(
            TableStyle([

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black,
                ),

                (
                    "TEXTCOLOR",
                    (1, 0),
                    (1, 0),
                    colors.blue,
                ),

                (
                    "TEXTCOLOR",
                    (1, 1),
                    (1, 1),
                    colors.red,
                ),
            ])
        )

        elements.append(
            summary_table
        )

        elements.append(
            Spacer(1, 35)
        )

        elements.append(
            Paragraph(
                "Authorization",
                styles["Heading2"],
            )
        )

        signature_table = Table(
            [[
                "Requested By",
                "Store Issued By",
                "Approved By",
            ]],

            colWidths=[
                170,
                170,
                170,
            ],
        )

        signature_table.setStyle(
            TableStyle([

                (
                    "LINEABOVE",
                    (0, 0),
                    (-1, 0),
                    1,
                    colors.black,
                ),

                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER",
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (0, 0),
                    colors.blue,
                ),

                (
                    "TEXTCOLOR",
                    (1, 0),
                    (1, 0),
                    colors.red,
                ),

                (
                    "TEXTCOLOR",
                    (2, 0),
                    (2, 0),
                    colors.green,
                ),
            ])
        )

        elements.append(
            signature_table
        )
        add_pdf_footer(elements)
        
        doc.build(
            elements
        )

        buffer.seek(0)

        return buffer