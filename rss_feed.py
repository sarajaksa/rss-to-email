from stable import folder, password, email, server, port
from email.message import EmailMessage
import feedparser
import smtplib
import time
import os


def get_current_time():
    current_time = time.gmtime()
    current_time = time.mktime(current_time)
    return current_time


def get_rss_links(folder, filename):
    with open(os.path.join(folder, filename)) as f:
        links = f.readlines()

    links = [link.strip() for link in links]
    return links


def get_time_threshold(folder, filename):
    try:
        with open(os.path.join(folder, filename)) as f:
            old_time = f.readlines()
            old_time = float(old_time[0].strip())
    except FileNotFoundError or ValueError or IndexError:
        old_time = 1
    return old_time


def get_all_rss_feeds(links, old_time):
    all_current_feeds = []
    for link in links:
        if not link:
            continue
        rss_feed = feedparser.parse(link)
        while "status" not in rss_feed:
            time.sleep(60 * 10)
        if rss_feed.status == 403:
            continue
        rss_feed = feedparser.parse(link)
        rss_entries = rss_feed["entries"]
        for entry in rss_entries:
            entry_time = entry["published_parsed"]
            entry_time = time.mktime(entry_time)
            if entry_time < old_time:
                continue
            try:
                title = entry["title"]
            except KeyError:
                title = ""
            try:
                link = entry["link"]
            except KeyError:
                continue
            all_current_feeds.append(tuple([title, link]))
    return all_current_feeds


def create_rss_email_text(all_current_feeds):
    new_email_text = "Nove RSS Objave\n\n\n"
    for title, link in all_current_feeds:
        new_email_text += title + "\n" + link + "\n\n"
    return new_email_text


def create_rss_email_message(new_email_text, email):
    message = EmailMessage()
    message.set_content(new_email_text)
    message["Subject"] = "RSS"
    message["From"] = email
    message["To"] = email
    return message


def send_rss_email(server, port, email, password, message):
    server = smtplib.SMTP_SSL(server, port)
    server.login(email, password)
    server.sendmail(email, email, message.as_string())
    server.close()


def save_new_time_threshold(folder, filename, current_time):
    with open(os.path.join(folder, filename), "w") as f:
        f.write(str(current_time))


def rss_to_email(email, passsword, server, port, folder):
    current_time = get_current_time()
    links = get_rss_links(folder, "rss-links.txt")
    old_time = get_time_threshold(folder, "time.txt")
    all_current_feeds = get_all_rss_feeds(links, old_time)
    new_email_text = create_rss_email_text(all_current_feeds)
    message = create_rss_email_message(new_email_text, email)
    send_rss_email(server, port, email, password, message)
    save_new_time_threshold(folder, "time.txt", current_time)


if __name__ == "__main__":
    rss_to_email(email, password, server, port, folder)
