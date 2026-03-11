import React, { createContext, useContext, useEffect, useState } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  NavLink,
  Link,
  useParams,
  Outlet,
  useLocation,
} from "react-router-dom";
import "./styles/global.css";

/**
 * Top-level App component
 *
 * Responsibilities:
 * - Sets up client-side routing for:
 *   / (Home)
 *   /tutorials (list)
 *   /tutorials/:id (tutorial detail)
 *   /print/:id (print view)
 * - Renders Header and Footer for non-print routes
 * - Provides a simple ThemeContext and provider
 * - Includes accessible navigation landmarks and a skip-to-content link
 */

/* -------------------------
   Theme context (simple)
   ------------------------- */
type Theme = "light" | "dark";
type ThemeContextType = {
  theme: Theme;
  toggleTheme: () => void;
};
const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [theme, setTheme] = useState<Theme>("light");

  useEffect(() => {
    // sync with document for easy CSS theming (e.g., [data-theme="dark"] ...)
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  const toggleTheme = () => setTheme((t) => (t === "light" ? "dark" : "light"));

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = (): ThemeContextType => {
  const ctx = useContext(ThemeContext);
  if (!ctx) {
    throw new Error("useTheme must be used within ThemeProvider");
  }
  return ctx;
};

/* -------------------------
   Small UI pieces
   ------------------------- */

const SkipToContent: React.FC = () => {
  // simple inline styles to ensure skip link is usable even if global.css doesn't define it
  const skipStyle: React.CSSProperties = {
    position: "absolute",
    top: -40,
    left: 8,
    background: "#000",
    color: "#fff",
    padding: "8px 12px",
    zIndex: 100,
    borderRadius: 4,
    transition: "top 0.2s",
  };
  const skipFocusStyle: React.CSSProperties = { top: 8 };

  // We cannot style :focus-within here without CSS, so use onFocus/onBlur to move it
  const [focused, setFocused] = useState(false);

  return (
    <a
      href="#main-content"
      onFocus={() => setFocused(true)}
      onBlur={() => setFocused(false)}
      style={focused ? { ...skipStyle, ...skipFocusStyle } : skipStyle}
      aria-label="Skip to main content"
    >
      Skip to content
    </a>
  );
};

const Header: React.FC = () => {
  const { theme, toggleTheme } = useTheme();
  return (
    <header role="banner" className="site-header" style={{ padding: "1rem", borderBottom: "1px solid #ddd" }}>
      <div className="header-inner" style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <h1 style={{ margin: 0, fontSize: "1.25rem" }}>
            <Link to="/" style={{ textDecoration: "none", color: "inherit" }}>
              Tutorial Site
            </Link>
          </h1>
          <p style={{ margin: 0, fontSize: "0.875rem" }}>Learn by doing</p>
        </div>

        <nav role="navigation" aria-label="Primary" style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
          <NavLink to="/" end style={({ isActive }) => ({ textDecoration: isActive ? "underline" : "none" })}>
            Home
          </NavLink>
          <NavLink to="/tutorials" style={({ isActive }) => ({ textDecoration: isActive ? "underline" : "none" })}>
            Tutorials
          </NavLink>
          <button onClick={toggleTheme} aria-pressed={theme === "dark"} style={{ marginLeft: "1rem" }}>
            {theme === "light" ? "Switch to dark" : "Switch to light"}
          </button>
        </nav>
      </div>
    </header>
  );
};

const Footer: React.FC = () => {
  return (
    <footer role="contentinfo" className="site-footer" style={{ padding: "1rem", borderTop: "1px solid #ddd", marginTop: "2rem" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <small>&copy; {new Date().getFullYear()} Tutorial Site</small>
        <nav aria-label="Footer" style={{ display: "flex", gap: "1rem" }}>
          <Link to="/tutorials">Tutorials</Link>
          <a href="/contact" onClick={(e) => e.preventDefault()}>
            Contact
          </a>
        </nav>
      </div>
    </footer>
  );
};

/* -------------------------
   Pages
   ------------------------- */

const Home: React.FC = () => {
  return (
    <main id="main-content" role="main" tabIndex={-1} style={{ padding: "1rem" }}>
      <h2>Welcome</h2>
      <p>This is the homepage. Browse tutorials to get started.</p>
      <p>
        <Link to="/tutorials">See tutorials</Link>
      </p>
    </main>
  );
};

const TutorialsList: React.FC = () => {
  // placeholder data
  const tutorials = [
    { id: "1", title: "Build a To-Do App" },
    { id: "2", title: "Introduction to TypeScript" },
    { id: "3", title: "React Accessibility Basics" },
  ];

  return (
    <main id="main-content" role="main" tabIndex={-1} style={{ padding: "1rem" }}>
      <h2>Tutorials</h2>
      <ul>
        {tutorials.map((t) => (
          <li key={t.id}>
            <Link to={`/tutorials/${t.id}`}>{t.title}</Link>
            {" — "}
            <Link to={`/print/${t.id}`} aria-label={`Print view for ${t.title}`}>
              Print
            </Link>
          </li>
        ))}
      </ul>
    </main>
  );
};

const TutorialDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  // In a real app, you'd fetch the tutorial by id
  return (
    <main id="main-content" role="main" tabIndex={-1} style={{ padding: "1rem" }}>
      <h2>Tutorial {id}</h2>
      <p>Details for tutorial {id} would be shown here.</p>
      <p>
        <Link to={`/print/${id}`} aria-label={`Print view for tutorial ${id}`}>
          Open print view
        </Link>
      </p>
      <p>
        <Link to="/tutorials">&larr; Back to tutorials</Link>
      </p>
    </main>
  );
};

const PrintView: React.FC = () => {
  const { id } = useParams<{ id: string }>();

  // For print route, we intentionally do not render header/footer (handled by layout)
  // Provide a simple print-optimized layout; assume global.css contains @media print rules
  return (
    <div role="main" aria-label={`Printable view for tutorial ${id}`} style={{ padding: "1rem" }}>
      <h1>Tutorial {id} — Printable Version</h1>
      <p>This view is optimized for printing.</p>
      <section>
        <h2>Content</h2>
        <p>Printable content for tutorial {id} goes here.</p>
      </section>
      <p>
        <Link to={`/tutorials/${id}`}>Return to tutorial</Link>
      </p>
    </div>
  );
};

/* -------------------------
   Layout component (non-print)
   ------------------------- */
const AppLayout: React.FC = () => {
  return (
    <>
      <Header />
      {/* The Outlet will render Home, TutorialsList, TutorialDetail */}
      <Outlet />
      <Footer />
    </>
  );
};

/* -------------------------
   App: Router and top-level provider
   ------------------------- */

const AppRouter: React.FC = () => {
  return (
    <BrowserRouter>
      <SkipToContent />
      <Routes>
        {/* Layout route for all non-print routes */}
        <Route path="/" element={<AppLayout />}>
          <Route index element={<Home />} />
          <Route path="tutorials" element={<TutorialsList />} />
          <Route path="tutorials/:id" element={<TutorialDetail />} />
        </Route>

        {/* Print route intentionally outside the main layout so no header/footer render */}
        <Route path="print/:id" element={<PrintView />} />

        {/* Fallback - render simple page inside layout */}
        <Route
          path="*"
          element={
            <AppLayout>
              <main id="main-content" role="main" tabIndex={-1} style={{ padding: "1rem" }}>
                <h2>Page not found</h2>
                <p>
                  <Link to="/">Go home</Link>
                </p>
              </main>
            </AppLayout>
          }
        />
      </Routes>
    </BrowserRouter>
  );
};

const App: React.FC = () => {
  return (
    <ThemeProvider>
      <AppRouter />
    </ThemeProvider>
  );
};

export default App;