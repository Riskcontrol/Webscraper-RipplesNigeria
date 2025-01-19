from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime

###
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

# Function to send an email with an attachment
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

    # Send the email using SMTP_SSL for port 465
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(sender_email, smtp_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()


###

# Keyword lists
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

# Chrome options
chrome_options = Options()
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6834.83 Safari/537.36"
)
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.binary_location = "/usr/bin/google-chrome"  # Ensure this is the correct path
# Optional: Proxy settings
chrome_options.add_argument("--proxy-server=http://your-proxy-server:port")

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


url = 'https://www.ripplesnigeria.com/'

try:
    driver.get(url)

    # Wait for content to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "h2"))
    )

    # Scroll to load lazy content
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    # Parse page content with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    posts = soup.find_all('h2')

    # Extract data
    data = []
    for post in posts:
        title = post.get_text(strip=True)
        link = post.find_parent('a')['href'] if post.find_parent('a') else None
        if not link:
            continue

        # Visit the article link to extract content
        driver.get(link)
        time.sleep(3)  # Allow content to load

        # Parse article content
        article_soup = BeautifulSoup(driver.page_source, 'html.parser')
        content_div = article_soup.find('div', {'id': 'mvp-content-wrap'})  # Adjust selector as needed
        content = content_div.get_text(strip=True) if content_div else ""

        # Check for keywords
        risk_indicator = next((word for word in risk_keywords if word.lower() in content.lower()), 'NO')
        life_death = next((word for word in life_death_keywords if word.lower() in content.lower()), 'NO')
        state = next((word for word in state_keywords if word.lower() in content.lower()), 'NO')
        case_situation = next((word for word in case_situation_keywords if word.lower() in content.lower()), 'NO')

        # Filter out rows where state is NO
        if state != 'NO':
            # Ensure at least one other column has a match
            if risk_indicator != 'NO' or life_death != 'NO' or case_situation != 'NO':
                data.append({
                    'title': title,
                    'link': link,
                    'Risk Indicator': risk_indicator,
                    'Life/Death': life_death,
                    'State': state,
                    'Case Situation': case_situation
                })

    # Save data to CSV
    if data:
        df = pd.DataFrame(data)

        # Save the filtered data to a CSV file with a timestamp to avoid overwriting
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f'filtered_news_headlines_{timestamp}.csv'
        df.to_csv(filename, index=False)

        ####
        # Email configuration
        sender_email =os.environ.get('USER_EMAIL')
        receiver_email = "nofiumoruf17@gmail.com" #"riskcontrolservicesnig@gmail.com"
        subject = "Ripples Nigeria Daily News Headlines"
        body = "Please find attached the latest news headlines with categorized information."
        smtp_server = "smtp.gmail.com"
        smtp_port = 465  # SSL port for Gmail
        smtp_password = os.environ.get('USER_PASSWORD')  

        # Send the email
        send_email(sender_email, receiver_email, subject, body, filename, smtp_server, smtp_port, smtp_password)

        print("Scraping, categorization, and email sent successfully.")

    else:
        print("No relevant data found to save.")

except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()



