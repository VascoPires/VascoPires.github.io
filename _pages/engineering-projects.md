---
layout: page
permalink: /projects/
title: projects
description: Selected research, engineering, and technical work.
nav: true
nav_order: 3
---

<style>
  .projects-hero {
    margin: 0 0 2rem;
    padding: 1.6rem 1.6rem 1.4rem;
    border: 1px solid rgba(120, 140, 180, 0.18);
    border-radius: 20px;
    background: linear-gradient(135deg, rgba(70, 95, 160, 0.08), rgba(255, 255, 255, 0.02));
  }

  .projects-kicker {
    margin: 0 0 0.55rem;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--global-theme-color);
  }

  .projects-hero h1,
  .projects-hero h2 {
    margin-bottom: 0.8rem;
  }

  .projects-lead {
    max-width: 48rem;
    font-size: 1.06rem;
    line-height: 1.75;
    margin-bottom: 1rem;
  }

  .chip-row,
  .skill-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.55rem;
  }

  .chip,
  .skill-chip {
    display: inline-flex;
    align-items: center;
    padding: 0.45rem 0.8rem;
    border-radius: 999px;
    border: 1px solid rgba(120, 140, 180, 0.2);
    background: rgba(120, 140, 180, 0.08);
    font-size: 0.9rem;
    line-height: 1.2;
  }

  .project-section {
    display: grid;
    grid-template-columns: minmax(0, 1.2fr) minmax(280px, 0.8fr);
    gap: 1.5rem;
    margin: 2rem 0;
    align-items: start;
  }

  .project-section.reverse {
    grid-template-columns: minmax(280px, 0.8fr) minmax(0, 1.2fr);
  }

  .project-card,
  .media-card,
  .supporting-card,
  .mini-card {
    border: 1px solid rgba(120, 140, 180, 0.16);
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.02);
    box-shadow: 0 12px 30px rgba(20, 28, 45, 0.06);
  }

  .project-card {
    padding: 1.5rem;
  }

  .project-meta {
    margin-bottom: 0.85rem;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--global-theme-color);
  }

  .project-card h3 {
    margin-bottom: 0.65rem;
  }

  .project-summary {
    font-size: 1.02rem;
    line-height: 1.7;
    margin-bottom: 1rem;
  }

  .project-details {
    display: grid;
    gap: 0.8rem;
  }

  .project-details div {
    padding-top: 0.7rem;
    border-top: 1px solid rgba(120, 140, 180, 0.12);
  }

  .project-details strong {
    display: block;
    margin-bottom: 0.25rem;
  }

  .media-card {
    position: sticky;
    top: 92px;
    padding: 1rem;
  }

  .media-frame {
    min-height: 320px;
    border-radius: 16px;
    border: 1px dashed rgba(120, 140, 180, 0.32);
    background:
      radial-gradient(circle at top left, rgba(96, 125, 200, 0.2), transparent 34%),
      linear-gradient(160deg, rgba(15, 23, 42, 0.14), rgba(120, 140, 180, 0.05));
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 1.2rem;
    color: var(--global-text-color-light);
    font-size: 0.95rem;
    line-height: 1.6;
  }

  .media-caption {
    margin-top: 0.75rem;
    font-size: 0.9rem;
    color: var(--global-text-color-light);
  }

  .section-heading {
    margin: 3rem 0 1rem;
  }

  .supporting-grid,
  .mini-grid {
    display: grid;
    gap: 1rem;
  }

  .supporting-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .mini-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .supporting-card,
  .mini-card {
    padding: 1.15rem;
  }

  .supporting-card h4,
  .mini-card h4 {
    margin-bottom: 0.45rem;
  }

  .placeholder-note {
    margin-top: 0.9rem;
    padding: 0.8rem 0.95rem;
    border-radius: 14px;
    background: rgba(120, 140, 180, 0.08);
    font-size: 0.92rem;
  }

  @media (max-width: 900px) {
    .project-section,
    .project-section.reverse,
    .supporting-grid,
    .mini-grid {
      grid-template-columns: 1fr;
    }

    .media-card {
      position: static;
    }
  }
</style>

<section class="projects-hero">
  <p class="projects-kicker">Research, engineering, and technical communication</p>
  <h1>Selected projects</h1>
  <p class="projects-lead">
    This page is a compact overview of the work that best reflects my profile as an engineer-researcher. It brings together composite materials, structural mechanics, aerospace-oriented design, computation, and teaching without splitting everything into separate project pages.
  </p>
  <div class="chip-row">
    <span class="chip">Composite materials</span>
    <span class="chip">Structural mechanics</span>
    <span class="chip">Aerospace structures</span>
    <span class="chip">FEA and CAD</span>
    <span class="chip">Python and Matlab</span>
    <span class="chip">Technical writing</span>
    <span class="chip">Teaching</span>
  </div>
