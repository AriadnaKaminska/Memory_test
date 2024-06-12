from psychopy import visual, core, event
import random
import DataContainer
import plansze

#tu jest ciężko i jestem przekonana, że da się to zrobić zgrabniej, ale zgrabniej nie chciało działać tyle razy, że niestety jest tak
#pojedyńczy etap obejmuje: wyświetlenie siatki i losowych kwadratów, zniknięcie losowych kwadratów i pojawianie się nowych po kliknięciu

def calculate_coordinates(pozycja2, rozmiar_siatki):
    y = (pozycja2 // rozmiar_siatki - (rozmiar_siatki / 2 - 0.5)) * 0.24
    x = (pozycja2 % rozmiar_siatki - (rozmiar_siatki / 2 - 0.5)) * 0.24
    return x, y
def kwadraty_random(win, il_randomowych_kwadratow, rozmiar_siatki):
    pozycje = list(range(rozmiar_siatki**2))
    random.shuffle(pozycje)
    pozycje = pozycje[:il_randomowych_kwadratow]

    kwadraty = []
    for pozycja2 in pozycje:
        x, y = calculate_coordinates(pozycja2, rozmiar_siatki)
        nowy_kwadrat = visual.Rect(win, pos=(x, y), width=0.2, height=0.2, fillColor=(240/255, 250/255, 250/255))
        kwadraty.append((pozycja2, nowy_kwadrat))

    return kwadraty
def kwadraty_siatka(win, rozmiar_siatki):
    kwadraty_siatka = []
    for pozycja2 in range(rozmiar_siatki**2):
        x, y = calculate_coordinates(pozycja2, rozmiar_siatki)
        kwadrat = visual.Rect(win, width=0.2, height=0.2, fillColor="blue", pos=(x, y))
        kwadraty_siatka.append((pozycja2, kwadrat))

    return kwadraty_siatka
def Rysowanie_siatki_kwadratow(kwadraty_siatka_lista):
    for _, kwadrat in kwadraty_siatka_lista:
        kwadrat.draw()
def Rysowanie_losowych_kwadratow(random_kwadraty):
    for _, kwadrat in random_kwadraty:
        kwadrat.draw()
def Rysowanie_nowych_kwadratow(zaz_kwadraty):
    for kwadrat in zaz_kwadraty:
        kwadrat.draw()
def Rysowanie_error_kwadratow(error_kwadraty):
    for kwadrat in error_kwadraty:
        kwadrat.draw()
def handle_selection(stage_data, pos_squares, idx, m_clock, rozmiar_siatki):
    event.Mouse()
    stage_data.selectedSquares.append((pos_squares[idx][0] % rozmiar_siatki, pos_squares[idx][0] // rozmiar_siatki))
    stage_data.actionTimes.append(m_clock.getTime())
    m_clock.reset()

def run_stage(stage_number, win, il_randomowych_kwadratow, rozmiar_siatki):
    if (rozmiar_siatki ** 2) / 2 <= il_randomowych_kwadratow:
        rozmiar_siatki += 1

    mouse = event.Mouse(visible=True)
    kwadraty_siatka_lista = kwadraty_siatka(win, rozmiar_siatki)
    random_kwadraty = kwadraty_random(win, il_randomowych_kwadratow, rozmiar_siatki)
    zaz_kwadraty = []
    error_kwadraty = []

    #to do zapisywania danych
    squares_locations = [(pos % rozmiar_siatki, pos // rozmiar_siatki) for pos, _ in random_kwadraty]
    stage_data = DataContainer.Stage(stage_number, squares_locations, [], [], 0, [])
    m_clock = core.Clock()

    #pojawienie się siatki i losowych kwadratów
    Rysowanie_siatki_kwadratow(kwadraty_siatka_lista)
    Rysowanie_losowych_kwadratow(random_kwadraty)
    win.flip()
    #ziknięcie losowych kwadratów, w specyfikacji było że po 2 sekundach, w grze na której się wzorowałam
    #też mi się wydaje, że było 2s, ale po odpalaniu tego n-ty raz okazuje się, że 2 sekundy to już mikrodrzemka
    core.wait(1.5)#więc jest mniej
    strikes_change = False
    flaga = 0

    # Główna pętla do rysowania kwadratów po kliknięciu
    while True:
        Rysowanie_siatki_kwadratow(kwadraty_siatka_lista)
        Rysowanie_nowych_kwadratow(zaz_kwadraty)
        Rysowanie_error_kwadratow(error_kwadraty)
        win.flip()

        if mouse.getPressed()[0]:  # Sprawdzanie kliknięcia lewym przyciskiem myszy
            mouse_pos = mouse.getPos()
            for pozycja2, kwadrat in kwadraty_siatka_lista:
                if kwadrat.contains(mouse):
                    if any(pozycja2 == pos for pos, _ in random_kwadraty):
                        handle_selection(stage_data, kwadraty_siatka_lista,
                                         kwadraty_siatka_lista.index((pozycja2, kwadrat)), m_clock, rozmiar_siatki)
                        x, y = calculate_coordinates(pozycja2, rozmiar_siatki)
                        zaz_kwadrat = visual.Rect(win, pos=(x, y), width=0.2, height=0.2, fillColor="white")
                        zaz_kwadraty.append(zaz_kwadrat)
                    else:
                        plansze.show_komunikat_bledu(win)
                        x, y = calculate_coordinates(pozycja2, rozmiar_siatki)
                        error_kwadrat = visual.Rect(win, pos=(x, y), width=0.2, height=0.2, color=(10, 26, 26), colorSpace='rgb255')
                        error_kwadraty.append(error_kwadrat)
                        stage_data.errorCount += 1
                        stage_data.errorLocations.append((pozycja2 % rozmiar_siatki, pozycja2 // rozmiar_siatki))
                        strikes_change = True #to do oznaczania błędów w poj. turze na różnych etapach
                    break

            # Sprawdzanie zakończenia programu (np. naciśnięcie klawisza ESC)
            if len(zaz_kwadraty) == len(random_kwadraty) or len(error_kwadraty) > 1:
                if len(error_kwadraty) > 1:
                    flaga=1 #to do oznaczania, że były dwa błędy na jednym etapie
                Rysowanie_siatki_kwadratow(kwadraty_siatka_lista)
                Rysowanie_nowych_kwadratow(zaz_kwadraty)
                Rysowanie_error_kwadratow(error_kwadraty)
                win.flip()
                core.wait(0.5)
                break

            # Resetowanie stanu myszy po kliknięciu
            while mouse.getPressed()[0]:
                pass



    return il_randomowych_kwadratow + 1, strikes_change, flaga, stage_data