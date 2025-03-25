

# import os
# import re
# import random
# import time
# from datetime import datetime
# import pandas as pd
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.application import MIMEApplication

# # -------------------------------
# # Initialize Groq API Client (for summarization)
# # -------------------------------
# from groq import AsyncGroq
# import asyncio

# client = AsyncGroq(api_key="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")

# async def summarize_content(content):
#     """
#     Uses Groq API to summarize the content in no more than 35 words.
#     """
#     try:
#         response = await client.chat.completions.create(
#             messages=[
#                 {"role": "system", "content": "Summarize the following news in no more than 35 words while keeping key details."},
#                 {"role": "user", "content": content}
#             ],
#             model="llama3-8b-8192"
#         )
#         summary = response.choices[0].message.content.strip()
#         words = summary.split()
#         if len(words) > 35:
#             summary = " ".join(words[:35]) + "..."
#         return summary
#     except Exception as e:
#         return f"Error generating summary: {e}"

# # -------------------------------
# # Define User Agents for Ripples Nigeria
# # -------------------------------
# USER_AGENTS = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
# ]

# # -------------------------------
# # Email Sending Function
# # -------------------------------
# def send_email(sender_email, receiver_email, subject, body, attachment_path, smtp_server, smtp_port, smtp_password):
#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = receiver_email
#     msg['Subject'] = subject

#     msg.attach(MIMEText(body, 'plain'))

#     with open(attachment_path, 'rb') as attachment:
#         part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
#     part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
#     msg.attach(part)

#     server = smtplib.SMTP_SSL(smtp_server, smtp_port)
#     server.login(sender_email, smtp_password)
#     server.sendmail(sender_email, receiver_email, msg.as_string())
#     server.quit()

# # -------------------------------
# # Keyword Lists for Filtering
# # -------------------------------
# risk_keywords = [
#     'Rape', 'rape', 'Kidnapping', 'kidnapping', 'Terrorism', 'terrorism',
#     'Assaults', 'Homicide', 'homicide', 'Cultism', 'cultism',
#     'Piracy', 'piracy', 'Drowning', 'Armed Robbery', 'Fire Outbreak',
#     'Unsafe Route/Violent Attacks', 'Human Trafficking', 'human trafficking',
#     'Crime', 'arrested', 'nabbed', 'paraded', 'detained', 'apprehended', 'arresting',
#     'remanded', 'rescued', 'crime', 'Arrest', 'arrest', 'ambush', 'Ambush',
#     'Bandit', 'bandit', 'accident', 'Accident', 'fraud', 'Fraud', 'corruption',
#     'Corruption', 'Organ Trafficking'
# ]
# life_death_keywords = ['Killed', 'casualties', 'casualty', 'dies', 'death', 'kill']
# state_keywords = [
#     'Abuja', 'Abia', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa',
#     'Benue', 'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu',
#     'Gombe', 'Imo', 'Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Kogi',
#     'Kwara', 'Lagos', 'Nassarawa', 'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo',
#     'Plateau', 'Rivers', 'Sokoto', 'FCT', 'Taraba', 'Yobe', 'Zamfara'
# ]
# case_situation_keywords = ['victims', 'victim', 'injured']

# # -------------------------------
# # Chrome Options with Extra Headers and Rotating User Agent
# # -------------------------------
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.binary_location = "/usr/bin/google-chrome"  # Adjust if needed

# # Rotate user agent
# user_agent = random.choice(USER_AGENTS)
# chrome_options.add_argument(f"user-agent={user_agent}")
# # Add extra headers via experimental options
# chrome_options.add_experimental_option("prefs", {
#     "profile.default_content_setting_values.notifications": 2,
# })
# chrome_options.add_argument("--lang=en-US")

# # -------------------------------
# # Initialize WebDriver
# # -------------------------------
# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service, options=chrome_options)

# # -------------------------------
# # Target URL for Ripples Nigeria
# # -------------------------------
# url = 'https://www.ripplesnigeria.com/feed/'

# try:
#     driver.get(url)
#     # Wait for at least one <h2> element to appear
#     WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "h2")))

#     # Scroll down to load lazy-loaded content
#     for _ in range(5):
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(3)

#     # Save full HTML for debugging (optional)
#     with open("debug_homepage.html", "w", encoding="utf-8") as f:
#         f.write(driver.page_source)

#     # Parse homepage content
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     posts = soup.find_all('h2')

#     data = []
#     for post in posts:
#         title = post.get_text(strip=True)
#         link_tag = post.find_parent('a')
#         link = link_tag['href'] if link_tag else None
#         if not link:
#             continue

#         # Visit the article link to extract content
#         driver.get(link)
#         time.sleep(3)  # Allow article to load

#         article_soup = BeautifulSoup(driver.page_source, 'html.parser')
#         content_div = article_soup.find('div', {'id': 'mvp-content-wrap'})  # Adjust if needed
#         content = content_div.get_text(strip=True) if content_div else ""

#         # Use Groq API to generate summary
#         summary = asyncio.run(summarize_content(content)) if content else ""

#         risk_indicator = next((word for word in risk_keywords if word.lower() in content.lower()), 'NO')
#         life_death = next((word for word in life_death_keywords if word.lower() in content.lower()), 'NO')
#         state = next((word for word in state_keywords if word.lower() in content.lower()), 'NO')
#         case_situation = next((word for word in case_situation_keywords if word.lower() in content.lower()), 'NO')

