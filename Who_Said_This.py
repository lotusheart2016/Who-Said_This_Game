import requests
from bs4 import BeautifulSoup
from random import choice as choose
class GuessWho():
	switch=True
	base_url="http://quotes.toscrape.com"

	def __init__(self):
		self.url=GuessWho.base_url

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
			# sleep(2)
			self.request()
			self.html=(self.response.text)
			soup=BeautifulSoup(self.html,"html.parser")
			data=soup.select(".quote")
			new_quotes=[[item.find(class_="text").get_text(),item.find(attrs={"itemprop":"author"}).get_text(),item.find("span").find_next("span").a['href']] for item in data]
			self.quotes.extend(new_quotes)
			self.url=self.url.replace(next_page,"")

		return self.quotes

	def show_quote(self):
		if GuessWho.switch:
			self.parser()
			self.shown_random_quote=choose(self.quotes)
			self.shown_quote_text=self.shown_random_quote[0]
			self.shown_quote_author=self.shown_random_quote[1]
			self.shown_quote_author_url=self.url+f"{self.shown_random_quote[2]}"
			self.res=requests.get(self.shown_quote_author_url)
			self.bio=(self.res.text)
			soup=BeautifulSoup(self.bio,"html.parser")
			self.bio_data=f"{soup.find(class_='row header-box').find_next('h1').text}\n{soup.find(class_='author-details').text}\n\n{soup.find(class_='author-description').text}"
			self.author_born_date=soup.find(class_='author-born-date').text
			self.author_born_location=soup.find(class_='author-born-location').text
			self.guess_remaining=4
			# print(self.shown_quote_author)
			self.user_answer=input(f"Here is a quote: \n {self.shown_quote_text}\n Who Said this ? Guesses Remaining {self.guess_remaining}.\n")
			self.check_answer()

	def check_answer(self):
		self.process_author_names()
		if self.user_answer_list==self.shown_quote_author_list:
			self.know_more=input(f"Bingo !!! You got the correct answer. To know more about {self.shown_quote_author} type 'Y' OR prese any other key to continuie.\n")
			self.about_author()
			self.terminal()
		else:
			self.guess_remaining-=1
			if self.guess_remaining>0:
				user_res=input(f"Sorry !!! Wrong Answer \n Guesses Reamining {self.guess_remaining}.\nTry Again ? Enter 'Y' to conintuie or any other key to reveal the answer.\n\n")
				if user_res.upper()=="Y":
					self.hints()
				else:
					self.reveal_answer()
			else:
				self.reveal_answer()

	def about_author(self):
		if self.know_more.upper()=="Y":
				print(self.bio_data)

	def reveal_answer(self):
		self.know_more=input(f"The correct answer is {self.shown_quote_author}. To know more about {self.shown_quote_author}, type 'Y' OR press any other key to continuie.\n\n")
		self.about_author()
		self.terminal()
	def terminal(self):
		user_res=input(f"Are you up for another game ? presey 'Y' to play a new 'Said Who?' Game OR press any other key to terminate and exit.\n\n")
		if user_res.upper()=='Y':
			self.show_quote()
		else:
			return print("Thanks for playing 'Said Who ?' game. We look forward to have you again. So long , have a nice day.")

	def hints(self):
		if self.guess_remaining==3:
			self.user_answer=input(f"Hmmm... The author was born on {self.author_born_date} in {self.author_born_location}.\n\n Can you guess the correct answer now ? Enter answer or press 'T' to terminate the game and exit.\n\n ")
			if self.user_answer.upper()=='T':
				self.reveal_answer()
				print("Thanks for playing 'Said Who ?' game. We look forward to have you again. So long , have a nice day.")
			else:
				self.check_answer()

		elif self.guess_remaining==2:
			self.user_answer=input(f"Well...Let me think what more I can reveal !!!\n The author's First name starts with letter '{self.shown_quote_author[0].upper()}'.\n\n Can you guess the correct answer now ? Enter answer or press 'T' to terminate the game and exit.\n\n ")
			if self.user_answer.upper()=='T':
				self.reveal_answer()
				print("Thanks for playing 'Said Who ?' game. We look forward to have you again. So long , have a nice day.")
			else:
				self.check_answer()

		elif self.guess_remaining==1:
			self.user_answer=input(f"Well, well well-This is your lasat hint !!!!\n The author's Last name starts with letter '{self.shown_quote_author.split(' ')[-1][0].upper()}'.\n\n Can you guess the correct answer now ? Enter answer or press 'T' to terminate the game and exit.\n\n ")
			if self.user_answer.upper()=='T':
				self.reveal_answer()
				print("Thanks for playing 'Said Who ?' game. We look forward to have you again. So long , have a nice day.")
			else:
				self.check_answer()
	def process_author_names(self):
		self.user_answer_list=[alphab for alphab in self.user_answer.upper() if alphab!=" " and alphab!=' ' and alphab!='.']
		self.shown_quote_author_list=[alphab for alphab in self.shown_quote_author.upper() if alphab!=" " and alphab!=' ' and alphab!='.']
		



def start_game():
		GuessWho().show_quote()
start_game()




