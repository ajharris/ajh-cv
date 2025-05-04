import requests
import re
import logging

# CONFIGURATION
GITHUB_TOKEN = "<github token>"  # <-- Replace with your GitHub token
REPO = "ajharris/ajh-cv"        # <-- Replace with your repo (e.g., 'johndoe/resume')

# Map of LaTeX section names to issue titles
section_templates = {
    "HEADING": "Update Heading Section",
    "Contact": "Update Contact Information",
    "Summary": "Revise Summary Section",
    "Objective": "Revise Objective Section",
    "Education": "Fill in Education Section",
    "Experience": "Add Experience",
    "Projects": "Document Projects",
    "Internships": "Detail Internship Experience",
    "Awards\\and\\Honors": "List Awards and Honors",
    "Skills": "Complete Skills Section"
}

# Load LaTeX template content
with open("template.tex", "r") as file:
    latex_text = file.read()

# GitHub API headers
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Match LaTeX section headers
logging.debug("Starting to match LaTeX section headers.")
pattern = r"%\s*-+\s*(.*?)\s*-+"
matches = re.finditer(pattern, latex_text)

# Generate issues
for match in matches:
    section_raw = match.group(1).strip()
    logging.debug(f"Matched section: {section_raw}")
    title = section_templates.get(section_raw, f"Update section: {section_raw}")
    body = f"""Please review and update the **{section_raw}** section of your resume.

- Replace placeholder content with your actual data.
- Follow formatting as per the LaTeX template.
- Ensure information is accurate and well-structured."""

    logging.debug(f"Creating issue with title: {title}")
    response = requests.post(
        f"https://api.github.com/repos/{REPO}/issues",
        headers=headers,
        json={"title": title, "body": body}
    )

    if response.status_code == 201:
        logging.info(f"Issue created successfully: {title}")
    else:
        logging.error(f"Failed to create issue: {title}")
        logging.error(f"Status code: {response.status_code}, Response: {response.text}")

