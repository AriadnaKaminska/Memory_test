import DataContainer
import poj_etap

#tu mamy procedurę pojedyńczej tury, badanie składa się z trzech tur plus jednej treningowej
#tura kończy się  gdy ktoś popełni trzy razy błąd w trzech różnych etapach LUB dwa w jednym etapie
def odpal_ture(session_number, win, is_training):
    session_data = DataContainer.Session(session_number+1, [], [], 0)
    il_randomowych_kwadratow = 3
    rozmiar_siatki = 3
    strikes = 0
    stage_number = 1
    flaga = 0

    while strikes < 3 and il_randomowych_kwadratow <= 20 and flaga == 0 and (not is_training or il_randomowych_kwadratow <= 6):
        il_randomowych_kwadratow, strikes_change, flaga, stage_data = poj_etap.run_stage(stage_number, win, il_randomowych_kwadratow, rozmiar_siatki)

        if strikes_change:
            session_data.errorStages.append(stage_number)
            strikes += 1

        session_data.stages.append(stage_data)
        stage_number += 1

    session_data.lastStage = min(il_randomowych_kwadratow, 20)
    return session_data
