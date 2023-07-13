from bs4 import BeautifulSoup
import json
import requests
from tabulate import tabulate

url = 'http://52.32.1.180:8080/SPLOT/SplotAnalysesServlet?action=select_model&enableSelection=false&&showModelDetails=true'  # replace with your URL

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

headers = [header.text for header in soup.find_all('th')]

table_data = []
for row in soup.find_all('tr'):
    columns = row.find_all('td')
    output_row = {}
    for header, column in zip(headers, columns):
        if column.find('a'):  # if the column contains a link
            # extract the text after the last slash
            output_row[header] = column.find('a')['href'].split('=')[-1]
        else:
            output_row[header] = column.text.strip()
    if output_row:
        table_data.append(output_row)

with open('statistics.json', 'w') as f:
    json.dump(table_data, f, indent=4)

markdown_table = tabulate(table_data, headers="keys", tablefmt="pipe")

with open('README.md', 'a') as f:
    f.write("Below, you can find the current statistics of the models from SPLOT\r\n")
    f.write(markdown_table)