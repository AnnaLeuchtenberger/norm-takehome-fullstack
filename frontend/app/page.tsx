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

  async function runSearch() {
    const res = await fetch(
      `http://localhost:8000/search?query=${encodeURIComponent(query)}`
    );
    const json = await res.json();
    setData(json);
  }

  return (
    <>
      <HeaderNav signOut={() => {}} />
      <main style={{ padding: '2rem' }}>
        <h1>Norm Ai – Search Demo</h1>

        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your query..."
        />
        <button onClick={runSearch}>Search</button>

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
            <h3 style={{ marginBottom: '0.5rem' }}>Citations</h3>
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
          </section>
        )}

        {/* Keep raw JSON for debugging */}
        <pre style={{ marginTop: '2rem', color: 'gray' }}>
          {data ? JSON.stringify(data, null, 2) : 'No results yet'}
        </pre>
      </main>
    </>
  );
}
