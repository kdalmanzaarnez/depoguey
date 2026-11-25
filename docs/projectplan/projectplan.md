# Projectplan PixelDepot WMS

24 november 2026 · Team DepoGuey

## Samenvatting

Wij zijn team DepoGuey: Daniel, Mahi en Kien. We bouwen in acht weken (vier sprints van twee weken) een intern magazijnsysteem voor PixelDepot, een fictieve Nederlandse verkoper van gamingaccessoires voor B2C en B2B.

| Onderdeel | Afspraak |
| --- | --- |
| Project | Warehouse Management System |
| Team | DepoGuey: Daniel, Mahi, Kien |
| Bedrijf | PixelDepot: headsets, controllers, toetsenborden en muizen, één magazijn met vakken zoals A-01 |
| Stack | React + TypeScript + Vite, Chakra UI, Django 5.2 + DRF, MySQL 8.4 via Docker |
| Inleveren | tbc |
| Deadline | tbc |

## Taakverdeling

Ieder van ons heeft een eigen onderdeel met backend en frontend, eigen tests en een eigen stuk documentatie.

| Teamlid | Bouwt | Documentatie |
| --- | --- | --- |
| Daniel | Backend-opzet (Django, DRF, MySQL via Docker), login en rollen, producten, voorraad ontvangen, afboeken en verplaatsen, Settings | Class Diagram, README-opstartstappen |
| Mahi | Navigatie per rol, klantenkaarten en kredietlimiet, dashboardwidgets en meldingen, verkooprapport | Bedrijfsprofiel, marktonderzoek en SWOT, styleguide en Chakra-thema, Use-Case Diagram, Scrum Board |
| Kien | Frontend-opzet (React, Vite, Chakra), orders zoeken, plaatsen, aanpassen, verzenden en annuleren | ERD, documentatie van de voorraadkeuzes |
| Samen | Gelijktijdigheidstest (Kien en Daniel), README-test vanuit een verse checkout (iedereen) | Stand-ups, reviews en retro's |

**Kruisreview:**

- Mahi reviewt Daniels product- en beheerschermen.
- Daniel reviewt Kiens voorraadregels.
- Kien reviewt Mahi's klantrechten, dashboarddata en rapportquery.

We spreken eerst samen het contract tussen producten, orders en klanten af, voordat ieder zijn eigen schermen bouwt.

## User stories

We zetten elke story als issue op ons GitHub Project-bord, met eigenaar, acceptatiecriteria, sprint en gekoppelde PR.

