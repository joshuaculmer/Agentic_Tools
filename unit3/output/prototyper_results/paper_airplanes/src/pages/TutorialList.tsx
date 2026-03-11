import React, { useMemo, useState } from "react";
import { Link } from "react-router-dom";

/**
 * TutorialList.tsx
 *
 * Page that lists tutorials grouped by difficulty with simple client-side filtering.
 * - Uses an inline TutorialCard component (self-contained for this file).
 * - Responsive CSS grid for cards.
 * - Filter buttons for difficulties with accessible aria-pressed states.
 * - Each card links to /tutorials/:id and has a "Printable view" button that opens /tutorials/:id/print in a new tab.
 */

/* ---------- Types ---------- */
type Difficulty = "Easy" | "Medium" | "Advanced";

type Tutorial = {
  id: string;
  title: string;
  difficulty: Difficulty;
  description: string;
  thumbnail?: string; // URL or data URI
};

/* ---------- Sample data: five tutorials ---------- */
const TUTORIALS: Tutorial[] = [
  {
    id: "t1",
    title: "Build a To-Do App",
    difficulty: "Easy",
    description: "Learn how to create a simple to-do app with add/remove and persistence.",
    thumbnail: generatePlaceholderDataUri("To-Do"),
  },
  {
    id: "t2",
    title: "Intro to TypeScript",
    difficulty: "Easy",
    description: "A gentle introduction to TypeScript and static typing in React apps.",
    thumbnail: generatePlaceholderDataUri("TS"),
  },
  {
    id: "t3",
    title: "Responsive Layouts",
    difficulty: "Medium",
    description: "Techniques for designing responsive UIs using CSS Grid and Flexbox.",
    thumbnail: generatePlaceholderDataUri("Grid"),
  },
  {
    id: "t4",
    title: "State Management Patterns",
    difficulty: "Medium",
    description: "Compare context, reducers, and external libraries for managing app state.",
    thumbnail: generatePlaceholderDataUri("State"),
  },
  {
    id: "t5",
    title: "Web Performance Optimization",
    difficulty: "Advanced",
    description: "Strategies to measure and speed up real-world web applications.",
    thumbnail: generatePlaceholderDataUri("Perf"),
  },
];

/* ---------- Utilities ---------- */
function generatePlaceholderDataUri(text: string) {
  // Simple SVG placeholder as data URI
  const svg = encodeURIComponent(
    `<svg xmlns='http://www.w3.org/2000/svg' width='400' height='240'>
      <rect width='100%' height='100%' fill='#f3f4f6'/>
      <text x='50%' y='50%' fill='#9ca3af' font-family='Arial, Helvetica, sans-serif' font-size='28' dominant-baseline='middle' text-anchor='middle'>${text}</text>
    </svg>`
  );
  return `data:image/svg+xml;charset=UTF-8,${svg}`;
}

/* ---------- TutorialCard: local simple implementation ---------- */
function TutorialCard({
  tutorial,
  onOpenPrint,
}: {
  tutorial: Tutorial;
  onOpenPrint: (id: string) => void;
}) {
  return (
    <article className="tutorial-card" aria-labelledby={`title-${tutorial.id}`}>
      <div className="thumbnail">
        <img src={tutorial.thumbnail} alt={`${tutorial.title} thumbnail`} />
        <span className={`badge badge-${tutorial.difficulty.toLowerCase()}`}>
          {tutorial.difficulty}
        </span>
      </div>
      <div className="card-body">
        <h3 id={`title-${tutorial.id}`} className="card-title">
          <Link to={`/tutorials/${tutorial.id}`} className="card-link">
            {tutorial.title}
          </Link>
        </h3>
        <p className="card-desc">{tutorial.description}</p>
        <div className="card-actions">
          <Link to={`/tutorials/${tutorial.id}`} className="btn btn-primary" aria-label={`Open ${tutorial.title} details`}>
            View details
          </Link>
          <button
            type="button"
            className="btn btn-outline"
            onClick={() => onOpenPrint(tutorial.id)}
            aria-label={`Open printable view for ${tutorial.title}`}
          >
            Printable view
          </button>
        </div>
      </div>
    </article>
  );
}

