import asyncio
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import yaml
from openai import AsyncOpenAI

from run_agent import run_agent
from tools import ToolBox
from usage import print_usage

toolbox = ToolBox()


def _repair_unescaped_quotes(s: str) -> str:
    out = []
    in_string = False
    escape = False
    i = 0
    while i < len(s):
        ch = s[i]
        if escape:
            out.append(ch)
            escape = False
            i += 1
            continue
        if ch == "\\":
            out.append(ch)
            escape = True
            i += 1
            continue
        if ch == '"':
            if not in_string:
                in_string = True
                out.append(ch)
                i += 1
                continue
            # in string: decide if this is closing or an embedded quote
            j = i + 1
            while j < len(s) and s[j].isspace():
                j += 1
            if j >= len(s) or s[j] in {",", "}", "]", ":"}:
                in_string = False
                out.append(ch)
            else:
                # likely an unescaped embedded quote
                out.append('\\"')
            i += 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def _parse_json(label: str, text: str) -> dict:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        # Simple recovery: extract the first JSON object in the text.
        start = text.find("{")
        end = text.rfind("}")
        candidate = text
        if start != -1 and end != -1 and end > start:
            candidate = text[start:end + 1]

        # Try repair for unescaped embedded quotes.
        repaired = _repair_unescaped_quotes(candidate)
        try:
            data = json.loads(repaired)
        except json.JSONDecodeError:
            print(f"ERROR: {label} did not return valid JSON.", file=sys.stderr)
            print(f"Raw output:\n{text}\n", file=sys.stderr)
            raise e
    if not isinstance(data, dict):
        raise ValueError(f"{label} JSON must be an object.")
    return data


