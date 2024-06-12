import plansze
import tura
import DataContainer
import dataclasses

from psychopy import visual, core
import json
import datetime
import os

def save_results(data_container):
    data = dataclasses.asdict(data_container)
    json_data = json.dumps(data)

    with open(f"Results\\memory_test_{str(datetime.datetime.now()).replace(' ', '_').replace(':', '-')[:-7]}.json", "x") as file:
        file.write(json_data)

def main():
    win = visual.Window(units="height",  fullscr=True, monitor=None, color=(10, 26, 26), colorSpace='rgb255')

    data_container = DataContainer.DataContainer([])

    plansze.show_instrukcja(win)
    plansze.show_trening(win)
    result = tura.odpal_ture(0, win, True).lastStage
    plansze.show_treining_koniec(win, result)
    for i in range(3):
        session_data = tura.odpal_ture(i, win, False)
        data_container.sessions.append(session_data)
        plansze.show_wynik(win, i+1, session_data.lastStage)
    plansze.show_plansza_koncowa(win, data_container.sessions[-1].lastStage)


    win.close()
    core.quit()


if __name__ == '__main__':
    main()