| ID | Als … wil ik … | Eigenaar | Klaar wanneer |
| --- | --- | --- | --- |
| US-01 | Medewerker of admin: inloggen | Daniel | Login en logout werken. `/api/auth/csrf/` zet de CSRF-cookie, `/api/auth/me/` geeft de rol. Bij een foute login verschijnt een algemene melding. |
| US-02 | Gebruiker: een menu dat bij mijn rol past | Mahi | Routes en menu volgen de rol. Een direct bezoek aan een afgeschermd scherm wordt afgevangen. Django controleert de rechten. |
| US-03 | Medewerker: producten doorzoeken | Daniel | Zoeken op naam en SKU, filteren op categorie en status, productdetail met voorraad per vak. |
| US-04 | Admin: producten beheren | Daniel | Aanmaken, aanpassen, deactiveren en verwijderen volgens de historieregel. Een dubbele SKU geeft een duidelijke fout. |
| US-05 | Admin: voorraad ontvangen, afboeken of verplaatsen | Daniel | Ontvangen verhoogt de voorraad op een vak en bewaart de leveringsreferentie. Afboeken vraagt om een reden. Verplaatsen laat het totaal gelijk. |
| US-06 | Medewerker: orders zoeken en openen | Kien | Zoeken op ordernummer of klant, filteren op status, detail met orderregels. |
| US-07 | Medewerker: een order plaatsen met directe reservering | Kien | Meerdere producten per order, één product uit meerdere vakken. Bij een tekort blijft alles ongewijzigd. |
| US-08 | Admin: order en status wijzigen | Kien | Aanpassen verwerkt het verschil in reservering. Verzenden werkt de voorraad één keer bij en volgt de statusregels. |
| US-09 | Admin: order annuleren | Kien | De order blijft zichtbaar. Alleen de eigen reserveringen komen vrij, ook bij een herhaalde annulering. |
| US-10 | Medewerker: klantenkaarten maken en gewone gegevens aanpassen | Mahi | Lijst, detail en formulier werken. De API stuurt geen gevoelige velden naar een medewerker en weigert wijziging ervan. |
| US-11 | Admin: kredietlimiet beheren | Mahi | De admin kan de kredietlimiet zien en wijzigen. Er is een rechtentest voor beide rollen. |
| US-12 | Gebruiker: recente orders op het dashboard | Mahi | Maximaal vijf orders, de nieuwste bovenaan, elk met een werkende link. |
| US-13 | Gebruiker: populairste product met het aantal bestellingen | Mahi, met Kien | Telt het aantal afzonderlijke geldige orders. Geannuleerde orders tellen niet mee. |
| US-14 | Gebruiker: meldingen over orders en producten | Mahi, met Daniel | Nieuwe orders en lage voorraad verschijnen als meldingen met links. |
| US-15 | Admin: top vijf meestverkochte producten | Mahi, met Kien | Endpoint en scherm tonen maximaal vijf producten op stuks uit verzonden orders. Een medewerker krijgt het rapport niet. |
| US-16 | Admin: accounts en rollen beheren | Daniel, review Mahi | Aanmaken, wijzigen, rol aanpassen, verwijderen of deactiveren. De laatste actieve admin blijft altijd bestaan. |
| US-17 | Beoordelaar: het project zelf kunnen starten | Iedereen | Een verse checkout start via de README met `docker compose up`. Demoaccounts en demodata zijn reproduceerbaar. |
| US-18 | Team: bewijzen dat gelijktijdige orders geen voorraad dubbel uitgeven | Kien en Daniel | Twee MySQL-verbindingen vragen tegelijk het laatste stuk. Eén slaagt, de ander krijgt 409, en er blijft niets half achter. |

## Weekplanning

We werken in sprints van twee weken en sluiten elke sprint af met een demo en een retrospective. De laatste kolom zegt wat er aan het einde van de week echt te zien moet zijn.

