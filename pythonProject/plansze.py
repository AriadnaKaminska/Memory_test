import instrukcja
from psychopy import visual, core, event

#tutaj są komunikaty tekstowe
def show_plansza1(win, text, to_continue="\n\n\nAby kontynuować, naciśnij dowolne miejsce na ekranie.", size=None):
    msg = visual.TextBox2(win, text=text+to_continue, font="Open Sans", alignment="centre", letterHeight=size)
    msg.draw()
    win.flip()

    mouse = event.Mouse(visible=True)
    while mouse.getPressed() == [0, 0, 0]:
        core.wait(0.0001)
    event.clearEvents()


def show_instrukcja(win):
    show_plansza1(win, instrukcja.INSTRUKCJA, size=0.02)


def show_komunikat_bledu(win):
    msg = visual.TextBox2(win, text="BŁĄD!", letterHeight=0.2, bold=True, font="Open Sans", alignment="centre")
    msg.draw()
    win.flip()
    core.wait(0.5)
    event.clearEvents()

def show_trening(win):
    show_plansza1(win, "Za chwilę rozpoczniesz krótką sesję treningową.", size=0.025)


def show_treining_koniec(win, wynik):
    show_plansza1(win, f"Zakończono sesję treningową."
                       f"\n\nLiczba ukończonych etapów: {wynik-4} na 3 możliwe."
                       f"\n\n Przed Tobą pierwsza sesja eksperymentalna.", size=0.025)


def show_wynik(win, nr_tury, wynik):
    if nr_tury == 3:
        return

    show_plansza1(win, f"Zakończono {nr_tury}. sesję eksperymentalną."
                       f"\n\nLiczba ukończonych etapów: {wynik-4} na 17 możliwych."
                       f"\n\nPrzed Tobą {nr_tury+1}. sesja eksperymentalna.", size=0.025)

def show_plansza_koncowa(win, wynik):
    show_plansza1(win, f"Zakończono ostatnią sesję eksperymentalną."
                       f"\n\nLiczba ukończonych etapów: {wynik-4} na 17 możliwych."
                       f"\n\nBardzo dziękujemy za wzięcie udziału w badaniu!",
               "\n\n\nW celu wyjścia, naciśnij dowolne miejsce na ekranie.", size=0.025)