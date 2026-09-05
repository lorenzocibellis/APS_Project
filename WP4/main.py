from CentralSystem.data.database import Database
from CentralSystem.rm import RM
from thirdParties.ca import CA
from users.clinic import Clinica
from users.patient import Paziente
from users.medic import Medico
from globalClasses.enumerations import Role


def menu_clinica(clinica):
    while True:
        print(f"\n--- MENU CLINICA (ID: {clinica._ID}) ---")
        print("1. Crea e Invia Referto")
        print("2. Revoca Referto")
        print("3. Aggiorna Referto")
        print("4. Richiedi Referto (ref_request)")
        print("5. Richiedi Registro di Audit (aud_request)")
        print("6. Visualizza Registri di Audit Salvati")
        print("0. Torna al menu principale")

        scelta = input("Seleziona un'operazione: ").strip()

        if scelta == "1":
            id_paziente = input("ID Paziente: ").strip()
            id_referto_locale = input("ID Referto Locale (es. REF_001): ").strip()
            contenuto = input("Contenuto del referto: ").strip()
            clinica.createAndSendReferto(id_paziente, id_referto_locale, contenuto)
        elif scelta == "2":
            id_paziente = input("ID Paziente: ").strip()
            id_referto = input("ID Referto Univoco (es. CLINICA_ID_REF_001): ").strip()
            motivo = input("Motivo della revoca: ").strip()
            clinica.revokeReferto(id_paziente, id_referto, motivo)
        elif scelta == "3":
            id_paziente = input("ID Paziente: ").strip()
            id_referto = input("ID Referto Univoco (es. CLINICA_ID_REF_001): ").strip()
            nuovo_contenuto = input("Nuovo contenuto referto: ").strip()
            clinica.updateReferto(id_paziente, id_referto, nuovo_contenuto)
        elif scelta == "4":
            id_paziente = input("ID Paziente: ").strip()
            id_referto = input("ID Referto Univoco (es. CLINICA_ID_REF_001): ").strip()
            clinica.ref_request(id_paziente, id_referto)
        elif scelta == "5":
            id_paziente = input("ID Paziente: ").strip()
            id_referto = input("ID Referto Univoco (es. CLINICA_ID_REF_001): ").strip()
            clinica.aud_request(id_paziente, id_referto)
        elif scelta == "6":
            print("\n[Registri di Audit salvati localmente dalla Clinica]")
            if clinica._registers:
                for paz_id, refs in clinica._registers.items():
                    for ref_id, reg in refs.items():
                        print(f"-> Paziente {paz_id}, Referto {ref_id}:\n{reg}")
            else:
                print("Nessun registro presente.")
        elif scelta == "0":
            break
        else:
            print("Opzione non valida.")


def menu_paziente(paziente):
    while True:
        print(f"\n--- MENU PAZIENTE (ID: {paziente._ID}) ---")
        print("1. Richiedi Chiavi Referto (key_request)")
        print("2. Richiedi Referto Cifrato (ref_request)")
        print("3. Richiedi Registro di Audit (aud_request)")
        print("4. Visualizza Registri di Audit Salvati")
        print("0. Torna al menu principale")

        scelta = input("Seleziona un'operazione: ").strip()

        if scelta == "1":
            id_referto = input("ID Referto Univoco (es. C0_REF_001): ").strip()
            paziente.key_request(id_referto)
        elif scelta == "2":
            id_referto = input("ID Referto Univoco (es. C0_REF_001): ").strip()
            paziente.ref_request(id_referto)
        elif scelta == "3":
            id_referto = input("ID Referto Univoco (es. C0_REF_001): ").strip()
            paziente.aud_request(id_referto)
        elif scelta == "4":
            print("\n[Registri di Audit salvati localmente]")
            if paziente._registers:
                for ref_id, reg in paziente._registers.items():
                    print(f"-> Referto {ref_id}:\n{reg}")
            else:
                print("Nessun registro presente.")
        elif scelta == "0":
            break
        else:
            print("Opzione non valida.")


