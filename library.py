# do połączenia bazy danych z kodem użyłem biblioteki mysql.connector

import mysql.connector

# Do połączenia z bazą danych MySQL używana jest biblioteka mysql.connector. W tym przypadku użyłem użytkownika root na hoście 127.0.0.1, który nie wymaga podawania hasła.

try:
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="biblioteka"
    )
except mysql.connector.Error as err:
    print(f"Błąd podczas łączenia z bazą danych: {err}")
    exit()

# Funkcja dodaj_ksiazke() pozwala na dodanie nowej książki do bazy danych. 
# Użytkownik wprowadza dane dotyczące książki, a następnie funkcja wykonuje zapytanie SQL w celu dodania rekordu do tabeli Ksiazki

def dodaj_ksiazke():
    try:
        tytul = input("Podaj tytuł książki: ")
        autor = input("Podaj autora książki: ")
        gatunek = input("Podaj gatunek książki: ")
        rok_wydania = int(input("Podaj rok wydania książki: "))
        liczba_egzemplarzy = int(input("Podaj liczbę egzemplarzy książki: "))

        cursor = mydb.cursor()
        sql = "INSERT INTO Ksiazki (tytul, autor, gatunek, rok_wydania, liczba_egzemplarzy) VALUES (%s, %s, %s, %s, %s)"
        val = (tytul, autor, gatunek, rok_wydania, liczba_egzemplarzy)
        cursor.execute(sql, val)
        mydb.commit()
        print("Książka dodana.")
    except mysql.connector.Error as err:
        print(f"Błąd podczas dodawania książki: {err}")

# Funkcja usun_ksiazke() umożliwia usunięcie książki z bazy danych.
# Użytkownik podaje ID książki do usunięcia, a następnie funkcja wykonuje zapytanie SQL usuwające rekord z tabeli Ksiazki.


def usun_ksiazke():
    try:
        id_ksiazki = int(input("Podaj ID książki do usunięcia: "))

        cursor = mydb.cursor()
        sql = "DELETE FROM Ksiazki WHERE id = %s"
        val = (id_ksiazki,)
        cursor.execute(sql, val)
        mydb.commit()
        print("Książka usunięta.")
    except mysql.connector.Error as err:
        print(f"Błąd podczas usuwania książki: {err}")

# Funkcja wyswietl_wszystkie_ksiazki() służy do wyświetlania wszystkich książek znajdujących się w bazie danych.
# Wykonuje zapytanie SQL, pobiera wyniki i wyświetla informacje o każdej książce.

def wyswietl_wszystkie_ksiazki():
    try:
        cursor = mydb.cursor()
        sql = "SELECT * FROM Ksiazki"
        cursor.execute(sql)
        results = cursor.fetchall()

        if not results:
            print("Brak książek w bazie danych.")
        else:
            for row in results:
                print("ID:", row[0])
                print("Tytuł:", row[1])
                print("Autor:", row[2])
                print("Gatunek:", row[3])
                print("Rok wydania:", row[4])
                print("Liczba egzemplarzy:", row[5])
                print("-----------------------")
                print("-----------------------")
                print("-----------------------")
                print("-----------------------")
    except mysql.connector.Error as err:
        print(f"Błąd podczas wyświetlania listy ksiązek: {err}")

# Funkcja wypozycz_ksiazke(id_czytelnika, id_ksiazki) pozwala na wypożyczenie książki przez czytelnika.
# Najpierw sprawdza dostępność książki, a następnie sprawdza, czy czytelnik już wypożyczył tę książkę.
# Jeśli książka jest dostępna i czytelnik jej jeszcze nie wypożyczył,
# funkcja aktualizuje liczbę egzemplarzy książki w tabeli Ksiazki i dodaje wpis do tabeli Wypozyczenia.