| Week | Daniel | Mahi | Kien | Te zien aan het einde |
| --- | --- | --- | --- | --- |
| 1 · Opzet (sprint 1) | GitHub-repo. Django, DRF en MySQL via Docker. `.env.example`, eerste migrate. | Bedrijfsprofiel, doelgroepen, concurrenten, SWOT, wireframe dashboard. Scrum Board. | React, TypeScript, Vite en Chakra, met Vite-proxy naar Django. Eerste ERD en statusregels. | Alle drie draaien de basis lokaal met migraties op MySQL. Besluit over rollen, voorraad en deadline. Elke story heeft een eigenaar. |
| 2 · Login en ontwerp (sprint 1) | Login, logout, CSRF, sessies, rol opvragen, twee demogebruikers. Modellen product, locatie en voorraad. Class Diagram. | Chakra-thema, navigatie, routes per rol, styleguide, Use-Case Diagram. Klantmodel. | Orderregels en toewijzingen ontwerpen. Modellen en API-contract afstemmen. Loginpagina in React met Daniel. | **Demo:** twee logins en een geweigerde adminactie. Eerste versie van alle drie de diagrammen staat in GitHub. |
| 3 · Producten en klanten (sprint 2) | **Dag 1: modellen gemerged.** Daarna demodata en productlijst met zoeken, filters en detail. | **Dag 1: klantmodel gemerged.** Daarna klantenkaarten en formulieren. Dashboardlayout. | Ordermigraties op de gemergde modellen. Orderlijst en orderdetail. Orderformulier voorbereiden. | Beide rollen zien producten, klanten en orders. De data sluit aan op het orderformulier. |
| 4 · Eerste order (sprint 2) | Productbeheer. Voorraad ontvangen, afboeken, verplaatsen. Voorraadconstraints testen met Kien. | Klantrechten afronden. Recente orders koppelen aan het orderdetail. | Order aanmaken, reserveren per vak, foutafhandeling bij te weinig voorraad. | **Demo:** order via React, te openen vanaf het dashboard. Voorraad daalt. Een te grote order verandert niets. Een ontvangst verhoogt de voorraad. |
| 5 · Verwerking (sprint 3) | Settings voor accounts en rollen. Deactiveren, en de laatste actieve admin beschermen. | Populairste product en meldingen. API voor het verkooprapport. | Order aanpassen, status wijzigen, verzenden en annuleren. | Admin past één order aan, verzendt een tweede en annuleert een derde. De voorraad klopt na elk scenario. |
| 6 · Basisversie af (sprint 3) | Settings en productbeheer afronden. Rechtentests van de API. Class Diagram bijwerken. | Rapportscherm (max. vijf). Klantrechten, navigatie, toetsenbord en mobiel testen. | Tests orderservices. Lege en fouttoestanden. ERD bijwerken. Opstartproces controleren met Daniel. | **Demo:** alle verplichte functies werken met echte data voor beide rollen. Openstaande problemen staan op het bord. |
| 7 · Kwaliteit (sprint 4) | Voorraad- en rolbeheer testen. Gelijktijdigheidstest (US-18) met Kien. README-opstartstappen. | Volledige scenario's doorlopen. Bedrijf, onderzoek en design afronden. Styleguide en Use-Case Diagram bijwerken. | Gelijktijdigheidstest (US-18) met Daniel. Rollback testen. Voorraadkeuzes documenteren. | Een verse checkout start via de README. Alle inlevereisen afgevinkt. |
| 8 · Inleveren (sprint 4) | Video: login, rechten, product en voorraad. Repositorylink controleren. | Video: klanten, dashboard, rapport, design. Scrum-verslagen bijwerken. | Video: orders en voorraad. Demodata klaarzetten voor de opnames. | **Eindreview.** Iedereen levert een eigen video in op Canvas. |

## Techniek

Onze backend draait op Django met MySQL 8.4 in Docker.

| Onderdeel | Keuze |
| --- | --- |
| Frontend | React + TypeScript + Vite, React Router |
| UI | Chakra UI met één gedeeld thema |
| Backend | Python 3.13, Django 5.2 LTS + Django REST Framework |
| Database | MySQL 8.4 LTS (InnoDB) via Docker |
| Login | Django-sessie + CSRF |
| Samenwerking | GitHub: Issues, Projects, pull requests |
| Ontwerp | Figma + Mermaid of diagrams.net |
| Versies | Node 24 LTS, Python 3.13, MySQL 8.4 |

**Database opzetten:**

1. We zetten een `docker-compose.yml` in de repo met `mysql:8.4`, database `pixeldepot_wms`, tekenset `utf8mb4`, een aparte applicatiegebruiker, poort `3307:3306` en een named volume.
2. Op macOS: `brew install pkg-config mysql-client`, anders mislukt `pip install mysqlclient`.
3. We zetten `mysqlclient` in `backend/requirements.txt`. Django leest de databasegegevens uit omgevingsvariabelen, en de namen zetten we in `.env.example`, zonder echte wachtwoorden.
4. We starten met `docker compose up -d` en draaien daarna `python manage.py migrate`.
5. We testen de hele keten: we voegen één headset toe en lezen hem terug via de API.

**Mappen in de repo:** `frontend/`, `backend/`, `docs/design/` (bedrijf, marktonderzoek, styleguide), `docs/design/diagrammen/`, `docs/scrum/`, plus `docker-compose.yml`, `.env.example` en `README.md`.

## Datamodel en voorraadregels

Elke voorraadrij hoort bij één product op één vak, met een fysiek aantal (`on_hand`) en een gereserveerd aantal (`reserved`). Beschikbaar is fysiek min gereserveerd.

### Entiteiten

