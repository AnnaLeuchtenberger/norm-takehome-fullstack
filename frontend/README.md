# Norm AI Take-Home — Client

This is a minimal React [Next.js](https://nextjs.org/) application that provides a simple UI for querying the FastAPI backend.

## Running the Application

### Prerequisites
- Node.js 18+  
- npm / yarn / pnpm / bun (choose one)  

### Local Development

1. **Install dependencies**  
   ```bash
   cd frontend
   npm install   # or yarn / pnpm / bun
   ```

2. **Start the dev server**  
   ```bash
   npm run dev
   ```
   The app will be available at [http://localhost:3000](http://localhost:3000).

3. **Connect to the backend**  
   By default, the client assumes the FastAPI server is running locally on port **8000**.  
   - **Backend endpoint:** `http://localhost:8000/search`  
   - Make sure the backend is running before issuing queries.

---

## Usage

- Type a question into the search box and press **Search**.  
- Or click one of the **example question buttons** to auto-fill the search box.  
- The response from the backend will be displayed below the search box.  

**Example flow:**  
1. Run the backend (`uvicorn app.main:app --reload`)  
2. Run the frontend (`npm run dev`)  
3. Navigate to [http://localhost:3000](http://localhost:3000) and try:  
   ```
   Ask: Which crimes result in amputation?
   ```


## Design Choices & Assumptions

- **Proof of concept** This project assumes it is a proof of concept for the client, and that the functionality expectations will stay within clearly delimited guardrails during the demo.
- **Stubbed backend:** The client calls the `/search` endpoint, which uses a stubbed Qdrant service unless configured otherwise. This is not a fully formed app (yet).
- **Example queries:** Hard-coded buttons demonstrate how to issue typical queries. Two answers are stubbed out - one about bakers, one about thieves. The goal is to make it easy for someone demo-ing this to the client - just click a button, and the search bar is prepopulated. 
- **Minimal search functionality** The logic powering the example queries also enables some custom queries, albeit ones leading to the same two answers. The "baker" answer is triggered by any of these words: "food," "baker," "flour," or "bread". The "thief" answer is triggered by any of these words: "hand"  "finger,"  "amputation,"  "thief," or "steal." Combining these two queries is currently not supported. 
- **Lightweight UI:** Minimal styling, neutral UI. The assumption is that the client is evaluating for functionality and intuitive understanding of the site's flow, not customization -- their own UI will come later. 
---

## Server

See the `app` folder for the FastAPI backend service, including setup instructions.
