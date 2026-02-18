from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas


def create_resume(filename, name, email, phone, skills, role):
    c = canvas.Canvas(filename, pagesize=LETTER)

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, name)
    c.setFont("Helvetica", 12)
    c.drawString(50, 735, role)

    # Contact Info (The parser needs these formats)
    c.setFont("Helvetica", 10)
    c.drawString(50, 715, f"Email: {email}")
    c.drawString(50, 700, f"Phone: {phone}")

    # Skills Section
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 670, "Technical Skills")
    c.setFont("Helvetica", 10)
    y_position = 650
    for skill in skills:
        c.drawString(70, y_position, f"- {skill}")
        y_position -= 15

    # Experience (Filler text)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position - 20, "Experience")
    c.setFont("Helvetica", 10)
    c.drawString(50, y_position - 40, "Worked on various projects using Python and SQL.")
    c.drawString(50, y_position - 55, "Developed machine learning models for business analytics.")

    c.save()
    print(f"✅ Created: {filename}")


if __name__ == "__main__":
    create_resume(
        "Resume_John.pdf",
        "John Doe",
        "john.doe@gmail.com",
        "+91 98765 43210",
        ["Python", "Machine Learning", "SQL", "Tableau", "Pandas"],
        "Data Scientist"
    )

    create_resume(
        "Resume_Sarah.pdf",
        "Sarah Jenkins",
        "sarah.j@techmail.com",
        "555-019-2834",
        ["HTML", "CSS", "React", "JavaScript", "Node.js"],
        "Frontend Developer"
    )

    create_resume(
        "Resume_Mike.pdf",
        "Mike Ross",
        "mikeross@business.net",
        "+1 (408) 555-9988",
        ["Project Management", "Communication", "Leadership", "Agile", "Scrum"],
        "Project Manager"
    )