| Entiteit | Belangrijkste velden en relaties |
| --- | --- |
| User | Gebruikersnaam, actiefvlag, rol via twee Django-groepen (Medewerker, Admin) |
| Customer | Type (consument of zakelijk), naam, e-mail, telefoon, adres, afgeschermde kredietlimiet. Heeft meerdere orders |
| Product | Unieke SKU, naam, categorie, beschrijving, compatibiliteit, prijs, actiefvlag, minimumvoorraad |
| Location | Unieke vakcode, omschrijving |
| Stock | Product + locatie (uniek), `on_hand`, `reserved` |
| Order | Ordernummer, klant, medewerker, status, tijdstempels |
| OrderLine | Order, product, aantal, verkoopprijs op het moment van bestellen |
| StockAllocation | Orderregel, voorraadrij, toegewezen aantal: welk vak levert hoeveel |
| StockMovement | Type (`receive`, `write_off`, `transfer`), product, vak(ken), aantal, reden of leveringsreferentie, uitvoerder, tijdstip |

### Wat Django doet per actie

| Actie | Wat er gebeurt |
| --- | --- |
| Order aanmaken | Order, regels en reserveringen in één transactie. Reserveren per vak, op volgorde van vakcode. Is er van één product te weinig, dan wordt de hele order geweigerd. |
| Order aanpassen | Alleen bij Nieuw of In verwerking. Reserveert het verschil erbij of geeft het vrij. Wordt alleen opgeslagen als alle regels haalbaar zijn. |
| Order annuleren | Geeft precies de eigen reserveringen vrij, op de oorspronkelijke vakken. Een tweede annulering verandert niets. |
| Order verzenden | Verlaagt fysiek én gereserveerd. Beschikbaar blijft gelijk. |
| Ontvangen | Verhoogt de fysieke voorraad op één vak en maakt de rij aan als die nog niet bestaat. Bewaart de leveringsreferentie. Een inactief product kan niets ontvangen. |
| Afboeken | Verlaagt de fysieke voorraad op één vak, met hoogstens het beschikbare aantal. Een reden is verplicht. |
| Verplaatsen | Van bronvak naar doelvak in één transactie. Alleen beschikbare stuks. Het totaal blijft gelijk. |

### Rekenvoorbeeld: headset op vak A-01

| Moment | Fysiek | Gereserveerd | Beschikbaar |
| --- | --- | --- | --- |
| Start | 10 | 0 | 10 |
| Order van 3 stuks geplaatst | 10 | 3 | 7 |
| Daarna geannuleerd | 10 | 0 | 10 |
| Of daarna verzonden | 7 | 0 | 7 |
| Na verzending 5 stuks ontvangen | 12 | 0 | 12 |

### Orderstatussen

Een order gaat van **Nieuw** naar **In verwerking** naar **Verzonden**. Annuleren kan vanuit Nieuw of In verwerking. Verzonden en Geannuleerd zijn eindstatussen. Alleen een admin wijzigt de status, en orders worden nooit verwijderd.

### Technische regels

- Alle mutaties lopen via Django-services (`OrderService`, `StockService`) binnen `transaction.atomic()`.
- We vergrendelen eerst de orderrij, dan de voorraadrijen met `select_for_update()`, in een vaste volgorde en op primaire sleutel.
- We dwingen `0 ≤ reserved ≤ on_hand` af, en de unieke combinatie van product en locatie.
- We slaan geld op als decimaal veld. Bestaande orders houden hun opgeslagen prijs.
- Eén orderregel per product, één toewijzing per orderregel en vak.

### Verwijderen

- **Product:** zonder voorraad en historie mag het weg. Met historie wordt het gedeactiveerd, en het blijft zichtbaar via het statusfilter en in oude orders.
- **Order:** nooit verwijderen. Annuleren is de administratieve handeling.
- **Account:** een ongebruikt account mag weg. Met historie wordt het gedeactiveerd. De laatste actieve admin blijft altijd bestaan.

## Rechten en schermen

