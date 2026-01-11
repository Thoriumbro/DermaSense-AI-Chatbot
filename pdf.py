def final_report(personal_details_dict,symptomsData):
    from fpdf import FPDF

    class PDF(FPDF):
        def header(self):
            self.image("logo.png",1,5,20)

    pdf = PDF("P", "cm", "A4")

    pdf.set_auto_page_break(5)

    pdf.add_page()

    pdf.set_font("Arial", style='B', size=24)
    pdf.cell(0, 3, 'PATIENT SCREENING REPORT', ln=True, align='C')

    pdf.set_font("Arial", style='B', size=20)
    pdf.cell(0, 3, 'Patient Details', ln=True, align='L')

    pdf.line(1,6,20,6)

    for detail, val in personal_details_dict.items():
        pdf.set_font("Arial", style='B', size=18)
        pdf.cell(10,1,detail,border=True,align='L')
        pdf.set_font("Arial", style='', size=18)
        pdf.cell(9,1,val,border=True,align='L',ln=True)

    pdf.ln(2)
    pdf.set_font("Arial", style='B', size=20)
    pdf.cell(0, 3, 'Symptom Summary', ln=True, align='L')
    pdf.line(1,15,20,15)

    count = 1
    for i in symptomsData:
        pdf.set_font("Arial", style='BU', size=18)
        pdf.cell(0,1,f"{count}.{i[1].title()}",ln=True)
        pdf.set_font("Arial", style='', size=18)
        pdf.cell(0,1,f'  Category: {i[0][0]}',ln=True)
        pdf.cell(0,1,f'  Duration: {list(i[2].values())[0]}',ln=True)
        pdf.cell(0,1,f'  Severity: {list(i[2].values())[1]}',ln=True)
        pdf.cell(0,1,f'  Issues: {list(i[2].values())[2]}',ln=True)
        pdf.ln(1)
        count += 1
        
    pdf.output("report.pdf")
    print(f"Patient report successfully saved as report.pdf .")