</section>

<section class="project-section">
  <article class="project-card">
    <div class="project-meta">Flagship work · Current research</div>
    <h3>PhD Research at Montanuniversitat Leoben</h3>
    <p class="project-summary">
      Research on the interaction of transverse cracks and delamination in cross-ply laminates, positioned at the intersection of composite materials, structural mechanics, and damage analysis.
    </p>
    <div class="skill-grid" style="margin-bottom: 1rem;">
      <span class="skill-chip">Composite damage</span>
      <span class="skill-chip">Structural analysis</span>
      <span class="skill-chip">FEA</span>
      <span class="skill-chip">Scientific writing</span>
    </div>
    <div class="project-details">
      <div>
        <strong>Context</strong>
        Current PhD research and teaching work in composite and polymer materials.
      </div>
      <div>
        <strong>Problem</strong>
        [Add the main research question here]
      </div>
      <div>
        <strong>What I did</strong>
        [Add your role in modelling, experiments, analysis, and teaching connection]
      </div>
      <div>
        <strong>Outcome</strong>
        [Add papers, findings, methods, or current status]
      </div>
    </div>
  </article>
  <aside class="media-card">
    <div class="media-frame">
      Replace this block with a laminate diagram, crack-path animation, simulation image, or test setup photo.
    </div>
    <p class="media-caption">A gif or technical figure works well here because it gives the page motion while keeping the writing compact.</p>
  </aside>
</section>

<section class="project-section reverse">
  <aside class="media-card">
    <div class="media-frame">
      Replace this block with a joint geometry image, failure sequence, poster crop, or short experimental gif.
    </div>
    <p class="media-caption">This is the strongest place to include a visual plus a short awards mention without making the page feel promotional.</p>
  </aside>
  <article class="project-card">
    <div class="project-meta">Flagship work · Thesis research</div>
    <h3>Master's Thesis at INEGI: Curved Composite Joints</h3>
    <p class="project-summary">
      Research on curved single lap joints designed to reduce delamination in composite structures, with clear relevance to aeronautical applications.
    </p>
    <div class="skill-grid" style="margin-bottom: 1rem;">
      <span class="skill-chip">Composite joints</span>
      <span class="skill-chip">Delamination</span>
      <span class="skill-chip">CAD</span>
      <span class="skill-chip">Conference communication</span>
    </div>
    <div class="project-details">
      <div>
        <strong>Context</strong>
        Master's thesis research carried out at INEGI.
      </div>
      <div>
        <strong>Problem</strong>
        [Add the design or failure problem addressed by the thesis]
      </div>
      <div>
        <strong>What I did</strong>
        [Add your work in design, analysis, testing, and dissemination]
      </div>
      <div>
        <strong>Outcome</strong>
        This thesis work received four awards and was presented in several conference formats. [Add the main technical outcome here]
      </div>
    </div>
  </article>
</section>

<section class="project-section">
  <article class="project-card">
    <div class="project-meta">Flagship work · Aerospace</div>
    <h3>ESA Structural and Configuration Work</h3>
    <p class="project-summary">
      Structural and configuration design for multi-spacecraft mission concepts developed through ESA programs, combining systems thinking with structural trade-offs and team-based mission design.
    </p>
    <div class="skill-grid" style="margin-bottom: 1rem;">
      <span class="skill-chip">Space systems</span>
      <span class="skill-chip">Configuration design</span>
      <span class="skill-chip">Concurrent design</span>
      <span class="skill-chip">Presentation</span>
    </div>
    <div class="project-details">
      <div>
        <strong>Context</strong>
        Combines ESA Alpbach Summer School and ESA Post Alpbach into one aerospace-focused project thread.
      </div>
      <div>
        <strong>Problem</strong>
        [Add the mission or systems challenge here]
      </div>
      <div>
        <strong>What I did</strong>
        [Add your role as lead structural/configuration engineer, trade-off work, and mission integration]
      </div>
      <div>
        <strong>Outcome</strong>
        Presented mission concepts to ESA experts and professionals.
      </div>
    </div>
  </article>
  <aside class="media-card">
    <div class="media-frame">
      Replace this block with a spacecraft render, systems layout, mission diagram, or team presentation image.
    </div>
    <p class="media-caption">A wide render or mission diagram would give this section a strong visual anchor.</p>
  </aside>