Wat een medewerker niet mag, weigert Django ook bij een direct API-verzoek. Het menu toont alleen de pagina's waar iemand recht op heeft.

| Handeling | Medewerker | Admin |
| --- | --- | --- |
| Inloggen, dashboard en meldingen | Ja | Ja |
| Producten zoeken en details bekijken | Ja | Ja |
| Producten aanmaken, aanpassen, deactiveren, verwijderen | Nee | Ja |
| Voorraad ontvangen, afboeken, verplaatsen | Nee | Ja |
| Orders zoeken, bekijken en aanmaken | Ja | Ja |
| Orders aanpassen, status wijzigen, annuleren | Nee | Ja |
| Klantenkaarten bekijken, maken, contactgegevens wijzigen | Ja | Ja |
| Kredietlimiet en gevoelige klantvelden | Nee | Ja |
| Verkooprapport | Nee | Ja |
| Gebruikers en rollen beheren | Nee | Ja |

| Scherm | Wat erop staat |
| --- | --- |
| Login | Gebruikersnaam en wachtwoord, een algemene foutmelding, doorsturen na de login, uitloggen. |
| Dashboard | Menu, de vijf recentste orders met links, het populairste product met het aantal orders, meldingen over nieuwe orders en lage voorraad. |
| Products | Tabel met naam, SKU, categorie, beschikbaar en status. Zoeken en filteren. Detail met prijs, compatibiliteit en voorraad per vak. Admin: beheer, ontvangen, afboeken, verplaatsen. |
| Orders | Tabel met nummer, klant, datum en status. Zoeken en filteren. Detail met regels, prijzen en vakken. Formulier voor een nieuwe order. Admin: aanpassen, status, annuleren. |
| Customers | Doorzoekbare klantenkaarten, consument of zakelijk, contactgegevens, formulier. Admin ziet ook de kredietlimiet. |
| Reports | Alleen admin. Top vijf op verkochte stuks uit verzonden orders: naam, SKU, aantal. |
| Settings | Alleen admin. Accounts toevoegen, wijzigen, deactiveren of verwijderen, en rollen wijzigen. |

**Hoe we de cijfers tellen.** De widget Populairste product telt het aantal niet-geannuleerde orders waarin het product voorkomt. Het rapport telt stuks uit verzonden orders. Voorbeeld: een product zit in twee orders, van 3 en van 1 stuk. De widget toont dan 2 bestellingen, en het rapport toont 4 stuks zodra beide orders verzonden zijn. Bij een gelijke uitkomst sorteren we op SKU.

## Styleguide

We kiezen een rustige, zakelijke stijl met donkerblauw als hoofdkleur, zodat magazijngegevens goed leesbaar blijven.

| Keuze | Waarde | Waarom |
| --- | --- | --- |
| Primaire kleur | Donkerblauw `#1E3A5F` | Navigatie, hoofdknoppen en een duidelijke hiërarchie |
| Secundaire kleur | Blauw `#2563EB` | Links, zichtbare focus, selectie en accenten |
| Achtergrond en kaarten | `#F4F6FA` en `#FFFFFF` | Scheidt het werkvlak van kaarten en tabellen |
| Tekst | `#172033` en `#475569` | Hoofdtekst en bijzaken zijn duidelijk te onderscheiden |
| Status Verzonden | Groen `#166534` | Herkenbaar signaal, altijd met tekstlabel |
| Status In verwerking | Amber `#92400E` | Herkenbaar signaal, altijd met tekstlabel |
| Status Geannuleerd | Rood `#B91C1C` | Herkenbaar signaal, altijd met tekstlabel |
| Lettertype interface | Inter | Goed leesbaar in tabellen en formulieren |
| Lettertype codes | IBM Plex Mono | SKU's en vakcodes zoals A-01 zijn snel te scannen |
| Componenten | Tabel, filters, statusbadge, formulier, bevestigingsdialoog, fout- en succesmelding | Dezelfde handelingen werken overal hetzelfde |

