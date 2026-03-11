import React from 'react';
import { Link } from 'react-router-dom';
import hero1 from '../assets/hero1.png';
import hero2 from '../assets/hero2.png';
import hero3 from '../assets/hero3.png';
import hero4 from '../assets/hero4.png';
import { tutorials as tutorialsData } from '../data/tutorials';

type Tutorial = {
  id: string;
  title: string;
  ageRange?: string;
  description?: string;
  thumbnail?: string;
  slug?: string;
};

const heroImages = [hero1, hero2, hero3, hero4];

const containerStyle: React.CSSProperties = {
  fontFamily: '"Baloo 2", "Comic Sans MS", "Trebuchet MS", sans-serif',
  color: '#2a2a2a',
  lineHeight: 1.35,
  padding: '1rem',
};

const heroStyle: React.CSSProperties = {
  background: 'linear-gradient(135deg, #FFFBF2 0%, #F6FDFF 100%)',
  borderRadius: 12,
  padding: '2rem',
  display: 'flex',
  flexWrap: 'wrap',
  gap: '1.5rem',
  alignItems: 'center',
  justifyContent: 'space-between',
  marginBottom: '1.5rem',
};

const heroTextStyle: React.CSSProperties = {
  flex: '1 1 320px',
  minWidth: 280,
};

const heroTitleStyle: React.CSSProperties = {
  fontSize: 'clamp(1.75rem, 3vw, 2.5rem)',
  margin: '0 0 0.5rem 0',
  color: '#234d6a',
};

const heroSubStyle: React.CSSProperties = {
  margin: '0 0 1rem 0',
  fontSize: '1rem',
  color: '#3b3b3b',
};

const ctaRowStyle: React.CSSProperties = {
  display: 'flex',
  gap: '0.75rem',
  flexWrap: 'wrap',
};

const ctaButtonStyle: React.CSSProperties = {
  padding: '0.6rem 1rem',
  borderRadius: 8,
  border: 'none',
  cursor: 'pointer',
  textDecoration: 'none',
  fontWeight: 700,
  display: 'inline-block',
};

const primaryStyle: React.CSSProperties = {
  ...ctaButtonStyle,
  background: '#6CC4A1',
  color: 'white',
};

const secondaryStyle: React.CSSProperties = {
  ...ctaButtonStyle,
  background: '#FFFFFF',
  color: '#234d6a',
  border: '2px solid #E8F5EE',
};

const heroImagesStyle: React.CSSProperties = {
  display: 'flex',
  gap: '0.6rem',
  flex: '0 0 320px',
  justifyContent: 'center',
  alignItems: 'center',
};

const heroImgStyle: React.CSSProperties = {
  width: 72,
  height: 72,
  objectFit: 'cover',
  borderRadius: 10,
  boxShadow: '0 6px 14px rgba(37, 63, 83, 0.08)',
  background: 'white',
  padding: 6,
};

const sectionStyle: React.CSSProperties = {
  marginBottom: '1.25rem',
};

const gridStyle: React.CSSProperties = {
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
  gap: '1rem',
};

const cardStyle: React.CSSProperties = {
  background: 'white',
  borderRadius: 10,
  padding: '0.75rem',
  boxShadow: '0 6px 18px rgba(38, 54, 68, 0.06)',
  display: 'flex',
  gap: '0.75rem',
  alignItems: 'flex-start',
};

const thumbStyle: React.CSSProperties = {
  width: 84,
  height: 64,
  objectFit: 'cover',
  borderRadius: 8,
  flex: '0 0 84px',
};

const quickLinksStyle: React.CSSProperties = {
  display: 'flex',
  gap: '0.5rem',
  flexWrap: 'wrap',
};

