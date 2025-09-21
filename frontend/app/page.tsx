'use client';

import { useState } from 'react';
import HeaderNav from '@/components/HeaderNav';

type Citation = {
  source: string;
  text: string;
};

type SearchResponse = {
  query: string;
  response: string;
  citations: Citation[];
};

export default function Page() {
  const [query, setQuery] = useState('');
  const [data, setData] = useState<SearchResponse | null>(null);
  const [showJson, setShowJson] = useState(false);

  async function runSearch() {
    const res = await fetch(
      `http://localhost:8000/search?query=${encodeURIComponent(query)}`
    );
    const json = await res.json();
    setData(json);
    setQuery(''); // clear input
  }

  return (
    <>
      <HeaderNav signOut={() => {}} />
      <main style={{ padding: '2rem' }}>
        <h1 style={{ textAlign: "right" }}>Norm Ai – Search Demo</h1>

        {/* Example questions + search box */}
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          {/* Example buttons */}
          <div style={{ marginBottom: '1rem' }}>
            <button onClick={() => setQuery("Which crimes result in amputation?")}>
              Ask: Which crimes result in amputation?
            </button>
            <button
              style={{ marginLeft: '1rem' }}
              onClick={() => setQuery("Is it against the law to sell bad food?")}
            >
              Ask: Is it against the law to sell bad food?
            </button>
          </div>

          {/* Search bar */}
          <div>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Enter thy query of the law..."
              style={{
                width: '400px',
                maxWidth: '100%',
                marginRight: '0.5rem',
                padding: '0.5rem',
                border: '1px solid #ccc',
                borderRadius: '4px',
              }}
            />
            <button onClick={runSearch}>Search</button>
          </div>
        </div>


        {data && (
          <section style={{ marginTop: '2rem' }}>
            {/* Query (above, smaller, lighter) */}
            <p style={{ fontSize: '1.1rem', fontStyle: 'italic', color: '#555' }}>
              {data.query}
            </p>

            {/* Response (below, larger, black) */}
            <p style={{ fontSize: '1.3rem', fontWeight: '500', color: '#000', margin: '0.5rem 0 1.5rem' }}>
              {data.response}
            </p>

            {/* Citations */}
            <div style={{ marginTop: '3rem' }}></div>
            <ul style={{ listStyle: 'none', paddingLeft: 0 }}>
              {data.citations.map((c, i) => (
                <li
                  key={i}
                  style={{
                    marginBottom: '1rem',
                    padding: '0.5rem 0',
                    borderBottom: '1px solid #eee',
                  }}
                >
                  <p style={{ margin: 0, color: '#333' }}>{c.text}</p>
                  <span style={{ fontSize: '0.9rem', color: '#777' }}>
                    — {c.source}
                  </span>
                </li>
              ))}
            </ul>
            <div style={{ marginBottom: '2rem' }}></div>
          </section>
        )}

        {/* Keep raw JSON for debugging */}
        <div style={{ marginTop: '7rem' }}>
          <button onClick={() => setShowJson(!showJson)}>
            {showJson ? "Hide Raw API Response" : "Show Raw API Response"}
          </button>
          {showJson && (
            <pre style={{ color: 'gray', marginTop: '1rem' }}>
              {data ? JSON.stringify(data, null, 2) : 'No results yet'}
            </pre>
          )}
        </div>
      </main>
    </>
  );
}
