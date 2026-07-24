from io import BytesIO
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
from app.utils.pdf_footer import add_pdf_footer

class PDFService:

    @staticmethod
    def generate_job_card_pdf(
        job_card,
        vehicle,
        driver,
        technician1,
        technician2,
        requested_by,
        verified_by,
        approved_by,
        parts,
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

        title = Paragraph(
            "VEHICLE JOB CARD",
            styles["Title"],
        )

        elements.append(title)

        elements.append(
            Spacer(1, 2)
        )

        header_data = [
        
            [
                "Job Card No",
                str(job_card.job_card_id),
            ],

            [
                "Vehicle",
                vehicle.vehicle_id
                if vehicle
                else "-",
            ],

            [
                "Driver",
                driver.driver_name
                if driver
                else "-",
            ],

            [
                "Technician 1",
                technician1.full_name
                if technician1
                else "-",
            ],

            [
                "Technician 2",
                technician2.full_name
                if technician2
                else "-",
            ],

            [
                "Status",
                job_card.job_status
                or "-",
            ],

            [
                "Maintenance Type",
                job_card.maintenance_type
                or "-",
            ],

            [
                "Zone",
                job_card.zone_area
                or "-",
            ],

            [
                "Mileage",
                job_card.mileage_hours
                or "-",
            ],
            [
                "Date Time In",
                str(
                    job_card.date_time_in
                    or "-"
                ),
            ],

            [
                "Date Time Out",
                str(
                    job_card.date_time_out
                    or "-"
                ),
            ],
        ]

        header_table = Table(
            header_data,
            colWidths=[
                140,
                320,
            ],
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
            Spacer(1, 4)
        )

        elements.append(
            Paragraph(
                "<b>Issue Reported</b>",
                styles["Heading2"],
            )
        )

        elements.append(
            Paragraph(
                job_card.issue_reported
                or "-",
                styles["Normal"],
            )
        )

        elements.append(
            Spacer(1, 4)
        )

        elements.append(
            Paragraph(
                "<b>Problems Found & Action Taken</b>",
                styles["Heading2"],
            )
        )

        elements.append(
            Paragraph(
                job_card.problem_found_action_taken
                or "-",
                styles["Normal"],
            )
        )

        elements.append(
            Spacer(1, 4)
        )
        
        elements.append(
            Paragraph(
                "Parts Used",
                styles["Heading2"],
            )
        )
        elements.append(
            Spacer(1, 2)
        )
        grand_total=0
        part_rows = [    
            [
                "Part Name",
                "Quantity",
                "Unit Price",
                "Total"
            ]
        ]
        for part in parts:
            part_name = part_lookup.get(
                part.part_id,
                "-"
            )
            qty = part.quantity or 0
            price = ( part.unit_price or 0 )
            total = qty * price
            grand_total += total
            part_rows.append(
                [
                    part_name,
                    str(qty),
                    str(round(float(price), 2)),
                    str(round(float(total), 2)),
                ]
            )
            part_table = Table(
            part_rows,
            colWidths=[150, 100],
            
        )
        part_rows.append(
            [
                "",
                "",
                "Grand Total",
                f"{grand_total:.2f}",
            ]
        )
        part_table = Table(
        part_rows,
        colWidths=[150, 100],)

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
            ])
        )
        elements.append(
            part_table
        )




        approval_data = [

        [
            "Requested By",

            requested_by.full_name
            if requested_by
            else "-",
        ],

        [
            "Verified By",

            verified_by.full_name
            if verified_by
            else "-",
        ],

        [
            "Approved By",

            approved_by.full_name
            if approved_by
            else "-",
        ],
    ]
        approval_table = Table(
            approval_data,
            colWidths=[
                140,
                320,
            ],
        )

        approval_table.setStyle(

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
            Paragraph(
                "<b>Approval Information</b>",
                styles["Heading2"],
            )
        )

        elements.append(
            approval_table
        )
        elements.append(
            Spacer(1, 40)
        )

        signature_table = Table(
            [[
                "Requested By",
                "Verified By",
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