# Norm AI Take-Home — Client

This is a minimal [Next.js](https://nextjs.org/) application that provides a simple UI for querying the FastAPI backend.

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
- The response from the backend will be displayed below the search box with citations.

**Example flow:**  
1. Run the backend (via `uvicorn` or Docker)  
2. Run the frontend (`npm run dev`)  
3. Navigate to [http://localhost:3000](http://localhost:3000) and try:  
   ```
   Ask: Which crimes result in amputation?
   ```

---

## Design Choices & Assumptions

- **Proof of concept:** The frontend is intentionally minimal, designed to demonstrate backend functionality and end-to-end flow.  
- **Live backend integration:** Queries are sent to the FastAPI `/search` endpoint, which returns synthesized answers with citations from `laws.pdf`.  
- **Example queries:** Hard-coded buttons make it easy to demo common queries without typing.  
- **Lightweight UI:** Minimal styling, neutral look. The assumption is that the client is evaluating functionality and clarity of flow, not polish.  