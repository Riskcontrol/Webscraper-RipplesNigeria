# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# import pandas as pd
# import time
# from datetime import datetime

# ###
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
# from email import encoders
# from email.mime.text import MIMEText
# from email.mime.application import MIMEApplication
# import os

# # Function to send an email with an attachment
# def send_email(sender_email, receiver_email, subject, body, attachment_path, smtp_server, smtp_port, smtp_password):
#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = receiver_email
#     msg['Subject'] = subject

#     # Attach the body text
#     msg.attach(MIMEText(body, 'plain'))

#     # Attach the file
#     with open(attachment_path, 'rb') as attachment:
#         part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
#     part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
#     msg.attach(part)

#     # Send the email using SMTP_SSL for port 465
#     server = smtplib.SMTP_SSL(smtp_server, smtp_port)
#     server.login(sender_email, smtp_password)
#     server.sendmail(sender_email, receiver_email, msg.as_string())
#     server.quit()


# ###

# # Keyword lists
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

# # Chrome options
# chrome_options = Options()
# chrome_options.add_argument(
#     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6834.83 Safari/537.36"
# )
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.binary_location = "/usr/bin/google-chrome"  # Ensure this is the correct path
# # Optional: Proxy settings
# chrome_options.add_argument("--proxy-server=http://your-proxy-server:port")

# # Initialize WebDriver
# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service, options=chrome_options)


# url = 'https://www.ripplesnigeria.com/'

# try:
#     driver.get(url)

#     # Wait for content to load
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_all_elements_located((By.TAG_NAME, "h2"))
#     )

#     # Scroll to load lazy content
#     for _ in range(5):
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(3)

#     # Parse page content with BeautifulSoup
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     posts = soup.find_all('h2')

#     # Extract data
#     data = []
#     for post in posts:
#         title = post.get_text(strip=True)
#         link = post.find_parent('a')['href'] if post.find_parent('a') else None
#         if not link:
#             continue

#         # Visit the article link to extract content
#         driver.get(link)
#         time.sleep(3)  # Allow content to load

#         # Parse article content
#         article_soup = BeautifulSoup(driver.page_source, 'html.parser')
#         content_div = article_soup.find('div', {'id': 'mvp-content-wrap'})  # Adjust selector as needed
#         content = content_div.get_text(strip=True) if content_div else ""

#         # Check for keywords
#         risk_indicator = next((word for word in risk_keywords if word.lower() in content.lower()), 'NO')
#         life_death = next((word for word in life_death_keywords if word.lower() in content.lower()), 'NO')
#         state = next((word for word in state_keywords if word.lower() in content.lower()), 'NO')
#         case_situation = next((word for word in case_situation_keywords if word.lower() in content.lower()), 'NO')

#         # Filter out rows where state is NO
#         if state != 'NO':
#             # Ensure at least one other column has a match
#             if risk_indicator != 'NO' or life_death != 'NO' or case_situation != 'NO':
#                 data.append({
#                     'title': title,
#                     'link': link,
#                     'Risk Indicator': risk_indicator,
#                     'Life/Death': life_death,
#                     'State': state,
#                     'Case Situation': case_situation
#                 })

#     # Save data to CSV
#     if data:
#         df = pd.DataFrame(data)

#         # Save the filtered data to a CSV file with a timestamp to avoid overwriting
#         timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#         filename = f'filtered_news_headlines_{timestamp}.csv'
#         df.to_csv(filename, index=False)

#         ####
#         # Email configuration
#         sender_email =os.environ.get('USER_EMAIL')
#         receiver_email = "nofiumoruf17@gmail.com" #"riskcontrolservicesnig@gmail.com"
#         subject = "Ripples Nigeria Daily News Headlines"
#         body = "Please find attached the latest news headlines with categorized information."
#         smtp_server = "smtp.gmail.com"
#         smtp_port = 465  # SSL port for Gmail
#         smtp_password = os.environ.get('USER_PASSWORD')  

#         # Send the email
#         send_email(sender_email, receiver_email, subject, body, filename, smtp_server, smtp_port, smtp_password)

#         print("Scraping, categorization, and email sent successfully.")

#     else:
#         print("No relevant data found to save.")

# except Exception as e:
#     print(f"Error: {e}")
# finally:
#     driver.quit()

# from playwright.sync_api import sync_playwright
# import pandas as pd
# from datetime import datetime
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.application import MIMEApplication
# import os