/* ---------- Main page component ---------- */
export default function TutorialList(): JSX.Element {
  const difficulties: Difficulty[] = ["Easy", "Medium", "Advanced"];
  // Start with all filters active
  const [activeFilters, setActiveFilters] = useState<Record<Difficulty, boolean>>({
    Easy: true,
    Medium: true,
    Advanced: true,
  });

  const toggleFilter = (d: Difficulty) => {
    setActiveFilters((prev) => ({ ...prev, [d]: !prev[d] }));
  };

  const visibleTutorials = useMemo(
    () => TUTORIALS.filter((t) => activeFilters[t.difficulty]),
    [activeFilters]
  );

  const openPrintable = (id: string) => {
    const url = `/tutorials/${id}/print`;
    // Open in a new tab/window
    window.open(url, "_blank", "noopener,noreferrer");
  };

  return (
    <div className="tutorial-list-page">
      <style>{styles}</style>

      <header className="page-header">
        <h1>Tutorials</h1>
        <p className="lead">Browse tutorials grouped by difficulty. Use the filters to narrow results.</p>

        <div
          className="filter-bar"
          role="toolbar"
          aria-label="Filter tutorials by difficulty"
        >
          {difficulties.map((d) => (
            <button
              key={d}
              type="button"
              className={`filter-btn ${activeFilters[d] ? "active" : ""}`}
              onClick={() => toggleFilter(d)}
              aria-pressed={activeFilters[d]}
              aria-label={`Filter ${d} tutorials`}
            >
              {d}
            </button>
          ))}
          <button
            type="button"
            className="filter-btn reset"
            onClick={() =>
              setActiveFilters({ Easy: true, Medium: true, Advanced: true })
            }
            aria-label="Reset filters"
          >
            Reset
          </button>
        </div>
      </header>

      <main>
        {difficulties.map((d) => {
          const group = TUTORIALS.filter((t) => t.difficulty === d);
          const visibleInGroup = group.filter((t) => activeFilters[d]);

          return (
            <section key={d} className="group-section" aria-labelledby={`group-${d}`}>
              <h2 id={`group-${d}`} className="group-heading">{d}</h2>

              {visibleInGroup.length > 0 ? (
                <div className="grid" role="list">
                  {visibleInGroup.map((t) => (
                    <div key={t.id} role="listitem" className="grid-item">
                      <TutorialCard tutorial={t} onOpenPrint={openPrintable} />
                    </div>
                  ))}
                </div>
              ) : (
                <div className="empty-state">
                  {activeFilters[d]
                    ? "No tutorials in this category."
                    : "Filtered out."}
                </div>
              )}
            </section>
          );
        })}

        {/* If no tutorials visible at all, show a helpful message */}
        {visibleTutorials.length === 0 && (
          <div className="no-results" role="status">
            No tutorials match the selected filters.
          </div>
        )}
      </main>
    </div>
  );
}

/* ---------- Minimal CSS (kept here for a self-contained file) ---------- */
const styles = `
:root{
  --gap: 16px;
  --card-radius: 8px;
  --primary: #2563eb;
  --muted: #6b7280;
  --bg: #ffffff;
  --surface: #ffffff;
  --border: #e5e7eb;
  --easy: #10b981;
  --medium: #f59e0b;
  --advanced: #ef4444;
}

.tutorial-list-page{
  max-width: 1100px;
  margin: 24px auto;
  padding: 0 16px 48px;
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
  color: #111827;
}

.page-header {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
  font-size: 28px;
}

.lead {
  margin: 0;
  color: var(--muted);
  font-size: 14px;
}

.filter-bar {
  display: flex;
  gap: 8px;
  margin-top: 12px;
  flex-wrap: wrap;
  align-items: center;
}

.filter-btn {
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: #fff;
  cursor: pointer;
  font-size: 14px;
  color: #111827;
}

.filter-btn.active {
  background: linear-gradient(180deg, rgba(37,99,235,0.08), rgba(37,99,235,0.04));
  border-color: rgba(37,99,235,0.25);
  box-shadow: 0 1px 0 rgba(16,24,40,0.02);
}

.filter-btn.reset {
  margin-left: 8px;
  background: transparent;
  border-style: dashed;
  color: var(--muted);
}

/* Group section */
.group-section {
  margin-top: 28px;
}

.group-heading {
  font-size: 18px;
  margin: 0 0 12px 0;
}

/* Grid */
.grid {
  display: grid;
  gap: var(--gap);
  grid-template-columns: repeat(1, 1fr);
}

@media (min-width: 640px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 980px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.grid-item {
  list-style: none;
}

/* Card */
.tutorial-card {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--border);
  border-radius: var(--card-radius);
  overflow: hidden;
  background: var(--surface);
  height: 100%;
}

.thumbnail {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  overflow: hidden;
  background: #f9fafb;
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.badge {
  position: absolute;
  top: 8px;
  left: 8px;
  padding: 6px 8px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  color: white;
  text-transform: uppercase;
}

.badge-easy {
  background: var(--easy);
}

.badge-medium {
  background: var(--medium);
}

.badge-advanced {
  background: var(--advanced);
}

.card-body {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1 1 auto;
}

.card-title {
  margin: 0;
  font-size: 16px;
}

.card-link {
  color: inherit;
  text-decoration: none;
}

.card-link:hover {
  text-decoration: underline;
}

.card-desc {
  margin: 0;
  color: var(--muted);
  font-size: 14px;
  flex: 1 1 auto;
}

.card-actions {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-top: 6px;
}

.btn {
  padding: 8px 10px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: #fff;
  cursor: pointer;
  text-decoration: none;
  font-size: 14px;
}

.btn-primary {
  background: var(--primary);
  color: #fff;
  border-color: rgba(37,99,235,0.8);
}

.btn-outline {
  background: transparent;
  color: var(--muted);
  border-color: var(--border);
}

/* Empty / No results */
.empty-state {
  color: var(--muted);
  font-size: 14px;
  padding: 8px 0;
}

.no-results {
  margin-top: 24px;
  padding: 12px;
  background: #fff7ed;
  border: 1px solid #fde3c6;
  color: #7c2d12;
  border-radius: 8px;
}
`;
