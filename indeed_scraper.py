import csv
from datetime import datetime
from bs4 import BeautifulSoup
from zenrows import ZenRowsClient
from tabulate import tabulate
import textwrap

def get_url(position, location):
    template = "https://de.indeed.com/jobs?q={}&l={}"
    url = template.format(position, location)
    return url

def get_record(card):
    atag = card.find("a", "jcs-JobTitle")
    job_link = "https://www.indeed.com" + atag.get("href")
    job_title = atag.span.text.strip()
    company_name = card.find("span", attrs={"data-testid": "company-name"}).text.strip()

    try:
        job_location = card.find("div", attrs={"data-testid": "text-location"}).text.strip()
    except AttributeError:
        job_location = ""

    try:
        job_description = card.find("div", "result-footer").div.ul.text.strip()
    except AttributeError:
        job_description = ""

    try:
        job_date = card.find("span", "date").text.strip()
        job_date = job_date[job_date.startswith("Posted") and len("Posted"):]
    except AttributeError:
        job_date = ""

    try:
        job_salary = card.find("div", "salary-snippet-container").div.text
    except AttributeError:
        job_salary = ""

    record = (job_title, company_name, job_location, job_description, job_salary, job_date, job_link)
    return record

def main(position, location):
    client = ZenRowsClient("Your id")
    url = get_url(position, location)
    records = [["Index", "Title", "Company", "Location", "Description", "Salary", "Date"]]
    links = []
    page_number = 0
    print("Start scanning...")

    # Extract job data
    while True:
        response = client.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("div", "result")
        
        for card in cards:
            record = get_record(card)
            wrapped_record = ["\n".join(textwrap.wrap(data, width=30)) for data in record[:len(record)-1]]
            records.append(wrapped_record)
            links.append(record[-1])

        if soup.find("a", attrs={"data-testid": "pagination-page-next"}):
            print("Scanning next page...")
            page_number += 10
            url = f"{get_url(position, location)}&start={page_number}"
        else:
            break
    
    # Save job data
    with open("results.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Company", "Location", "Description", "Salary", "Date"])  
        writer.writerows(records)  

    print(tabulate(records, headers="firstrow", tablefmt="fancy_grid", showindex="always"))
    
    while True:
        link_request = input("Enter index to get job link, enter 'q' to quit: ").strip()
        if link_request.lower() == "q":
            break
        elif not link_request.isdigit():
            print("Invalid input.")
        else:
            print(f"Link for job {int(link_request)}: {links[int(link_request)]}")




main(input("Position: "), input("Location: "))