We maken wireframes van login, dashboard, productlijst en -detail, orderlijst en order aanmaken, klantenkaart, rapporten en instellingen, met één medewerker- en één adminweergave. We controleren toetsenbordbediening, zichtbare focus, labels bij formuliervelden en het kleurcontrast.

## API-afspraken

We leggen deze endpoints in week 1 en 2 vast, met één conventie voor veldnamen, zodat ieder los zijn eigen schermen kan bouwen.

| Gebied | Endpoints |
| --- | --- |
| Auth | `GET /api/auth/csrf/`, `POST /api/auth/login/`, `GET /api/auth/me/`, `POST /api/auth/logout/` |
| Products | `GET /api/products/?search=&active=`, `GET /api/products/{id}/` |
| Stock | `POST /api/stock/receive/`, `POST /api/stock/write-off/`, `POST /api/stock/transfer/` |
| Orders | `GET /api/orders/?status=`, `POST /api/orders/`, `PATCH /api/orders/{id}/`, acties voor status wijzigen en annuleren |
| Customers | `GET /api/customers/`, `POST /api/customers/`, `PATCH /api/customers/{id}/`, velden per rol |
| Dashboard | `GET /api/dashboard/` |
| Reports | `GET /api/reports/top-products/` |
| Settings | `/api/settings/users/` |

| Foutcode | Wanneer |
| --- | --- |
| 400 | Ongeldige invoer |
| 403 | Ingelogd, maar geen rechten |
| 409 | Voorraadconflict |

Django bepaalt de prijs, de rol en de geldige statusovergangen. React toont alleen de uitkomst. Elke schrijfactie stuurt een CSRF-token mee.

## Verificatietests

Met deze tests bewijzen we dat de rechten en de voorraadregels kloppen. Elke test hoort bij een story en draait voordat die story op Done gaat.

| Situatie | Verwacht | Story |
| --- | --- | --- |
| Medewerker vraagt het rapport of gebruikersbeheer direct op via de API | Geweigerd | US-15, US-16 |
| Medewerker stuurt een kredietlimiet mee | Geweigerd, het bedrag blijft gelijk en staat niet in de respons | US-10, US-11 |
| Order met twee producten, één daarvan heeft te weinig voorraad | Geen order en geen reservering | US-07 |
| Twee verbindingen vragen tegelijk het laatste stuk | Eén slaagt, de ander krijgt 409, er blijft niets half achter | US-18 |
| Order van 3 stuks wordt 5, en wordt daarna geannuleerd | Eerst 2 extra gereserveerd, daarna alle 5 vrijgegeven, precies één keer | US-08, US-09 |
| Een product komt uit twee vakken | Aantallen per vak bewaard, annuleren herstelt de juiste vakken | US-07, US-09 |
| Admin ontvangt 5 stuks op een nieuw vak, verplaatst er 2, boekt er 1 af | Totaal +5, dan gelijk, dan −1. Drie StockMovements | US-05 |
| Een product met historie wordt gedeactiveerd | Oude orders blijven kloppen. Het product kan niet meer besteld of ontvangen worden | US-04 |
| Zes producten met verzonden orders, plus een geannuleerde order | Rapport toont er hoogstens vijf, zonder de geannuleerde order | US-15 |
| Een nieuw teamlid volgt de README | Docker, frontend en backend starten, migraties lopen, beide demologins werken | US-17 |

## Opleveren

We leveren de code en documentatie in via één GitHub-repository. Ieder van ons levert daarnaast een eigen video in op Canvas.

