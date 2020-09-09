import requests
from bs4 import BeautifulSoup
from time import sleep
from csv import writer
class scrapper_quotes():

	def __init__(self,url):
		self.url=url

	def request(self):
		self.response=requests.get(self.url)
		return self.response

	def parser(self):
		self.request()
		self.html=(self.response.text)
		soup=BeautifulSoup(self.html,"html.parser")
		data=soup.select(".quote")
		self.quotes=[[item.find(class_="text").get_text(),item.find(attrs={"itemprop":"author"}).get_text(),item.find("span").find_next("span").a['href']] for item in data]
		
		while soup.find(class_="next"):
			next_page=soup.find(class_="next").a["href"]
			self.url=self.url+f"{next_page}"
			sleep(2)
			self.request()
			self.html=(self.response.text)
			soup=BeautifulSoup(self.html,"html.parser")
			data=soup.select(".quote")
			new_quotes=[[item.find(class_="text").get_text(),item.find(attrs={"itemprop":"author"}).get_text(),item.find("span").find_next("span").a['href']] for item in data]
			self.quotes.extend(new_quotes)
			self.url=self.url.replace(next_page,"")
	def write_quotes_file(self):
		self.parser()
		with open("quotes.csv","w") as file:
			csv_writer=writer(file)
			csv_writer.writerow(["Text","Author_Name","Author_Location"])
			for quote in self.quotes:
				csv_writer.writerow(quote)

def refresh(url):
	scrapper_quotes(url).write_quotes_file()
refresh("http://quotes.toscrape.com")




