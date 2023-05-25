import re

import requests
from bs4 import BeautifulSoup


def main():

    # Firstly, I wanted to know how many pages are there in the website.
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
    }
    # sending a html get request to the desired website
    url = "https://business.sdsu.edu/about/faculty-staff-listing"
    response = requests.get(url, headers=headers)

    # creating a beautifulsoup object
    soup = BeautifulSoup(response.content, "html.parser")

    # finding no of pages. I wanna some way to combine the first two find_all
    fac_list = soup.find_all("section", class_="grid")

    page_class = fac_list[0].find_all("div", class_="pagination")

    page_list = page_class[0].find_all("a")

    # no_of_pages is the second last element
    no_of_pages = int(page_list[-2].text)
    prof_list = []

    # iterating through the no of pages
    for i in range(1, no_of_pages):

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
        }
        # iterating through different pages
        url = "https://business.sdsu.edu/about/faculty-staff-listing?page=" + str(i)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        fac_list = soup.find_all("article", class_="list-card")

        # I was able to find name easily, but webiste did not have just names of professors,
        # they had staff and everyone else out there. So, if someone has professor in his
        # title he's the one I care about

        for j in fac_list:
            name = j.find("h2").text
            if j.find("span", class_="list-title"):
                tit = j.find("span", class_="list-title").text
                if "professor" in tit.lower():
                    prof_list.append(
                        re.sub(
                            r",",
                            "",
                            re.sub(r"\b[Pp]\.?\s?[Hh]\.?\s?[Dd]\.?\b", " ", name),
                        )
                    )

    # printing the name of all the professors
    for k in prof_list:
        print(k)


if __name__ == "__main__":
    main()
