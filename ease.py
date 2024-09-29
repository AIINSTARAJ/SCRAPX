from bs4 import BeautifulSoup #type: ignore
import requests #type: ignore


def scrap(url):
    code = requests.get(url).text
    soup = BeautifulSoup(code,"lxml")
    books = soup.find_all("div", class_ = "book-item col-sm-3")
    for book in books:
        info_class =  book.find("div", id = "book-info")
        Title = info_class.find("a", id = "title").text
        Author = info_class.find("p", id = "author").text
        Publisher = info_class.find("p", id = "publisher").text
        Category = info_class.find("p", id = "category").text
        Year = info_class.find("p", id = "year").text
        image = book.find("img")['src']
        link = info_class.find("a")['href']

        print(Title, Author, Publisher, Category, Year)
        print("IMG_LINK: ",image)
    

if __name__ == "__main__":
    scrap("http://127.0.0.1:5000")
    