# # Function to send email with attachment
# def send_email(sender_email, receiver_email, subject, body, attachment_path, smtp_server, smtp_port, smtp_password):
#     try:
#         msg = MIMEMultipart()
#         msg['From'] = sender_email
#         msg['To'] = receiver_email
#         msg['Subject'] = subject

#         # Attach the body text
#         msg.attach(MIMEText(body, 'plain'))

#         # Attach the file
#         with open(attachment_path, 'rb') as attachment:
#             part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
#             part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
#             msg.attach(part)

#         # Send the email
#         with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
#             server.login(sender_email, smtp_password)
#             server.send_message(msg)
#         print("Email sent successfully.")
#     except Exception as e:
#         print(f"Failed to send email: {e}")

# # Keyword lists
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

# # Scraper logic
# def scrape_ripples():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         context = browser.new_context()
#         page = context.new_page()

#         # Visit the website
#         page.goto("https://www.ripplesnigeria.com/")
#         # Wait for network to be idle
#         page.wait_for_load_state("networkidle")
#         # Save a screenshot to see the page state
#         page.screenshot(path="debug_screenshot.png", full_page=True)

#         # Save the page content to check if it loaded
#         with open("debug_page_content.html", "w", encoding="utf-8") as f:
#             f.write(page.content())

#         # page.wait_for_selector("h2")
#         # Increase timeout
#         if page.locator("h2").count() == 0:
#             print("No <h2> tags found on the page.")
#         else:
#             print(f"Found {page.locator('h2').count()} <h2> tags.")

#         page.wait_for_selector("h2", timeout=60000)  # 60 seconds timeout

#         # Scroll down to load all content
#         for _ in range(10):
#             page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
#             page.wait_for_timeout(3000)

#         # Extract articles
#         articles = page.locator("h2").all()
#         data = []
#         for article in articles:
#             title = article.inner_text()
#             link = article.locator("xpath=..").get_attribute("href")
#             if not link:
#                 continue

#             # Visit article page
#             page.goto(link)
#             page.wait_for_selector("#mvp-content-wrap", timeout=5000)
#             content = page.locator("#mvp-content-wrap").inner_text()

#             # Check for keywords
#             risk_indicator = next((word for word in risk_keywords if word.lower() in content.lower()), 'NO')
#             life_death = next((word for word in life_death_keywords if word.lower() in content.lower()), 'NO')
#             state = next((word for word in state_keywords if word.lower() in content.lower()), 'NO')
#             case_situation = next((word for word in case_situation_keywords if word.lower() in content.lower()), 'NO')

#             if state != 'NO' and (risk_indicator != 'NO' or life_death != 'NO' or case_situation != 'NO'):
#                 data.append({
#                     'title': title,
#                     'link': link,
#                     'Risk Indicator': risk_indicator,
#                     'Life/Death': life_death,
#                     'State': state,
#                     'Case Situation': case_situation
#                 })

#         browser.close()

#         # Save data to CSV
#         if data:
#             df = pd.DataFrame(data)
#             timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#             filename = f'filtered_news_headlines_{timestamp}.csv'
#             df.to_csv(filename, index=False)

#             # Email configuration
#             sender_email = os.environ.get('USER_EMAIL')
#             receiver_email = "nofiumoruf17@gmail.com"
#             subject = "Ripples Nigeria Daily News Headlines"
#             body = "Please find attached the latest news headlines with categorized information."
#             smtp_server = "smtp.gmail.com"
#             smtp_port = 465
#             smtp_password = os.environ.get('USER_PASSWORD')

#             # Send the email
#             send_email(sender_email, receiver_email, subject, body, filename, smtp_server, smtp_port, smtp_password)
#         else:
#             print("No relevant data found.")

# # Run the scraper
# if __name__ == "__main__":
#     scrape_ripples()





import os
import re
import random
import time
import asyncio
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# -------------------------------
# Initialize Groq API Client
# -------------------------------
# Make sure the async_groq package is installed.
from groq import AsyncGroq

client = AsyncGroq(api_key="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")

async def summarize_content(content):
    """
    Uses Groq API to summarize the content in no more than 35 words.
    """
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
# Define User Agents for Ripples Nigeria
# -------------------------------
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
]

