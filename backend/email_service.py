import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailService:
    def __init__(self):
        # In a real scenario, these would come from environment variables
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv("SENDER_EMAIL", "noreply@talentscout.ai")
        self.sender_password = os.getenv("SENDER_PASSWORD", "mock_password")
        self.mock_mode = True # Set to False if you configure real credentials

    def send_shortlist_email(self, recipient_email, candidate_data, match_score, matching_skills):
        subject = f"Candidate Shortlisted: Match Score {match_score}%"
        
        body = f"""
        <html>
        <body>
            <h2>Candidate Shortlisted</h2>
            <p>A candidate has matched your job requirements.</p>
            
            <h3>Match Details</h3>
            <ul>
                <li><strong>Match Score:</strong> {match_score}%</li>
                <li><strong>Matching Skills:</strong> {', '.join(matching_skills)}</li>
            </ul>
            
            <h3>Candidate Details</h3>
            <ul>
                <li><strong>Name:</strong> {candidate_data.get('Name', 'N/A')}</li>
                <li><strong>Email:</strong> {candidate_data.get('Email', 'N/A')}</li>
                <li><strong>Phone:</strong> {candidate_data.get('Phone', 'N/A')}</li>
            </ul>
            
            <p><em>This is an automated message from TalentScout AI.</em></p>
        </body>
        </html>
        """

        if self.mock_mode or not recipient_email:
            print(f"n[MOCK EMAIL SERVICE]nTo: {recipient_email}nSubject: {subject}nBody Summary: Candidate matched with {match_score}% score.n")
            return True

        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
