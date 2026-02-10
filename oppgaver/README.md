## 🚀 Kom i gang

### 1. Klon repoet

### 2. Sett opp miljøvariabler

For å kunne bruke Azure-tjenestene må vi legge til API-nøkler og endepunkter i en `.env`-fil. Dette bidrar til å holde sensitiv informasjon sikker.

_Slik gjør du:_

1. **Naviger til Backend-mappen**

Åpne en terminal og naviger til oppgaver-mappen, deretter backend-mappen:

```bash
cd oppgaver/backend
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
   Åpne en terminal og naviger til oppgaver-mappen, deretter backend-mappen:
   ```bash
   cd oppgaver/backend
   ```
2. **Opprett et virtuelt miljø**
   ```bash
   python3 -m venv .venv
   ```
3. **Aktiver et virtuelt miljø**
   ```bash
   (Mac/linux) source .venv/bin/activate
   (Windows) .venv\Scripts\activate
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
   cd oppgaver/frontend

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
### 1.0 Legg til riktig token fra Spotify

_For å få tilgang til dine Spotify-spillelister, trenger vi riktig token._


**Oppgave**

1. Gå til https://developer.spotify.com/
2. Logg inn og scroll ned til **Code**
3. Kopier token fra kodeeksemplet – dette er din token for å få tilgang til Spotify API'et
4. Naviger til `.env`-filen og lim inn token fra Spotify for `SPOTIFY_ACCESS_TOKEN`

**Eksempel:**

Fra https://developer.spotify.com/:
```javascript
const token = 'eksempel_token123'
```
I .env filen:
```
SPOTIFY_ACCESS_TOKEN='eksempel_token123'
```


_OBS: Token varer kun én time, når du går ut vil du få en feilmelding. Når dette skjer må du laste laste inn siden på nytt, og oppdatere .env filen med den nye token._ 

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


### 1.3 Backend-route for å sende spilleliste til bilde genereringsmodellen.

_Når en `GET`-forespørsel sendes til `/generate-cover`, skal spillelisten som blir sendt med forespårslen behandlet av Azure modellen for å genere et coverbilde basert på sangtitlene. Forespørslen skal inneholde en spilleliste id og en bruker id, og endepunktet skal returnere bildet som er generert. 

**Oppgave**

1. Naviger til services/routes.py i backend
2. Oppdater endepunktet i routes.py for å motta bildet:
   - Metode: `GET`-forespørsel
   - URL:`/generate-cover`
3. Finn ut hvilket klasse og metode som små brukes for å kalle Azure modellen
4. Returner 
5. Erstatt `return "todo", 200` med en JSON-respons som returnerer `blob_image_url`

   _Tips: Du kan finne lignende struktur i en annen methode i filen._



Når oppgaven er fullført, skal det være mulig å kjøre kommandoen `flask run` i backend-terminalen uten at det gir feilmelding. Husk å kjøre kommandoen i `cd oppgaver/backend`

### 1.4 Legg til knapp for generering av spillelistecover

_I denne oppgaven skal du gj.  Komponenten er designet for at brukeren skal kunne se det genererte bildet som er laget av modellen._

**Oppgave**

1. ** Oprett genererings knapp**:
   - Oprett en knapp med onClick og tekst "Generate AI Cover Image"
   - OnClick eventet skal vise til generateCover
   - Tilordne den CSS-klassen className={styles.generateButton}.

2. **Variere tekst for å se om bildet holder på å genereres**
   - For å variere tekst som vises på knappen kan vi benytte oss av 'Conditional Rendering', ved hjelp av useState 'generating' i filen. 
   - Gjør dette for knappen med teksten "Generate AI Cover Image" og "Generating..."
   - For eksempel:

```javascript
const [example, setExample] = useState(false);

{example ? "Example is true" : "Example is false"}
```

3. **Lag et API kall**
   - Oppdater responsen med et kall vd bruk av 'await.axios.get', hvor vi skal kalle på "api/get-tracks", og hvor vi sender inn playlist_id som argument. 
   - Oppdater setTracks state med responsen sin data. 


Når alt fungerer, skal du kunne genere et bilde ved hjelp av knappen. 

## Oppgave 2 – Last opp bilder til bildebibliotek

For å se alle bildene vi har laget ved hjelp av modellen vår, vil vi lagre de i Azure Blob Storage, og vise dem frem i et bibliotek. Vi trenger derfor å først laste bildet opp til Azure Blob Storage, og deretter vise bildene frem ved å laste de ned fra Azure Blob Storage. 

---

**Oppgave**
1. Naviger til BlobStorageClient.
2. Oppdater blob_client ved å bruke blob_service_client og metoden get_blob_client. 
   - Tips: Husk å ha med containernavn og blob navn.
   - Tips2: https://learn.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob.blobserviceclient?view=azure-python#azure-storage-blob-blobserviceclient-get-blob-client
3. Last opp bildet til blob_client ved å bruke upload_blob. 
   - Husk å sende med bildedata, content_settings, og blob_type="BlockBlob". 
4. Det er url'en til bildet som brukes i routern, sett url'en. 

## Oppgave 3 - Vis frem bildene
1. Naviger til BlobStorageClient.
2. Oppdater blob_list ved hjelp av container_client og list_blobs
3. Oppdater blob_client ved å bruke blob_service_client og metoden get_blob_client. 
4. Vi trenger id, playlistId, imageUrl, createdAt, ved å benytte seg av playlist_id eller hjelp av blob_client. 
   
Biblioteket skal nå fungere 🎉


## Oppgave 4 - Forbedre prompten
En godt formulert prompt er avgjørende for å generere relevante og presise resultater.

1. Gå gjennom eksisterende tekst i prompten i playlist_generator.py.