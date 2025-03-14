from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import os

if not os.path.exists("flowcharts"):
    os.makedirs("flowcharts")

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"message": "Hello, this is a profession suggestion Application"}
            self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Handles POST requests. Generates suggestions & ASCII flowcharts."""
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        if self.path == "/suggest":
            interest = data.get("interest", "").lower()
            profession = data.get("profession", "").lower()

            profession_paths = {
                "technology": ["Software Engineer", "Data Scientist", "Cybersecurity Analyst"],
                "medicine": ["Doctor", "Nurse", "Medical Researcher"],
                "finance": ["Financial Analyst", "Accountant", "Investment Banker"],
                "law": ["Lawyer"],
                "art": ["Graphic Designer", "Musician", "Filmmaker"]
            }

            profession_roadmaps = {
                "software engineer": [
                    "Learn Programming (Python, Java, etc.)",
                    "Understand Data Structures & Algorithms",
                    "Build Projects & Open-Source Contributions",
                    "Master System Design & Databases",
                    "Apply for Internships & Jobs"
                ],
                "data scientist": [
                    "Learn Python & SQL",
                    "Master Statistics & Probability",
                    "Understand Machine Learning & AI",
                    "Work on Data Science Projects",
                    "Apply for Data Science Roles"
                ],
                "cybersecurity analyst": [
                    "Learn Networking & Security Fundamentals",
                    "Get Certified (CEH, CISSP, etc.)",
                    "Master Ethical Hacking & Penetration Testing",
                    "Gain Hands-on Experience with Security Tools",
                    "Apply for Cybersecurity Jobs"
                ],
                "doctor": [
                    "Complete MBBS Degree",
                    "Internship & Residency Training",
                    "Choose Specialization (MD/MS)",
                    "Gain Clinical Experience",
                    "Work as a Practicing Doctor"
                ],
                "nurse": [
                    "Earn Nursing Degree (B.Sc Nursing, etc.)",
                    "Obtain Necessary Certifications",
                    "Gain Clinical Experience in Hospitals",
                    "Specialize in a Nursing Field",
                    "Work as a Registered Nurse"
                ],
                "medical researcher": [
                    "Earn a Degree in Biology/Medicine",
                    "Obtain Advanced Research Training (PhD, MSc)",
                    "Gain Experience in Laboratory Research",
                    "Publish Scientific Papers",
                    "Work in Research Institutions or Pharmaceuticals"
                ],
                "financial analyst": [
                    "Earn a Finance/Accounting Degree",
                    "Master Financial Modeling & Analysis",
                    "Get Certified (CFA, CPA, etc.)",
                    "Gain Experience in Investment Analysis",
                    "Apply for Financial Analyst Roles"
                ],
                "accountant": [
                    "Earn an Accounting Degree (B.Com, CA, CPA)",
                    "Gain Practical Experience in Accounting Firms",
                    "Understand Taxation & Auditing",
                    "Get Certified (CA, CPA, ACCA, etc.)",
                    "Work as a Corporate Accountant or Auditor"
                ],
                "investment banker": [
                    "Study Finance, Economics, or Business",
                    "Gain Knowledge in M&A & Financial Markets",
                    "Intern at Investment Banks",
                    "Network & Apply for Banking Roles",
                    "Work on IPOs, M&As, and Corporate Finance"
                ],
                "lawyer": [
                    "Earn a Law Degree (LLB)",
                    "Pass Bar Examination",
                    "Gain Legal Internship Experience",
                    "Specialize in a Legal Field",
                    "Practice as an Attorney or Advocate"
                ],
                "graphic designer": [
                    "Learn Design Principles & Color Theory",
                    "Master Graphic Design Tools (Photoshop, Illustrator, etc.)",
                    "Understand Typography & Layout Techniques",
                    "Build a Strong Portfolio with Real Projects",
                    "Network & Apply for Graphic Design Jobs or Freelance Work"
                ],
                "musician": [
                    "Choose Your Instrument or Specialization (Vocals, Guitar, etc.)",
                    "Learn Music Theory & Fundamentals",
                    "Practice Daily & Improve Your Skills",
                    "Record & Produce Music (DAW, Mixing & Mastering)",
                    "Perform Live & Build an Audience",
                    "Network & Collaborate with Other Musicians",
                    "Release Music on Streaming Platforms or Join a Band/Label"
                ],
                "filmmaker": [
                    "Learn the Basics of Filmmaking & Storytelling",
                    "Understand Camera Work, Lighting & Cinematography",
                    "Master Video Editing & Post-Production (Premiere Pro, DaVinci Resolve, etc.)",
                    "Write & Create Your Own Short Films",
                    "Gain Hands-on Experience in Film Production",
                    "Build a Portfolio & Submit to Film Festivals",
                    "Network with Industry Professionals",
                    "Work on Feature Films, Advertisements, or Start Your Own Production House"
                ]
            }

            if profession in profession_roadmaps:
                roadmap = profession_roadmaps[profession]
                flowchart_ascii = self.generate_ascii_flowchart(profession, roadmap)
                response = {
                    "profession": profession,
                    "roadmap": roadmap,
                    "flowchart": flowchart_ascii
                }
            else:
                suggestions = profession_paths.get(interest, ["No suggestions are not available"])
                flowchart_ascii = self.generate_ascii_flowchart(interest, suggestions)
                response = {
                    "interest": interest,
                    "suggestions": suggestions,
                    "flowchart": flowchart_ascii
                }

            self.send_response(200)
        else:
            self.send_response(404)
            response = {"error": "Endpoint not found"}

        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def generate_ascii_flowchart(self, title, steps):
        flowchart = f"{title.capitalize()}\n"
        flowchart += "   |\n   v\n"

        for step in steps:
            flowchart += f"--> {step}\n"

        return flowchart.strip()

#server end , guys if u wnt change it to https
server_address = ("", 8000)
httpd = HTTPServer(server_address, MyHandler)
print("Server running on http://127.0.0.1:8000")
httpd.serve_forever()