#         if state != 'NO' and (risk_indicator != 'NO' or life_death != 'NO' or case_situation != 'NO'):
#             data.append({
#                 'title': title,
#                 'link': link,
#                 'Risk Indicator': risk_indicator,
#                 'Life/Death': life_death,
#                 'State': state,
#                 'Case Situation': case_situation,
#                 'Summary': summary
#             })

#     if data:
#         df = pd.DataFrame(data)
#         timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#         filename = f'filtered_news_headlines_{timestamp}.csv'
#         df.to_csv(filename, index=False)

#         # Email configuration (update credentials as needed)
#         sender_email = 'rcsnbc@gmail.com'
#         receiver_email = 'nofiumoruf17@gmail.com'
#         subject = "Ripples Nigeria Daily News Headlines"
#         body = "Please find attached the latest news headlines with categorized information and summaries."
#         smtp_server = "smtp.gmail.com"
#         smtp_port = 465  # SSL port for Gmail
#         smtp_password = 'wkhf nxrn uigo uxom'  # Your app-specific password

#         send_email(sender_email, receiver_email, subject, body, filename, smtp_server, smtp_port, smtp_password)
#         print("Scraping, categorization, summarization, and email sent successfully.")
#     else:
#         print("No relevant data found to save.")

# except Exception as e:
#     print(f"Error: {e}")
# finally:
#     driver.quit()

import os
import re
import time
import asyncio
from datetime import datetime
import pandas as pd
import feedparser
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import nest_asyncio

nest_asyncio.apply()

# -------------------------------
# Initialize Groq API Client
# -------------------------------
from groq import AsyncGroq

client = AsyncGroq(api_key="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")

async def summarize_content(content):
    try:
        response = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Summarize the following news in no more than 35 words while keeping key details."},
                {"role": "user", "content": content}
            ],
            model="llama3-8b-8192"
        )
        summary = response.choices[0].message.content.strip()
        words = summary.split()
        if len(words) > 35:
            summary = " ".join(words[:35]) + "..."
        return summary
    except Exception as e:
        return f"Error generating summary: {e}"

# -------------------------------
# Email Sending Function
# -------------------------------
def send_email(sender_email, receiver_email, subject, body, attachment_path, smtp_server, smtp_port, smtp_password):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with open(attachment_path, 'rb') as attachment:
        part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
    msg.attach(part)

    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(sender_email, smtp_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

# -------------------------------
# Keyword Lists
# -------------------------------
risk_keywords = [
    'rape', 'kidnapping', 'terrorism', 'assault', 'homicide', 'cultism', 'piracy', 'drowning', 'robbery',
    'fire', 'trafficking', 'crime', 'arrest', 'ambush', 'bandit', 'accident', 'fraud', 'corruption', 'organ'
]
life_death_keywords = ['killed', 'casualties', 'casualty', 'dies', 'death', 'kill']
state_keywords = [
    'Abuja', 'Abia', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa',
    'Benue', 'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu',
    'Gombe', 'Imo', 'Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Kogi',
    'Kwara', 'Lagos', 'Nassarawa', 'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo',
    'Plateau', 'Rivers', 'Sokoto', 'FCT', 'Taraba', 'Yobe', 'Zamfara'
]
case_situation_keywords = ['victims', 'victim', 'injured']

# -------------------------------
# Main RSS Scraper Logic
# -------------------------------
rss_url = "https://www.ripplesnigeria.com/feed/"
feed = feedparser.parse(rss_url)
data = []

for entry in feed.entries:
    title = entry.title
    link = entry.link
    description_html = entry.get("description", "")
    description_text = BeautifulSoup(description_html, "html.parser").get_text()

    # Summarize
    summary = asyncio.run(summarize_content(description_text)) if description_text else ""

    # Keyword Filtering
    content_lower = description_text.lower()
    risk_indicator = next((word for word in risk_keywords if word in content_lower), 'NO')
    life_death = next((word for word in life_death_keywords if word in content_lower), 'NO')
    state = next((word for word in state_keywords if word.lower() in content_lower), 'NO')
    case_situation = next((word for word in case_situation_keywords if word in content_lower), 'NO')

    if state != 'NO' and (risk_indicator != 'NO' or life_death != 'NO' or case_situation != 'NO'):
        data.append({
            'title': title,
            'link': link,
            'Risk Indicator': risk_indicator,
            'Life/Death': life_death,
            'State': state,
            'Case Situation': case_situation,
            'Summary': summary
        })

# -------------------------------
# Save + Email
# -------------------------------
if data:
    df = pd.DataFrame(data)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f'filtered_news_rss_{timestamp}.csv'
    df.to_csv(filename, index=False)

    send_email(
        sender_email=os.environ.get('USER_EMAIL'),
        receiver_email='riskcontrolservicesnig@gmail.com',
        subject="Ripples Nigeria Daily News",
        body="Attached is today's news summary with risk indicators.",
        attachment_path=filename,
        smtp_server="smtp.gmail.com",
        smtp_port=465,
        smtp_password=os.environ.get('USER_PASSWORD')
    )
    print("RSS parsing, summarization, and email sent successfully.")
else:
    print("No relevant articles matched the filter.")