export default function Home(): JSX.Element {
  const tutorials: Tutorial[] = Array.isArray(tutorialsData)
    ? (tutorialsData as Tutorial[])
    : [];

  const featured = tutorials.length > 0 ? tutorials.slice(0, 4) : [
    {
      id: 'paper-flowers',
      title: 'Easy Paper Flowers',
      ageRange: '5–9',
      description: 'Make colorful flowers with simple paper and glue.',
      thumbnail: hero1,
      slug: '/tutorials/paper-flowers',
    },
    {
      id: 'sticker-book',
      title: 'Sticker Storybook',
      ageRange: '4–8',
      description: 'Create a short story using stickers and drawings.',
      thumbnail: hero2,
      slug: '/tutorials/sticker-book',
    },
    {
      id: 'handprint-animals',
      title: 'Handprint Animals',
      ageRange: '2–6',
      description: 'Turn handprints into cute animal characters.',
      thumbnail: hero3,
      slug: '/tutorials/handprint-animals',
    },
    {
      id: 'simple-cards',
      title: 'Simple Greeting Cards',
      ageRange: '6–12',
      description: 'Design cards for family with coloring and cutouts.',
      thumbnail: hero4,
      slug: '/tutorials/simple-cards',
    },
  ];

  return (
    <div style={containerStyle}>
      <header aria-labelledby="site-heading">
        <div style={heroStyle} role="region" aria-label="Welcome banner">
          <div style={heroTextStyle}>
            <h1 id="site-heading" style={heroTitleStyle}>
              Creative Kids Studio
            </h1>
            <p style={heroSubStyle}>
              Hands-on, screen-friendly projects made for curious kids and busy parents.
              Short, joyful tutorials that spark imagination and build fine motor skills.
            </p>

            <div style={ctaRowStyle}>
              <Link to="/tutorials" style={primaryStyle} aria-label="Browse tutorials">
                Browse Tutorials
              </Link>
              <Link to="/printables" style={secondaryStyle} aria-label="Download printable templates">
                Printable Templates
              </Link>
            </div>
            <p style={{ marginTop: '0.75rem', fontSize: '0.9rem', color: '#556' }}>
              Suitable activities for ages 2–12. New projects added every week!
            </p>
          </div>

          <div style={heroImagesStyle} aria-hidden>
            {heroImages.map((src, i) => (
              <img
                key={i}
                src={src}
                alt={`Decorative sample ${i + 1}`}
                style={heroImgStyle}
                loading="lazy"
              />
            ))}
          </div>
        </div>
      </header>

      <main>
        <section style={sectionStyle} aria-labelledby="featured-heading">
          <h2 id="featured-heading" style={{ margin: '0 0 0.5rem 0', color: '#234d6a' }}>
            Featured Tutorials
          </h2>
          <p style={{ margin: '0 0 0.75rem 0', color: '#486' }}>
            A few of our favorite quick projects — great for a rainy afternoon or a crafty party.
          </p>

          <div style={gridStyle} role="list" aria-label="Featured tutorials list">
            {featured.map((t) => (
              <article key={t.id} style={cardStyle} role="listitem" aria-labelledby={`t-${t.id}-title`}>
                <img
                  src={t.thumbnail}
                  alt={t.title ? `${t.title} thumbnail` : `Tutorial ${t.id} thumbnail`}
                  style={thumbStyle}
                  loading="lazy"
                />
                <div style={{ flex: 1 }}>
                  <h3 id={`t-${t.id}-title`} style={{ margin: '0 0 0.25rem 0', fontSize: '1rem' }}>
                    {t.title}
                  </h3>
                  <p style={{ margin: '0 0 0.4rem 0', color: '#556', fontSize: '0. nine' }}>
                    <strong style={{ color: '#6b8' }}>{t.ageRange}</strong>{' '}
                    {t.description ? `— ${t.description}` : ''}
                  </p>
                  <div>
                    <Link
                      to={t.slug || `/tutorials/${t.id}`}
                      style={{ color: '#2a7aa6', textDecoration: 'underline', fontWeight: 600 }}
                      aria-label={`Open tutorial ${t.title}`}
                    >
                      View Tutorial
                    </Link>
                  </div>
                </div>
              </article>
            ))}
          </div>
        </section>

        <section style={sectionStyle} aria-labelledby="quick-links-heading">
          <h2 id="quick-links-heading" style={{ margin: '0 0 0.5rem 0', color: '#234d6a' }}>
            Quick Links
          </h2>
          <p style={{ margin: '0 0 0.5rem 0', color: '#3b3b3b' }}>
            Jump to the places parents and kids visit most.
          </p>
          <nav aria-label="Quick links">
            <div style={quickLinksStyle}>
              <Link to="/tutorials" style={secondaryStyle}>
                All Tutorials
              </Link>
              <Link to="/printables" style={secondaryStyle}>
                Printable Templates
              </Link>
              <Link to="/about" style={secondaryStyle}>
                About Us
              </Link>
              <Link to="/contact" style={secondaryStyle}>
                Contact
              </Link>
            </div>
          </nav>
        </section>
      </main>

      <footer style={{ marginTop: '1.5rem', color: '#7a7a7a', fontSize: '0.9rem' }} aria-label="Site footer">
        <p style={{ margin: 0 }}>
          © {new Date().getFullYear()} Creative Kids Studio — gentle, fun learning for ages 2–12.
        </p>
      </footer>
    </div>
  );
}