def wypozycz_ksiazke(id_czytelnika, id_ksiazki):
    try:
        cursor = mydb.cursor()

        # Sprawdzenie dostępności książki
        sql = "SELECT liczba_egzemplarzy FROM Ksiazki WHERE id = %s"
        val = (id_ksiazki,)
        cursor.execute(sql, val)
        result = cursor.fetchone()

        if result is None:
            print("Nie ma książki o podanym ID.")
            return

        liczba_egzemplarzy = result[0]

        if liczba_egzemplarzy <= 0:
            print("Książka niedostępna.")
            return

        # Sprawdzenie, czy czytelnik już wypożyczył tę książkę
        sql = "SELECT id_czytelnika FROM Wypozyczenia WHERE id_ksiazki = %s AND id_czytelnika = %s"
        val = (id_ksiazki, id_czytelnika)
        cursor.execute(sql, val)
        result = cursor.fetchone()

        if result is not None:
            print("Czytelnik już wypożyczył tę książkę.")
            return
        
        sql = "UPDATE Ksiazki SET liczba_egzemplarzy = liczba_egzemplarzy - 1 WHERE id = %s"
        val = (id_ksiazki,)
        cursor.execute(sql, val)

        # Dodanie  do tabeli Wypozyczenia
        sql = "INSERT INTO Wypozyczenia (id_czytelnika, id_ksiazki) VALUES (%s, %s)"
        val = (id_czytelnika, id_ksiazki)
        cursor.execute(sql, val)

        mydb.commit()
        print("Książka wypożyczona.")
    except mysql.connector.Error as err:
        print(f"Błąd podczas wypozyczania ksiazki: {err}")

# Funkcja oddaj_ksiazke(id_czytelnika, id_ksiazki) umożliwia oddanie wypożyczonej książki.
# Sprawdza, czy czytelnik wypożyczył tę konkretną książkę, a następnie aktualizuje liczbę egzemplarzy książki w tabeli Ksiazki i usuwa wpis z tabeli Wypozyczenia.


def oddaj_ksiazke(id_czytelnika, id_ksiazki):
    try:
        cursor = mydb.cursor()

        # Sprawdzenie, czy czytelnik wypożyczył tę książkę
        sql = "SELECT id_czytelnika FROM Wypozyczenia WHERE id_ksiazki = %s AND id_czytelnika = %s"
        val = (id_ksiazki, id_czytelnika)
        cursor.execute(sql, val)
        result = cursor.fetchone()

        if result is None:
            print("Czytelnik nie wypożyczył tej książki.")
            return

        # Aktualizacja liczby egzemplarzy książki
        sql = "UPDATE Ksiazki SET liczba_egzemplarzy = liczba_egzemplarzy + 1 WHERE id = %s"
        val = (id_ksiazki,)
        cursor.execute(sql, val)

        # Usunięcie wpisu z tabeli Wypozyczenia
        sql = "DELETE FROM Wypozyczenia WHERE id_ksiazki = %s AND id_czytelnika = %s"
        val = (id_ksiazki, id_czytelnika)
        cursor.execute(sql, val)

        mydb.commit()
        print("Książka zwrócona.")
    except mysql.connector.Error as err:
        print(f"Błąd podczas oddawania książki: {err}")

# Funkcja dodaj_czytelnika() pozwala na dodanie nowego czytelnika do bazy danych.
# Użytkownik wprowadza dane dotyczące czytelnika, a następnie funkcja wykonuje zapytanie SQL w celu dodania rekordu do tabeli Czytelnicy.

def dodaj_czytelnika(imie, nazwisko):
    try:
        cursor = mydb.cursor()
        
        sql = "INSERT INTO Czytelnicy (imie, nazwisko) VALUES (%s, %s)"
        val = (imie, nazwisko)
        cursor.execute(sql, val)

        mydb.commit()
        print("Czytelnik dodany do bazy danych.")
    except mysql.connector.Error as err:
        print(f"Błąd podczas dodawania czytelnika: {err}")

# Funkcja wyswietl_wszystkich_czytelnikow() służy do wyświetlania wszystkich czytelników znajdujących się w bazie danych.
# Wykonuje zapytanie SQL, pobiera wyniki i wyświetla informacje o każdym czytelniku.



def wyswietl_czytelnikow():
    try:
        cursor = mydb.cursor()
        sql = "SELECT * FROM Czytelnicy"
        cursor.execute(sql)
        results = cursor.fetchall()

        if not results:
            print("Brak czytelników w bazie danych.")
        else:
            for row in results:
                print("ID:", row[0])
                print("Imię:", row[1])
                print("Nazwisko:", row[2])
                print("-----------------------")
    except mysql.connector.Error as err:
        print(f"Błąd podczas wyświetlania listy czytelników: {err}")

def usun_czytelnika():
    try:
        id_czytelnika = int(input("Podaj ID czytelnika do usunięcia: "))

        cursor = mydb.cursor()
        sql = "DELETE FROM Czytelnicy WHERE id = %s"
        val = (id_czytelnika,)
        cursor.execute(sql, val)
        mydb.commit()
        print("Użytkownik usunięty.")
    except mysql.connector.Error as err:
        print(f"Błąd podczas usuwania czytelników: {err}")

