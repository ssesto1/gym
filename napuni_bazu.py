import os
import django

# Inicijalizacija Django okruženja
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gym.settings')
django.setup()

from workouts.models import Program, DanTreninga, Vjezba

def pokreni_punjenje():
    print("🚀 Pokrećem automatsko punjenje baze...\n")

    # 1. KREIRANJE PROGRAMA (Ispravljeno: uklonjen nepostojeći 'ukupno_dana')
    p1, created = Program.objects.get_or_create(
        naziv="PPL (Push/Pull/Legs) ZA MUŠKARCE",
        opis="Napredni 3-dnevni split za maksimalnu hipertrofiju. Fokus na teške osnovne vježbe i izolaciju slabih točaka."
    )
    
    p2, created = Program.objects.get_or_create(
        naziv="Full Body Početnički",
        opis="Idealan program za početnike. Pogađa sve mišićne skupine 2 puta tjedno za optimalan početni rast."
    )

    print("✅ Programi kreirani.")

    # 2. KREIRANJE DANA ZA PPL PROGRAM
    dan_push, _ = DanTreninga.objects.get_or_create(program=p1, naziv="Dan 1: Push (Prsa, Ramena, Triceps)")
    dan_pull, _ = DanTreninga.objects.get_or_create(program=p1, naziv="Dan 2: Pull (Leđa, Biceps)")
    dan_legs, _ = DanTreninga.objects.get_or_create(program=p1, naziv="Dan 3: Noge (Kvadriceps, Loža, Listovi)")

    # 3. KREIRANJE DANA ZA FULL BODY PROGRAM
    dan_fb1, _ = DanTreninga.objects.get_or_create(program=p2, naziv="Trening A (Fokus: Čučanj i Potisci)")
    dan_fb2, _ = DanTreninga.objects.get_or_create(program=p2, naziv="Trening B (Fokus: Mrtvo dizanje i Vučenja)")

    print("✅ Dani treninga kreirani.")

    # 4. KREIRANJE VJEŽBI (S YouTube linkovima Jeff Nipparda i RP Hypertrophy)
    vjezbe_baza = [
        # --- PUSH VJEŽBE ---
        {
            "dan": dan_push, "broj": 1, "naziv": "Bench Press šipkom", 
            "url": "https://www.youtube.com/embed/vcBig73ojpE",
            "upute": "Legni na klupu, spoji lopatice. Uhvati šipku malo šire od ramena. Kontrolirano spusti do donjeg dijela prsa i eksplozivno potisni."
        },
        {
            "dan": dan_push, "broj": 2, "naziv": "Kosi potisak bučicama", 
            "url": "https://www.youtube.com/embed/8iPEnn-ltC8",
            "upute": "Klupa na 30-45 stupnjeva. Spuštaj bučice duboko do prsa za maksimalno istezanje gornjeg dijela prsa."
        },
        {
            "dan": dan_push, "broj": 3, "naziv": "Overhead Press (Potisak iznad glave)", 
            "url": "https://www.youtube.com/embed/_RlRDWO2jfg",
            "upute": "Stisni gluteus i trup. Potisni šipku tik uz lice prema gore. Zaključaj laktove na vrhu."
        },
        {
            "dan": dan_push, "broj": 4, "naziv": "Lateralno podizanje bučicama", 
            "url": "https://www.youtube.com/embed/WJm9OskIGfs",
            "upute": "Lagana fleksija u laktu, diži bučice u stranu kao da izlijevaš vodu iz vrčeva na vrhu."
        },
        {
            "dan": dan_push, "broj": 5, "naziv": "Triceps ekstenzija sajlom", 
            "url": "https://www.youtube.com/embed/nRiJVZDpdY0",
            "upute": "Laktovi prikovani uz tijelo. Gurni sajlu prema dolje i raširi konop na dnu za jaču kontrakciju."
        },

        # --- PULL VJEŽBE ---
        {
            "dan": dan_pull, "broj": 1, "naziv": "Zgibovi (Pull-ups)", 
            "url": "https://www.youtube.com/embed/eGo4IYONOSQ",
            "upute": "Uhvati šipku, spusti ramena (depresija lopatica) i povuci prsa prema šipci. Puni opseg pokreta."
        },
        {
            "dan": dan_pull, "broj": 2, "naziv": "Veslanje u pretklonu (Barbell Row)", 
            "url": "https://www.youtube.com/embed/G8l_8chR5BE",
            "upute": "Kut leđa oko 45 stupnjeva. Vuci šipku prema pupku i snažno stisni lopatice."
        },
        {
            "dan": dan_pull, "broj": 3, "naziv": "Face Pulls", 
            "url": "https://www.youtube.com/embed/V8d6XjgVWzE",
            "upute": "Vuci konop prema čelu, a pritom rotiraj šake prema van. Odlično za stražnje rame i zdravlje rotatora."
        },
        {
            "dan": dan_pull, "broj": 4, "naziv": "Biceps pregib šipkom", 
            "url": "https://www.youtube.com/embed/in7PcmGcGTI",
            "upute": "Bez ljuljanja! Laktovi uz tijelo, podigni težinu stišćući biceps, spusti polako (naglasak na negativ)."
        },

        # --- NOGE VJEŽBE ---
        {
            "dan": dan_legs, "broj": 1, "naziv": "Čučanj šipkom (Barbell Squat)", 
            "url": "https://www.youtube.com/embed/PQpARQNjwy8",
            "upute": "Stopala u širini ramena, blago prema van. Duboko udahni, spusti se ispod paralele gurajući koljena van."
        },
        {
            "dan": dan_legs, "broj": 2, "naziv": "Rumunjsko mrtvo dizanje (RDL)", 
            "url": "https://www.youtube.com/embed/_Oyx8v7I21E",
            "upute": "Lagano savijena koljena. Guraj kukove unatrag dok ne osjetiš jako istezanje u stražnjoj loži. Leđa ravna!"
        },
        {
            "dan": dan_legs, "broj": 3, "naziv": "Bugarski čučanj (Split Squat)", 
            "url": "https://www.youtube.com/embed/2C-uNgKwPLE",
            "upute": "Stražnja noga na klupi. Kontrolirano spuštanje. Što si nagnutiji naprijed, to više radi gluteus."
        },
        {
            "dan": dan_legs, "broj": 4, "naziv": "Nožni potisak (Leg Press)", 
            "url": "https://www.youtube.com/embed/IZxyjW7cgng",
            "upute": "Stopala nisko i usko za kvadriceps. Spusti težinu duboko, ali ne dopusti da ti se donji dio leđa odvoji od sjedala."
        },
        {
            "dan": dan_legs, "broj": 5, "naziv": "Podizanje na listove", 
            "url": "https://www.youtube.com/embed/-M4-G8p8fmc",
            "upute": "Puna ekstenzija na vrhu, obavezna stanka od 1 sekunde na dnu u maksimalnom istezanju tetive."
        },

        # --- FULL BODY A (Reciklaža za brzi setup) ---
        {"dan": dan_fb1, "broj": 1, "naziv": "Čučanj šipkom", "url": "https://www.youtube.com/embed/PQpARQNjwy8", "upute": "Osnovna vježba za noge."},
        {"dan": dan_fb1, "broj": 2, "naziv": "Bench Press šipkom", "url": "https://www.youtube.com/embed/vcBig73ojpE", "upute": "Osnovna vježba za prsa."},
        {"dan": dan_fb1, "broj": 3, "naziv": "Veslanje u pretklonu", "url": "https://www.youtube.com/embed/G8l_8chR5BE", "upute": "Osnovna vježba za leđa."},
        {"dan": dan_fb1, "broj": 4, "naziv": "Triceps ekstenzija sajlom", "url": "https://www.youtube.com/embed/nRiJVZDpdY0", "upute": "Izolacija za triceps."},

        # --- FULL BODY B ---
        {"dan": dan_fb2, "broj": 1, "naziv": "Konvencionalno Mrtvo dizanje", "url": "https://www.youtube.com/embed/vl5Ljc2vX8E", "upute": "Šipka uz potkoljenicu. Spusti kukove, ispravi leđa. Gurni nogama kroz pod i povuci."},
        {"dan": dan_fb2, "broj": 2, "naziv": "Overhead Press", "url": "https://www.youtube.com/embed/_RlRDWO2jfg", "upute": "Potisak šipkom iznad glave za ramena."},
        {"dan": dan_fb2, "broj": 3, "naziv": "Zgibovi", "url": "https://www.youtube.com/embed/eGo4IYONOSQ", "upute": "Zgibovi za širinu leđa."},
        {"dan": dan_fb2, "broj": 4, "naziv": "Biceps pregib šipkom", "url": "https://www.youtube.com/embed/in7PcmGcGTI", "upute": "Izolacija za biceps."}
    ]

    for v in vjezbe_baza:
        Vjezba.objects.get_or_create(
            dan=v['dan'],
            redni_broj=v['broj'],
            naziv=v['naziv'],
            video_url=v['url'],
            upute=v['upute']
        )

    print("✅ Baza je uspješno napunjena sa 15 stručnih vježbi i 2 programa!")
    print("🔥 Možeš pokrenuti server i testirati aplikaciju.")

if __name__ == '__main__':
    pokreni_punjenje()