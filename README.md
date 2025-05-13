# Estudiju "Gaidāmie notikumi" pievienošana apple kalendāram(iCalendar)
Python webscraping automatizācija izmantojot selenium bibliotēku, lai pārvērstu iegūto informāciju par gaidāmajiem darbu iesniegšanas termiņiem icould .ics kalendāra formā.
## Projekta uzdevums
  Šajā python projektā tiek izmantota selenium bibliotēka, ar kuras palīdzību caur Google Chrome pārlūkprogrammu tiek veikta pieslēgšanās estudijas.rtu.lv sistēmā.
  
  Pēc pieslēgšanās programma atrod sadaļu "Gaidāmie notikumi" un secīgi pēc kārtas izvēlas katru šīs sadaļas elementu, uz kura tiek uzklikšķināts ar metodi `.click()`, kā rezultātā atveras jauns logs, kurā atrodas programmai nepieciešamie dati(Notikuma nosaukums; datums un laiks; moduļa/priekšmeta nosaukums; saite uz notikumu). Ar cikla palīdzību katra sadaļas elementa logs tiek atvērts, dati tiek nolasīti un logs aizvērts.
  
  Kad dati nolasīti, tiek pārveidots datums un laiks, jo sākotnēji iegūtie dati sastāv no datuma, kurā mēneša nosaukums dots nevis ar cipariem, bet gan ar mēneša vārdu latviešu valodā, piemēram, `Piektdiena, 8. maijs, 16:30`. Izmantojot vārdnīcu, kurā katram mēneša nosaukumam tiek piešķirta divu ciparu vērtība šo datumu un laiku pārveido formātā `GGGG-MM-DD HH:MM`, un atbrīvojas no nedēļas dienas nosaukuma, jo tas mums nav nepieciešams.

  Tālāk visa derīgā informācija tiek saglabāta sarakstā, kas sastāv no vārdnīcām: 
```
"Title": event_title,
"Course": course_name,
"due": date,
"link": link_href
```
Lai pievienotu sarakstā saglabāto notikumu informāciju icloud kalendāram un varētu strādāt ar .ics failu formātu(iCalendar), nepieciešams no `ics` bibliotēkas importēt klases `Calendar` un `Event`.

No saraksta ar vārdnīcām, informācija ar cikla palīdzību tiek piešķirta `ics` bibliotēkas `Event` klases objektiem, pēc kā tā tiek ierakstīta `.ics` failā un atverot šo failu lietotājs ērti pievieno visus _Gaidāmos notikumus_ savam apple kalendāram.

## Izmantoto biblioteku lietojums
Projekta izstrādē lietoju bibliotēku `selenium`, jo šīs bibliotēkas sniegtās iespējas ļauj man automatizēt ielogošanos savā rtu e-studiju vides profilā, datu nolasīšanu, pogu klikšķināšanu, teksta ievadi, u.c., taču konkrētāk par no selenium bibliotēkas izmantotajām klasēm rakstīšu zemāk:

`Webdriver` klase no `selenium` bibliotēkas importē WebDriver API(Aplication Programming Interface), kas atļauj pārlūkprogrammas(šajā gadījumā Google Chrome) automatizāciju.

`Keys` klase no `selenium.webdriver` nepieciešama, lai varētu simulēt, piemēram, taustiņa _enter_ nospiešanu.

`Service` klase no `selenium` bibliotēkas nepieciešama, lai varētu konfigurēt tieši kā pārlūkprogramma sāks darbu.

Klase `By` nepieciešama html elementu meklēšanai tīmekļa lapā. Tā palīdz atrast elementu pēc kādas konkrētas klases nosaukuma, vai identifikatora(`By.ID`, `By.CLASS_NAME`, utt.)

`WebDriverWait` un `EC(Expected Conditions)` klases nepieciešamas, lai programma gaidītu, līdz izpildas konkrēti nosacījumi, lai tā turpinātu darbu.

Bibliotēka `time` nepieciešama, lai iepauzētu programmas izpildi ar komandu `.sleep()` brīdī, kad tīmekļa lapa ielādē vajadzīgo saturu.

Bibliotēka `ics` un tās klases `Calendar` un `Event` nepieciešamas, lai varētu saglabāt _"noskrāpēto"_ informāciju icloud kalendāram nepieciešamajā formātā.

`Datetime` bibliotēku izmantoju, lai formatētu iegūto datumu un laiku uz nepieciešamo ISO formātu iCalendar `.ics` faila tipam.

Un `getpass` bibliotēku lietoju, lai pie estudiju paroles ievades konsolē tā nebūtu redzama.
