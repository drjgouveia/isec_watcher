from searcher import Searcher
from decouple import config

if __name__ == "__main__":
    searcher = Searcher(config('STUDENT_EMAIL', default=""), config('STUDENT_PASSWORD', default=""))
    searcher.login()
    searcher.go_to_inscricoes()
    results = searcher.availability_date_checker()
    if results:
        print("There is something!")
    else:
        print("No grammy for you :(")