def menu_medico(medico):
    while True:
        print(f"\n--- MENU MEDICO (ID: {medico._ID}) ---")
        print("1. Richiedi Autorizzazione al Paziente (vis_request)")
        print("2. Richiedi Referto Cifrato a RM (ref_request)")
        print("3. Richiedi Registro di Audit a RM (aud_request)")
        print("4. Visualizza Autorizzazioni e Registri Salvati")
        print("0. Torna al menu principale")

        scelta = input("Seleziona un'operazione: ").strip()

        if scelta == "1":
            id_paziente = input("ID Paziente: ").strip()
            id_referto = input("ID Referto Univoco (es. C0_REF_001): ").strip()
            medico.vis_request(id_paziente, id_referto)
        elif scelta == "2":
            id_paziente = input("ID Paziente: ").strip()
            id_referto = input("ID Referto Univoco (es. C0_REF_001): ").strip()
            medico.ref_request(id_paziente, id_referto)
        elif scelta == "3":
            id_paziente = input("ID Paziente: ").strip()
            id_referto = input("ID Referto Univoco (es. C0_REF_001): ").strip()
            medico.aud_request(id_paziente, id_referto)
        elif scelta == "4":
            print("\n[Autorizzazioni Salvate]")
            print(medico._auth)
            print("\n[Registri di Audit Salvati]")
            print(medico._registers)
        elif scelta == "0":
            break
        else:
            print("Opzione non valida.")


def registraNuovoUtente(ca, rm, cliniche, pazienti, medici):
    print("\n--- REGISTRAZIONE NUOVO UTENTE ---")
    print("1. Nuova Clinica")
    print("2. Nuovo Paziente")
    print("3. Nuovo Medico")
    print("0. Annulla")

    scelta = input("Seleziona tipo di utente: ").strip()

    if scelta == "1":
        nuovo = Clinica(ca, rm)
        cliniche.append(nuovo)
        print(f"\n[+] Creata con successo Clinica (ID: {nuovo._ID})")
    elif scelta == "2":
        nuovo = Paziente(ca, rm)
        pazienti.append(nuovo)
        print(f"\n[+] Creato con successo Paziente (ID: {nuovo._ID})")
    elif scelta == "3":
        nuovo = Medico(ca, rm)
        medici.append(nuovo)
        print(f"\n[+] Creato con successo Medico (ID: {nuovo._ID})")
    elif scelta == "0":
        return
    else:
        print("Scelta non valida.")


def main():
    ca = CA()
    db = Database()
    rm = RM(Role.RM, ca, db)

    # 2 utenti di default per ogni categoria
    cliniche = [Clinica(ca, rm), Clinica(ca, rm)]      # C0, C1
    pazienti = [Paziente(ca, rm), Paziente(ca, rm)]    # P0, P1
    medici = [Medico(ca, rm), Medico(ca, rm)]          # M0, M1

    while True:
        print("\n==========================================")
        print("   SISTEMA DI GESTIONE REFERTI MEDICI    ")
        print("==========================================")
        print("Seleziona l'utente con cui operare:")

        menu_map = {}
        idx = 1

        print("\n--- CLINICHE ---")
        for c in cliniche:
            print(f"{idx}. Clinica (ID: {c._ID})")
            menu_map[str(idx)] = ("Clinica", c)
            idx += 1

        print("\n--- PAZIENTI ---")
        for p in pazienti:
            print(f"{idx}. Paziente (ID: {p._ID})")
            menu_map[str(idx)] = ("Paziente", p)
            idx += 1

        print("\n--- MEDICI ---")
        for m in medici:
            print(f"{idx}. Medico (ID: {m._ID})")
            menu_map[str(idx)] = ("Medico", m)
            idx += 1

        print("\n--- GESTIONE UTENTI ---")
        idx_registra = str(idx)
        print(f"{idx_registra}. Registra nuovo utente")
        print("0. Esci")

        scelta = input("\nScelta: ").strip()

        if scelta == "0":
            print("\nChiusura dell'applicazione.")
            break
        elif scelta == idx_registra:
            registraNuovoUtente(ca, rm, cliniche, pazienti, medici)
        elif scelta in menu_map:
            ruolo, utente = menu_map[scelta]
            if ruolo == "Clinica":
                menu_clinica(utente)
            elif ruolo == "Paziente":
                menu_paziente(utente)
            elif ruolo == "Medico":
                menu_medico(utente)
        else:
            print("Scelta non valida.")


if __name__ == "__main__":
    main()