async def main(agent_config: Path):
    client = AsyncOpenAI()
    config = yaml.safe_load(agent_config.read_text())
    agents = {agent['name']: agent for agent in config['agents']}

    usage = []
    chat_history = []


    # print("What is your website idea?")
    # idea = input(">>> ").strip()
    # if not idea:
    #     return
    idea = "paper_airplanes"

    # # 1) Designer Agent asks clarifying questions
    # print("\n-------<planning clarifying questions>-------")
    # designer_input = json.dumps({"idea": idea})
    # expander_raw = await run_agent(
    #     client, toolbox, agents['designer'],
    #     designer_input, [], usage
    # )
    # expander = _parse_json("designer", expander_raw)
    # website_idea = expander.get("website_idea", "").strip()
    # questions = expander.get("clarifying_questions", []) or []

    # # System Output asks User clarifying questions
    # clarifications = []
    # for q in questions[:5]:
    #     print(q)
    #     answer = input(">>> ").strip()
    #     clarifications.append({"question": q, "answer": answer})

    # # 2) Architect agent creates build tasks
    # print("\n-------<planning file requirements>-------")
    # architect_input = json.dumps({
    #     "idea": idea,
    #     "website_idea": website_idea,
    #     "clarifications": clarifications
    # })
    # architect_raw = await run_agent(
    #     client, toolbox, agents['architect'],
    #     architect_input, [], usage
    # )
    # architect = _parse_json("architect", architect_raw)
    # build_tasks = architect.get("build_tasks", []) or []
    # if not build_tasks:
    #     print("No build tasks returned.", file=sys.stderr)
    #     return
    
    build_tasks =  [{'file_name': 'App.tsx', 'purpose': 'Top-level React component: sets up client-side routing, global layout and provides theme/context if needed.', 'path': 'src/App.tsx', 'file_req': 'TypeScript React component. Use react-router-dom to define routes: / (Home), /tutorials (list), /tutorials/:id (tutorial detail), /print/:id (print view). Import global stylesheet. Render Header and Footer on non-print routes. Accessible navigation landmarks and skip-to-content link.'}, {'file_name': 'main.tsx', 'purpose': 'Entrypoint that mounts the React app to the DOM and wraps App with BrowserRouter.', 'path': 'src/main.tsx', 'file_req': 'TypeScript file that imports React, ReactDOM, BrowserRouter, App, and global CSS. Ensure strict typing and root element mounting compatible with Vite default index.html.'}, {'file_name': 'index.css', 'purpose': 'Global styles, pastel theme variables, typography, layout helpers and print styles.', 'path': 'src/index.css', 'file_req': 'Defines CSS variables for pastel palette, large readable fonts, spacing scale for children (8–11). Include responsive layout rules and a11y contrast checks. Add @media print rules: hide navigation/header/footer, set body background white, ensure images and SVG templates scale to page width, and set font sizes comfortable for printing. Keep class names global; comment sections for maintainability.'}, {'file_name': 'types.ts', 'purpose': 'Shared TypeScript types for tutorials and steps.', 'path': 'src/types.ts', 'file_req': "Export interfaces: Tutorial { id:string; title:string; difficulty:'easy'|'medium'|'advanced'; ageRange:string; description:string; steps: Step[]; templatePath:string; placeholderImage:string } and Step { order:number; title:string; description:string; image?:string }. Use strict typing for all fields."}, {'file_name': 'tutorials.ts', 'purpose': 'Static content store that lists the five tutorials (2 easy, 2 medium, 1 advanced) with step-by-step data and placeholder references.', 'path': 'src/data/tutorials.ts', 'file_req': "TypeScript module that exports a typed array of Tutorial objects (use types.ts). Provide 5 tutorial entries with 6–10 steps each for medium/advanced and 4–6 for easy. For images use paths into src/assets/placeholders (placeholder-1..5). Provide a templatePath pointing to SVG template files in src/assets/templates. Do not fetch external images; use local placeholders only. Include short kid-friendly descriptions and intended ageRange '8-11'."}, {'file_name': 'Header.tsx', 'purpose': 'Site header with logo/title and main navigation.', 'path': 'src/components/Header.tsx', 'file_req': "TypeScript React functional component. Show site title 'PaperAirplane Tutorials' with a small pastel mascot SVG (simple inline SVG placeholder). Provide accessible nav links to Home and Tutorials. Include a prominent 'Printable Templates' link that goes to /tutorials. Ensure keyboard focus styles and aria attributes. Mobile responsive (collapsed hamburger optional but can be simple stacked links)."}, {'file_name': 'Footer.tsx', 'purpose': 'Simple footer with copyright and a short parental note.', 'path': 'src/components/Footer.tsx', 'file_req': "TypeScript React functional component. Keep minimal text, accessible, includes link to Print view explanation. Styled to match pastel theme and fixed at bottom on large screens only; ensure it's hidden when printing via CSS."}, {'file_name': 'Home.tsx', 'purpose': 'Landing page describing the site, target age, featured tutorials and quick links.', 'path': 'src/pages/Home.tsx', 'file_req': 'React TypeScript page component. Use prominent hero with pastel background, brief copy aimed at kids and parents, and CTA buttons linking to Tutorials list and printable templates. Include 3-4 hero placeholder images (from assets) and a small gallery of featured tutorials (pull from data). Ensure semantic HTML and accessible headings.'}, {'file_name': 'TutorialList.tsx', 'purpose': 'Page that lists the five tutorials with cards grouped by difficulty and small filters.', 'path': 'src/pages/TutorialList.tsx', 'file_req': "TypeScript React page. Display tutorial cards (TutorialCard component) in a responsive grid. Group headings for 'Easy', 'Medium', and 'Advanced'. Each card shows title, difficulty badge, short description, and a thumbnail placeholder image. Provide link to detail page /tutorials/:id and a button to open printable template or print view. Implement simple client-side filter by difficulty (buttons) with accessible aria-pressed states."}, {'file_name': 'TutorialCard.tsx', 'purpose': 'Reusable card component for listing tutorials.', 'path': 'src/components/TutorialCard.tsx', 'file_req': "TypeScript React component with props for tutorial info. Present thumbnail, title, difficulty label, short description and two actions: 'View' (link to details) and 'Print Template' (link to /print/:id). Should be keyboard accessible, support alt text for images, and be responsive."}, {'file_name': 'TutorialPage.tsx', 'purpose': 'Detail page for an individual tutorial with step-by-step instructions, images, and an interactive progress checklist.', 'path': 'src/pages/TutorialPage.tsx', 'file_req': "TypeScript React page. Read tutorial id from URL params, load tutorial from data. Render title, difficulty, printable template preview, and a list of Step components in order. Include a Checklist component (per-step checkbox) that persists completion state in localStorage (keyed by tutorial id). Provide controls: 'Mark all complete', 'Reset', 'Print Instructions' that navigates to /print/:id or triggers window.print() for a print-friendly modal. Ensure large tap targets and accessible labels on checkboxes."}, {'file_name': 'Step.tsx', 'purpose': 'Component to render an individual step: step number, image placeholder, short instruction text and a checkbox control.', 'path': 'src/components/Step.tsx', 'file_req': 'TypeScript React component. Accepts Step data, and a checked boolean plus onToggle callback. Show clear step number badge, image with alt text, large readable instruction copy. Checkbox should be large and touch-friendly. Use CSS to ensure step layout stacks on small screens and shows image + text side-by-side on wider screens.'}, {'file_name': 'Checklist.tsx', 'purpose': 'Manages and displays the per-tutorial checklist and localStorage persistence.', 'path': 'src/components/Checklist.tsx', 'file_req': 'TypeScript React component. Accept props: tutorialId and numberOfSteps (or steps array). Use a custom hook useLocalStorage to persist an array/Set of completed step indexes. Expose functions to mark all, reset, and toggle single step. Optionally animate a simple confetti-style CSS flourish when all steps completed (pure CSS/JS small effect).'}, {'file_name': 'PrintView.tsx', 'purpose': "Print-optimized page that renders a tutorial's instructions and the full-size printable template ready for physical printing.", 'path': 'src/pages/PrintView.tsx', 'file_req': 'TypeScript React page component used at route /print/:id. Render tutorial title, ordered steps (image placeholders and concise text), and the template SVG at full width. Apply print-only styles (margin, page-breaks if needed) so when users invoke browser print dialog the output is formatted as a simple, single-column printable sheet. Hide navigation and interactive controls when printing.'}, {'file_name': 'useLocalStorage.ts', 'purpose': 'Custom hook to abstract localStorage get/set logic with JSON typing and SSR safety checks.', 'path': 'src/hooks/useLocalStorage.ts', 'file_req': 'TypeScript hook that accepts a key and initial value. Returns [value, setValue] with types inferred. Safely check for window availability, serialize/deserialize JSON, and handle parsing errors. Use this in Checklist to persist progress.'}, {'file_name': 'assets: placeholder images', 'purpose': 'Local placeholder images used for step illustrations and thumbnails.', 'path': 'src/assets/placeholders/placeholder-1.png', 'file_req': "Create 5 placeholder PNGs (placeholder-1.png ... placeholder-5.png). They can be simple colored rectangles or exported from a design tool, sized ~1200x800 for step images and also usable as thumbnails. Include brief filenames and ensure each has an associated alt text in components. If actual image files aren't created in this task, include clear placeholder filenames referenced by data/tutorials.ts."}, {'file_name': 'assets: SVG templates', 'purpose': 'Printable plane templates (one per tutorial) in vector format so parents/kids can print and fold.', 'path': 'src/assets/templates/template-easy-1.svg', 'file_req': 'Provide one SVG file per tutorial e.g. template-easy-1.svg, template-easy-2.svg, template-medium-1.svg, template-medium-2.svg, template-advanced-1.svg. Each SVG should be a simple outline of a paper sheet with fold lines indicated (placeholder SVG content is fine). Ensure they scale to 100% width when printed, have white background and include title text as fallback.'}, {'file_name': 'utils/printHelpers.ts', 'purpose': 'Small helper functions to create print-friendly URLs and programmatically trigger print with a timeout (for single-page prints).', 'path': 'src/utils/printHelpers.ts', 'file_req': 'TypeScript functions: getPrintUrl(tutorialId:string) returning `/print/${tutorialId}` and a printWithDelay() helper that focuses the print area before calling window.print() with a small delay. Keep minimal and document usage.'}, {'file_name': 'README.md', 'purpose': "Developer notes and run instructions specific to this children's tutorial site.", 'path': 'README.md', 'file_req': 'Short markdown file describing project structure, how to run dev server (npm run dev), build (npm run build), where to add real images/templates, and notes about accessibility, printing and persisting checklist state.'}]

    # 5) Build agent runs once per task
    print(f"\n-------<executing build tasks: {build_tasks}>-------")
    async def _run_build_task(task):
        task_json = json.dumps(task)
        bulid_raw = await run_agent(
            client, toolbox, agents['builder'],
            task_json, [], usage
        )
        return {"result": bulid_raw, "path": task["path"]}

    build_results = await asyncio.gather(
        *[_run_build_task(task) for task in build_tasks]
    )


    for result in build_results:
        print(result)
        path = "output/prototyper_results/"+ idea + "/" + result["path"]
        os.makedirs(os.path.dirname(path), exist_ok=True)  # Create directories if they don't exist
        print(path)
        with open(path, "w") as file:
            file.write(result["result"])



    # # 6) Synthesizer agent produces final report
    # print("\n-------<generating report>-------")
    # synth_input = json.dumps({
    #     "topic": topic,
    #     "topic_summary": topic_summary,
    #     "clarifications": clarifications,
    #     "search_summaries": search_summaries
    # })
    # report = await run_agent(
    #     client, toolbox, agents['synthesizer'],
    #     synth_input, [], usage
    # )

    # print("\n" + report + "\n")
    print_usage(agents['chat']['model'], usage)


if __name__ == '__main__':
    load_dotenv()
    config_file = sys.argv[1] if len(sys.argv) > 1 else 'frontend_prototyper.yaml'
    asyncio.run(main(Path(config_file)))