# Funkcja sprawdz_wypozyczenia() służy do sprawdzienia książek wypożyczonych przez czytelnika.
# Wykonuje zapytanie SQL, pobiera wyniki i wyświetla informacje o książkach wypożyczonych przez konkretnego czytelnika.

def sprawdz_wypozyczenia(id_czytelnika):
    try:
        cursor = mydb.cursor()
        sql = "SELECT Ksiazki.tytul, Ksiazki.autor FROM Wypozyczenia INNER JOIN Ksiazki ON Wypozyczenia.id_ksiazki = Ksiazki.id WHERE Wypozyczenia.id_czytelnika = %s"
        val = (id_czytelnika,)
        cursor.execute(sql, val)
        results = cursor.fetchall()

        if not results:
            print("Czytelnik nie ma wypożyczonych książek.")
        else:
            print("Książki wypożyczone przez czytelnika:")
            for row in results:
                print("Tytuł:", row[0])
                print("Autor:", row[1])
                print("-----------------------")
    except mysql.connector.Error as err:
        print(f"Błąd podczas sprawdzania wypozyczeń: {err}")

# funkcja pozwala na wyświetlenie informacji o wypożyczonych książkach


def wyswietl_wypozyczenia():
    try:
        cursor = mydb.cursor()
        sql = "SELECT Czytelnicy.imie, Czytelnicy.nazwisko, Ksiazki.tytul FROM Wypozyczenia INNER JOIN Czytelnicy ON Wypozyczenia.id_czytelnika = Czytelnicy.id INNER JOIN Ksiazki ON Wypozyczenia.id_ksiazki = Ksiazki.id"
        cursor.execute(sql)
        results = cursor.fetchall()

        if not results:
            print("Brak wypożyczonych książek.")
        else:
            print("Wypożyczone książki:")
            for row in results:
                print("Czytelnik:", row[0], row[1])
                print("Tytuł książki:", row[2])
                print("-----------------------")
    except mysql.connector.Error as err:
        print(f"Błąd podczas wyświetlania wypoyczeń: {err}")
# główny panel nawigacyjny, dzięki któremu użytkownik w prosty sposób może korzystać z funkcji programu

def system_nawigacyjny():
    while True:
        print("--- MENU ---")
        print("1. Dodaj książkę")
        print("2. Usuń książkę")
        print("3. Wypożycz książkę")
        print("4. Oddaj książkę")
        print("5. Wyświetl wszystkie książki")
        print("6. Dodaj czytelnika.")
        print("7. Wyświetl wszystkich czytelników")
        print("8. Sprawdź wypożyczenia czytelnika")
        print("9. Wyświetl wszystkie wypożyczenia")
        print("10. Usuń czytelnika")
        print("0. Wyjście")


        wybor = input("Wybierz opcję: ")

        if wybor == "1":
            dodaj_ksiazke()
        elif wybor == "2":
            usun_ksiazke()
        elif wybor == "3":
            id_czytelnika = int(input("Podaj ID czytelnika: "))
            id_ksiazki = int(input("Podaj ID książki do wypożyczenia: "))
            wypozycz_ksiazke(id_czytelnika, id_ksiazki)
        elif wybor == "4":
            id_czytelnika = int(input("Podaj ID czytelnika: "))
            id_ksiazki = int(input("Podaj ID książki do oddania: "))
            oddaj_ksiazke(id_czytelnika, id_ksiazki)
        elif wybor == "5":
            wyswietl_wszystkie_ksiazki()
        elif wybor == "6":
            imie = input("Podaj imię czytelnika: ")
            nazwisko = input("Podaj nazwisko czytelnika: ")
            dodaj_czytelnika(imie, nazwisko)
        elif wybor == "7":
            print(wyswietl_czytelnikow())
        elif wybor == "8":
            id_czytelnika = int(input("Podaj ID czytelnika: "))
            sprawdz_wypozyczenia(id_czytelnika)
        elif wybor == "9":
            wyswietl_wypozyczenia()
        elif wybor == "10":
            usun_czytelnika()
        elif wybor == "0":
            break
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")
            
try:
    system_nawigacyjny()
except KeyboardInterrupt:
    print("Program zakończony przez użytkownika.")
except Exception as err:
    print(f"Wystąpił nieoczekiwany błąd: {err}")
finally:
    mydb.close()