# -------------------------------
# Email Sending Function
# -------------------------------
def send_email(sender_email, receiver_email, subject, body, attachment_path, smtp_server, smtp_port, smtp_password):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the body text
    msg.attach(MIMEText(body, 'plain'))

    # Attach the file
    with open(attachment_path, 'rb') as attachment:
        part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
    msg.attach(part)

    # Send the email using SMTP_SSL (port 465 for Gmail)
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(sender_email, smtp_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

# -------------------------------
# Keyword Lists for Filtering
# -------------------------------
risk_keywords = [
    'Rape', 'rape', 'Kidnapping', 'kidnapping', 'Terrorism', 'terrorism',
    'Assaults', 'Homicide', 'homicide', 'Cultism', 'cultism',
    'Piracy', 'piracy', 'Drowning', 'Armed Robbery', 'Fire Outbreak',
    'Unsafe Route/Violent Attacks', 'Human Trafficking', 'human trafficking',
    'Crime', 'arrested', 'nabbed', 'paraded', 'detained', 'apprehended', 'arresting',
    'remanded', 'rescued', 'crime', 'Arrest', 'arrest', 'ambush', 'Ambush',
    'Bandit', 'bandit', 'accident', 'Accident', 'fraud', 'Fraud', 'corruption',
    'Corruption', 'Organ Trafficking'
]
life_death_keywords = ['Killed', 'casualties', 'casualty', 'dies', 'death', 'kill']
state_keywords = [
    'Abuja', 'Abia', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa',
    'Benue', 'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu',
    'Gombe', 'Imo', 'Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Kogi',
    'Kwara', 'Lagos', 'Nassarawa', 'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo',
    'Plateau', 'Rivers', 'Sokoto', 'FCT', 'Taraba', 'Yobe', 'Zamfara'
]
case_situation_keywords = ['victims', 'victim', 'injured']

# -------------------------------
# Chrome Options with Rotating User Agent
# -------------------------------
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = "/usr/bin/google-chrome"  # Adjust path if needed

# Rotate user agent
user_agent = random.choice(USER_AGENTS)
chrome_options.add_argument(f"user-agent={user_agent}")

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# -------------------------------
# Target URL for Ripples Nigeria
# -------------------------------
url = 'https://www.ripplesnigeria.com/'

try:
    driver.get(url)
    # Wait for at least one <h2> element to ensure the page loads
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "h2")))

    # Scroll down to load lazy-loaded content
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    # Parse the homepage content with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    posts = soup.find_all('h2')

    # Extract data from each post
    data = []
    for post in posts:
        title = post.get_text(strip=True)
        link_tag = post.find_parent('a')
        link = link_tag['href'] if link_tag else None
        if not link:
            continue

        # Visit the article link to extract its content
        driver.get(link)
        time.sleep(3)  # Allow the article to load

        article_soup = BeautifulSoup(driver.page_source, 'html.parser')
        content_div = article_soup.find('div', {'id': 'mvp-content-wrap'})  # Adjust selector if necessary
        content = content_div.get_text(strip=True) if content_div else ""

        # Use Groq API to summarize the article content
        # (Run the async summarization using asyncio.run)
        summary = asyncio.run(summarize_content(content)) if content else ""

        # Check for keywords in the article content
        risk_indicator = next((word for word in risk_keywords if word.lower() in content.lower()), 'NO')
        life_death = next((word for word in life_death_keywords if word.lower() in content.lower()), 'NO')
        state = next((word for word in state_keywords if word.lower() in content.lower()), 'NO')
        case_situation = next((word for word in case_situation_keywords if word.lower() in content.lower()), 'NO')

        # Filter to include articles with a valid state and at least one other match
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

    # Save data to CSV if any articles were collected
    if data:
        df = pd.DataFrame(data)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f'filtered_news_headlines_{timestamp}.csv'
        df.to_csv(filename, index=False)

        # Email configuration (update these with your actual credentials)
        sender_email = os.environ.get('USER_EMAIL')
        receiver_email = 'nofiumoruf17@gmail.com'
        subject = "Ripples Nigeria Daily News Headlines"
        body = "Please find attached the latest news headlines with categorized information and summaries."
        smtp_server = "smtp.gmail.com"
        smtp_port = 465  # SSL port for Gmail
        smtp_password = os.environ.get('USER_PASSWORD')  # Your app-specific password

        # Send the email with the CSV attachment
        send_email(sender_email, receiver_email, subject, body, filename, smtp_server, smtp_port, smtp_password)
        print("Scraping, categorization, summarization, and email sent successfully.")
    else:
        print("No relevant data found to save.")

except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()