| Onderdeel | Wat erin moet | Plek | Eigenaar |
| --- | --- | --- | --- |
| Code | Frontend, backend, migraties, Docker, `.env.example`, demodata | `frontend/`, `backend/` | Iedereen |
| Bedrijfsinformatie | Profiel, assortiment, klanten, magazijnproces, het probleem dat het WMS oplost | `docs/design/bedrijf.md` | Mahi |
| Marktonderzoek | Eén à twee pagina's: doelgroep, Coolblue en Alternate vergeleken, verkoopkanalen, bronnen met raadpleegdatum, SWOT | `docs/design/marktonderzoek.md` | Mahi |
| Styleguide en wireframes | Kleuren met codes, fonts, keuzes met reden, ontwerplink | `docs/design/styleguide.md` | Mahi |
| ERD | Entiteiten, sleutels, cardinaliteiten, unieke combinaties | `docs/design/diagrammen/` | Kien, met Daniel |
| Class Diagram | Modelklassen, `OrderService`, `StockService` en hun relaties | `docs/design/diagrammen/` | Daniel, review Kien |
| Use-Case Diagram | Medewerker en Admin buiten de systeemgrens, met hun acties | `docs/design/diagrammen/` | Mahi, review Daniel |
| Scrum | Bord, planning, taakverdeling, stand-ups, reviews, retro's | GitHub Projects, `docs/scrum/` | Iedereen |
| README | Doel, stack, opstarten, demodata, rollen, tests, team | `README.md` | Daniel, test door iedereen |

### Video per persoon (5 tot 10 minuten)

| Tijd | Inhoud |
| --- | --- |
| 0:00 | Jezelf, PixelDepot en jouw rol in team DepoGuey |
| 0:45 | Het dashboard en een korte route door de app |
| 2:00 | Jouw eigen functie, plus één fout- of rechtencontrole |
| 4:30 | Jouw code: waar de handeling begint en waar Django de regels uitvoert. Een test of PR |
| 6:00 | Jouw design, documentatie of diagram, en hoe we hebben samengewerkt |
| 7:15 | Eén technische uitdaging en hoe we die hebben opgelost |

We controleren voor het inleveren dat de beoordelaar de repository kan openen en dat de README uitlegt hoe de demodata geladen wordt.

## Werkwijze

We werken met Scrum op een GitHub Project-bord en mergen alleen gereviewde pull requests.

**Scrum**

- **Bord:** Backlog → Ready → In progress → Review → Done. Elke issue heeft een eigenaar, acceptatiecriteria, een sprint en een gekoppelde PR.
- **Stand-up:** bij elk werkmoment bespreken we wat af is, wat het volgende is en wat blokkeert. We noteren datum, aanwezigen, blocker en actiehouder in `docs/scrum/`.
- **Sprintreview:** we demonstreren de afgeronde stories met demodata en zetten feedback om in issues.
- **Retrospective:** we noteren wat goed ging, wat stroef liep en één actie met een eigenaar voor de volgende sprint.

**Git en code**

- Eén branch per issue, bijvoorbeeld `feature/us-07-order-create`.
- Kleine commits met een duidelijke beschrijving, regelmatig en vanaf ons eigen account. Dat telt mee in de beoordeling.
- Elke PR wordt gereviewd door een ander teamlid en getest voor de merge.
- Bedrijfsregels staan in Django-services. React-componenten doen alleen de interface.
- Duidelijke namen, zoals `availableQuantity` in TypeScript en `reserved_quantity` in Python.
- Comments leggen uit waarom iets zo gebouwd is. Terugkerende validatie hergebruiken we (DRY).

**Definition of Done:** de feature werkt vanuit het gewone scherm, beide rollen zijn getest, de randgevallen zijn afgehandeld, de PR is gereviewd en de documentatie is bijgewerkt.

## Extra, als de basis af is

We beginnen pas aan uitbreidingen als de basisversie aantoonbaar werkt. De picklijst is onze eerste keuze.

| Uitbreiding | Wat het doet | Werk |
| --- | --- | --- |
| Picklijst per order | Producten per vak gegroepeerd, met SKU en aantal, eventueel met afdrukweergave | Klein |
| CSV-export van het rapport | Dezelfde top vijf als bestand | Klein |
| Voorraadgeschiedenis per product | De StockMovements per product, met datum, wie en waarom | Klein |
| Zoeken met barcode | Een USB-scanner werkt als toetsenbord om een product of vak te vinden | Middel |
| Meldingen als gelezen markeren | Per medewerker bijhouden welke meldingen gezien zijn | Middel |
| Retouren | Een retour koppelen aan een verzonden order en terugboeken op een vak | Middel tot groot |
