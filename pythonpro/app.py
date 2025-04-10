import os
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv


class PriceChecker:
    def __init__(self, urls, headers, sender_email, sender_password, recipient_email):
        self.urls = urls
        self.headers = headers
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_email = recipient_email

    def get_price(self, url):
        try:
            page = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(page.content, "html.parser")

            if "notino" in url:
                price_element = soup.find(id="pd-price")
                if price_element:
                    price_text = price_element.get_text().strip()
                    price_value = float("".join(filter(str.isdigit, price_text)))
                    return price_value
                else:
                    print(f"Price not found for URL: {url}")
                    return None

            elif "euro.com.pl" in url:
                price_element = soup.find("span", class_="price-template__default--amount")
                if price_element:
                    price_text = price_element.get_text().strip()
                    price_value = float("".join(filter(str.isdigit, price_text)))
                    return price_value
                else:
                    print(f"Price not found for URL: {url}")
                    return None
            else:
                print(f"Unsupported URL format: {url}")
                return None
        except Exception as e:
            print(f"An error occurred while fetching the price from {url}: {e}")
            return None

    def check_prices(self):
        items_to_notify = []

        for url, price_threshold in self.urls:
            price = self.get_price(url)
            if price is not None and price < price_threshold:
                items_to_notify.append(f"Item: {url}\nPrice: {price}")
                print(f"Price for {url} is below threshold: {price} < {price_threshold}")

        if items_to_notify:
            self.send_email(items_to_notify)

    def send_email(self, items):
        subject = "Price Alert"
        message = "\n\n".join(items)

        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, self.recipient_email, msg.as_string())
            print("Email notification sent successfully!")
        except Exception as e:
            print(f"An error occurred while sending the email: {e}")
        finally:
            server.quit()


# Load environment variables from .env file
load_dotenv()

# Usage
if __name__ == "__main__":
    URLs = [
        ("https://www.notino.pl/azzaro/chrome-woda-toaletowa-dla-mczyzn/p-59969/", 300),
        ("https://www.notino.pl/guerlain/aqua-allegoria-pera-granita-woda-toaletowa-dla-kobiet/", 400),
        (
        "https://www.euro.com.pl/odkurzacze-automatyczne/roborock-s8-czarny-mopowanie.bhtml?cd=191780169&ad=10070947089&kd=&gclid=EAIaIQobChMI3o7gg7XAgQMV2OyyCh0vZQ5aEAQYBCABEgLcOvD_BwE&gclsrc=aw.ds",
        2500),
        (
        "https://www.euro.com.pl/odkurzacze-automatyczne/roborock-q7-max-bialy.bhtml?&cd=191780169&ad=10070947089&kd=&gclid=Cj0KCQjwvL-oBhCxARIsAHkOiu0R-ybG2gKqgA2JwP9MWxqIoeNi60vhT709nlSer7e6CMqssst_084aAmyKEALw_wcB&gclsrc=aw.ds",
        2000)
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.53"}

    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    recipient_email = os.getenv("RECIPIENT_EMAIL")

    price_checker = PriceChecker(URLs, headers, sender_email, sender_password, recipient_email)
    price_checker.check_prices()