</section>

<h2 class="section-heading">Supporting work</h2>

<section class="supporting-grid">
  <article class="supporting-card">
    <h4>Medical Supply UAV in Composite Materials</h4>
    <p>
      Structural and kinematic development of wing and control-surface systems for a composite UAV intended for medical supply delivery in Nepal.
    </p>
    <div class="chip-row">
      <span class="chip">UAV design</span>
      <span class="chip">Composite structures</span>
      <span class="chip">CAD</span>
    </div>
    <div class="placeholder-note">Placeholder for UAV render, CAD screenshot, or short control-surface gif.</div>
  </article>

  <article class="supporting-card">
    <h4>CAD Reconstruction of a De Havilland Goblin Engine</h4>
    <p>
      Reconstruction of internal mechanisms and sub-assemblies in CAD using a real engine as reference, resulting in a technically grounded digital model of a historic jet engine.
    </p>
    <div class="chip-row">
      <span class="chip">CAD modelling</span>
      <span class="chip">Mechanical systems</span>
      <span class="chip">Technical visualization</span>
    </div>
    <div class="placeholder-note">Placeholder for CAD assembly image or exploded-view animation.</div>
  </article>

  <article class="supporting-card">
    <h4>Engineering Scripts and Computational Support</h4>
    <p>
      Space for Python or Matlab tools, automation scripts, post-processing workflows, and engineering utilities that support analysis or communication.
    </p>
    <div class="chip-row">
      <span class="chip">Python</span>
      <span class="chip">Matlab</span>
      <span class="chip">Automation</span>
    </div>
    <div class="placeholder-note">Placeholder for code screenshot, plot, or gif showing a tool in use.</div>
  </article>

  <article class="supporting-card">
    <h4>COVID-19 3D-Printed Devices</h4>
    <p>
      Practical devices developed using CAD, structural simulation, and FDM 3D printing to reduce hand contact with shared surfaces.
    </p>
    <div class="chip-row">
      <span class="chip">3D printing</span>
      <span class="chip">Simulation</span>
      <span class="chip">Applied engineering</span>
    </div>
    <div class="placeholder-note">Placeholder for device photos, a testing image, or a publication link.</div>
  </article>
</section>

<h2 class="section-heading">Teaching and communication</h2>

<section class="project-section">
  <article class="project-card">
    <div class="project-meta">Supporting work · Teaching</div>
    <h3>Teaching, resources, and technical communication</h3>
    <p class="project-summary">
      Teaching is part of my current work and complements my research by forcing clarity in how technical ideas are structured, explained, and shared.
    </p>
    <div class="project-details">
      <div>
        <strong>Teaching</strong>
        Composite and polymer materials, with an emphasis on clear explanation and technically grounded examples.
      </div>
      <div>
        <strong>Resources</strong>
        Tutorials, course material, and technical explanations that may be useful to students and engineers.
      </div>
      <div>
        <strong>Where next</strong>
        Visit the <a href="/teaching/">teaching and resources page</a> for the material that is already available publicly.
      </div>
    </div>
  </article>
  <aside class="media-card">
    <div class="media-frame">
      Replace this block with a tutorial gif, lecture slide crop, or a screenshot of one of your interactive resources.
    </div>
    <p class="media-caption">This section can balance the heavier research content with something more visual and accessible.</p>
  </aside>
</section>

<h2 class="section-heading">Additional work</h2>

<section class="mini-grid">
  <article class="mini-card">
    <h4>WheelRoute</h4>
    <p>Interdisciplinary startup concept related to route planning for reduced mobility users.</p>
  </article>
  <article class="mini-card">
    <h4>Rufo project</h4>
    <p>Experimental interdisciplinary project involving silk, TPU, wood, and 3D printing, later shown in Kyoto.</p>
  </article>
</section>

<h2 class="section-heading">Skills reflected across these projects</h2>

<div class="chip-row">
  <span class="chip">Composite materials</span>
  <span class="chip">Structural mechanics</span>
  <span class="chip">Aerospace structures</span>
  <span class="chip">FEA</span>
  <span class="chip">CAD</span>
  <span class="chip">Python</span>
  <span class="chip">Matlab</span>
  <span class="chip">Engineering problem-solving</span>
  <span class="chip">Technical writing</span>
  <span class="chip">Scientific communication</span>
  <span class="chip">Teaching</span>
</div>

<p style="margin-top: 1.25rem; color: var(--global-text-color-light);">
  If one of these projects later needs more depth, I can expand it into a dedicated page. For now, I prefer to keep the portfolio compact and easy to scan.
</p>
