## 🚀 Kom i gang

### 1. Klon repoet

### 2. Sett opp miljøvariabler

For å kunne bruke Azure-tjenestene må vi legge til API-nøkler og endepunkter i en `.env`-fil. Dette bidrar til å holde sensitiv informasjon sikker.

_Slik gjør du:_

1. **Naviger til Backend-mappen**

Åpne en terminal og naviger til intro-oppgaver-mappen, deretter backend-mappen:

```bash
cd intro-oppgaver/backend
```

2. Opprett en `.env`-fil i rooten på backend-prosjektet.

3. Klikk på lenken under og kopier alt.
   - TODO
4. Lim inn i `.env`-filen

### 3. Kjør prosjektet

For å kjøre prosjektet anbefales det å bruke to separate terminaler: én for frontend og én for backend.

### Backend

Følg disse trinnene for å sette opp og kjøre backend:

1. **Naviger til Backend-mappen**  
   Åpne en terminal og naviger til intro-oppgaver-mappen, deretter backend-mappen:
   ```bash
   cd intro-oppgaver/backend
   ```
2. **Opprett et virtuelt miljø**
   ```bash
   python3 -m venv .spotify-env
   ```
3. **Aktiver et virtuelt miljø**
   ```bash
   (Mac/linux) source .spotify-env/bin/activate
   (Windows) .spotify-env\Scripts\activate
   ```
4. **Installer nødvendige Python-pakker**
   ```bash
   pip3 install -r requirements.txt
   ```
5. **Kjør Flask server**

   ```bash
   flask run

   ```

*🚨 Første gang prosjektet kjøres, vil kommandoen "flask run" gi en feilmelding. Dette skyldes at det gjenstår noen oppgaver som må fullføres for at den skal fungere som forventet🚨*

### Frontend

Følg disse trinnene for å sette opp og kjøre frontend:

1. **Naviger til Frontend-mappen**
  Åpne en terminal og naviger til `frontend`-mappen:

   ```bash
   cd intro-oppgaver/frontend

   ```

2. **Installer avhengigheter**
   ```bash
   npm install
   ```
3. Run dev server
   ```bash
   npm run dev
   ```

## Oppgave 1 – Spotify API 🔍

_I oppgave 1 skal vi benytte oss av Spotify sitt API for å hente spillelistene dine fra Spotify. Deretter skal vi benytte oss av Azure sin modell for generering av et spilleliste-cover basert på sangene i spillelisten din._
_ For å få til dette skal vi sette opp .env-fil, backend-route, og koble dette til frontend._

---

### 1.1 Opprett en route i Frontend for å vise hjemsiden

_Den ferdiglagde komponenten PlaylistPage viser en side i frontenden der brukerne kan se alle spillelistene sine. Vi skal nå sette opp en route som viser denne som hjemmesiden_

**Oppgave**

1. Naviger til `App.tsx`, som ligger i `src`-mappen.
2. Legg til en ny route med en tom path ("/") slik at PlaylistPage blir hovedsiden.
3. Husk å importere PlaylistPage.

Når du har fullført oppgaven, skal **ImageUploadPage** vises på skjermen.

### 1.2 Legg til knapp

_PlaylistCard-komponenten er hvert kort som viser alle spillelistene til brukeren, her ønsker vi å legge til en knapp som lar brukeren komme til en ny side, med mer info om spillelisten sin, og mulighet genere coverbilde eller beskrivelse av spillelisten sin._

**Oppgave**

1. Naviger til `components/PlaylistCard/PlaylistCard.tsx`
2. Importer `Link` fra `react-router-dom`
3. Legg til en `<Link>` komponent som navigerer til `/cover/${playlist.id}`
   - Inne i Link-komponenten, legg til en `<button>` med teksten "Info"

_Hint: Link-komponenten bruker `to`-attributtet for å spesifisere hvor den skal navigere. Bruk template literals (backticks) for å inkludere playlist.id i path._

Når oppgaven er fullført, skal man kunne trykke inn på hver spilleliste, og få listet opp sanger i spillelisten. 

### 1.3 Endre bakgrunnsfarge

1. Naviger til ` cd styles/index.css `
2. Bakgrunnen er nå hvit – bytt den til din favorittfarge!


### 1.4 Lag en knapp for å generere coverbilde

_På GeneratorPage-siden vises alle sangene i spillelisten. Nå skal vi legge til en knapp som lar brukeren generere et AI-basert coverbilde for spillelisten._

**Oppgave**

1. Naviger til `pages/GeneratorPage/GeneratorPage.tsx`
2. Finn kommentaren `{/* TODO: 1.4 */}` 
3. Erstatt kommentaren med en `<button>` som har følgende:
   - `onClick` skal kalle funksjonen `generateCover`
   - `disabled` skal være `true` når `generating` er `true` eller `tracks.length === 0`
   - `className` skal være `{styles.generateButton}`
   - Knappeteksten skal vise "Generating..." når `generating` er `true`, ellers "Generate AI Cover Image"

_Hint: Bruk en ternary operator (betingelse ? true : false) for å vise forskjellig tekst basert på `generating`-tilstanden._

_Hint2: Du kan se et lignende eksempel ved den andre knappen som genererer en beskrivelse av spillelisten. _

OBS: Denne knappen fungerer først fullføringen av neste oppgave.

## Oppgave 2 – INNHOLDSGENERERING  🧠

_I oppgave 2 skal bildet genereres basert på sangene i spillelisten._

---


### 2.1 BILDEGENERERING 🖼️ 

Klassen `CoverImageGeneratorClient` er laget for å samhandle med OpenAI’s DALL-E 3-modell gjennom Azure OpenAI-tjenester, og brukes til å generere bilder basert på tekstbeskrivelser (kalt "prompt").

**Oppgave**

1. Naviger til `cover_image_generator_client.py` i backend.

2. Sett modellen til **"dall-e-3"**.

3. Endre størrelsen på bilde til å være **1024x1024**.
4. 

Når du har fullført oppgaven, skal det være mulig å klikke på knappen fra forrige oppgave og generere et AI-coverbilde basert på sangene i spillelisten.

### 2.2 TEKSTGENERERING 💬

Klassen LangueModelClient bruker OpenAI sin GPT-4-modell via Azure for å generere tekst basert på en prompt.
**Oppgave**

1. Naviger til `llm_client` i backend.

2. Sett modellen til **"gpt-4o-mini"**.


### 2.3 Forbedre Prompten 💡

_En godt formulert prompt er avgjørende for å generere relevante og presise resultater._

#### Oppgave

1. Gå gjennom eksisterende tekst i prompten i `recipe_generator.py`.

2. Sørg for at prompten er klar, spesifikk og inkluderer all nødvendig kontekst for å generere en oppskrift av høy
   kvalitet.



