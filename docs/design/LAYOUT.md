# Layout and style reference

Screenshots are in this folder (live site, full mockup, older mockup). The text below is
the authoritative description, since the coding model can't see images.

## Global style
- Clean corporate look, lots of white space, sans-serif (Arial/Helvetica/system), bold headings.
- Primary blue about #1565C0 for buttons, card headers, bars, links and the active nav item.
  Text #222, body grey #555, panels #f5f5f5, white background.
- Logo: text "V2R" (V blue, "2R" black, large bold) with a small "Virtual to Reality"
  caption beneath. Build it in HTML/CSS. TODO: real logo asset.
- Buttons: rectangular, almost no radius, small bold text. Primary = solid blue with white
  text, secondary = white with blue text, dark = near-black with white text.
- Circular icon buttons (about 28-30px): search = blue, LinkedIn = dark blue, WhatsApp = green.
- Content container max-width about 1100-1200px, centered.

## Header (wide, 900px and up)
- White, with a thick blue line (4-5px) along the bottom.
- Left: logo. Center: bold black "Project Management & Support Services" (about 28px)
  with the nav links in a row beneath (small, grey, active = blue): Home, About, Services,
  Who We Serve, Areas of Experience, Contact Us.
- Right: tagline "provide remote virtual team support work from anywhere" (small document
  icon at left, thin blue underline), then the three circle icons below it.

## Header (narrow)
- Logo left, small menu button right. The nav, tagline and icons live in a right-side
  slide-in panel (see AGENTS.md).

## Hero
- Full-width dark-overlaid photo (man leaping across a gap in a broken bridge, desaturated),
  about 450-500px tall.
- Centered white bold text (about 34px, `clamp()` on small screens), 2 lines:
  "We provide project management, engineering, and support services to the infrastructure sector"
  (SiteText `hero.title`).
- Two buttons: "Our Services" (solid blue) and "Areas of Expertise" (white), both anchor-scroll.
- 4 small dots below (first active). Simplest option: static dots, or a vanilla crossfade.
- White circle badge with a blue down-arrow at the bottom center, overlapping the hero edge.

## Services section (#services)
- Centered bold heading "We Offer Services in The Following Areas".
- 3-column grid of 6 cards (2 rows), equal height. Each card has a 1px blue border and a
  solid blue header bar with a white UPPERCASE bold title and a small downward triangle
  notch beneath it. The body has a bold uppercase subheading and a bulleted list
  (small grey text, small blue/orange bullets).
- Centered blue "View All" button below (TODO link).

Cards (title | subheading | items):
- Project Management Systems | Project Management Systems | PM System Development; Project Controls Systems; System Maturity Models; Project Procedures; Consultation/Advisory
- Front End Project Development | Project Structuring & Scope Definition | Project Brief; Concept Designs; FEED Support; Tender Document Review; Tender Process Support; Alternative Design & Solutions
- Project Planning & Analysis | Detailed Planning | Programs & Planning; Resource Scheduling; Value Engineering; Option Analysis; Risk Assessments; Alternative Solutions; Execution Strategies
- Project Deliverables | Execution Phase Level of Detail | Execution Strategy; Detailed Design; Methods of Work; Sequences of Work; Temporary Works
- Review Services | Conduct Reviews & Report | Tender Documents; Technical Reviews; Contract Reviews; Bid / Tender Reviews; Design Reviews; Constructability; Overflow Work
- Other Support Services | Detailed Planning | Visualization (2D/3D); Engineering Support; Independent Assessment; Claim Prevention Strategies; 3D+ Visualization Claim Support

## About
- Full-width blurred office photo (smiling woman at right) with a dark overlay.
- Centered white: "About V2R" (bold, about 28px), paragraph (SiteText `about.body`), blue "Learn More" button.

## Areas of Experience (#experience)
- Same card style and 3-column grid. The second row has 2 cards, left-aligned at the same
  column widths. Centered "View All" button below.

Cards (title | items):
- Key Project Types | Port & Harbor Works; Jetties & Wharves; Pipelines - Land & Marine; Tender Document Review; Breakwaters - Coastal Protection; Temporary Works
- Project Phases | Project Development; Front End Studies; Budgets & Estimates; Tendering & Proposals; Design & Engineering; Pre-Construction; Project Start Ups; Project monitoring & controls; Package Management
- Process Experience | Scope Management; Requirements Management; Time - planning; Resource Management; Cost Management; Engineering Management; Production Management; Project Controls; Risk Management; Change Management; Issue Management; Value Engineering; Process Maturity Studies; Peer Review Process; Quality Management; HSE Management; Claims Management
- Activity Based - Civil | Site Conditions - Survey; Geotechnical Investigation; Steel Piling Works; Concrete Piling - bored cast insitu; Sheet Piled Structures; Combi-Wall Structures; Precast Concrete Works; Temporary Works; Earthworks; Ground Improvement; Reinforced Concrete Works; Marine Cofferdams; Land Based Cofferdams
- Activity Based - Marine/Pipelines | Bridge Works; Breakwaters & Revetments; Marina Works; Marine Pipeline Works; Land Based Pipelines; HDPE Pipeline; GRP Pipeline; Carbon steel Pipeline; Building Works
(TODO: client to confirm the two "Activity Based" titles.)

## Who We Serve (#who)
- Heading, short intro (SiteText `who.intro`), simple list of 3-4 client types (dummy, TODO).

## Our Recent Work
- Left-aligned heading "Our Recent Work", blue "View All Projects" button on the right.
- Mosaic: left, a 2x2 grid of 4 square image tiles. Right, one large tile spanning 2 rows.
  Each tile has a solid blue label bar at the bottom with white "Project Name" text.
  Images come from `static/img/work/` (I'll add them).

## What Our Clients Say
- Centered heading. Row of 3 testimonial cards: side cards light grey with muted text,
  the center/active card solid blue with white text, slightly larger or raised.
- Each card: small avatar top-left (placeholder circle), bold name and "Customer" beside it,
  quote text below, dark circular quote-mark button at the bottom center.
- Pagination dots below. Only `is_published=True` reviews are shown.
- Mobile: 1 card at a time. Degrade gracefully with 0-2 reviews. "Write a review" link below.

## Careers band
- Full-width split. Left 50%: photo of people working around a table. Right 50%: solid blue
  panel with white text: "Careers at V2R", paragraph (SiteText `careers.body`), two dark
  buttons "Life At V2R" and "Current Positions" (TODO links).
- Mobile: stacked, photo on top.

## Contact Us (#contact)
- Simple section above the footer: small contact form (ContactMessage) plus the details
  from SiteText (address, phone, email). Rough first, to be beautified later.

## Footer
- White background. Columns side by side on desktop, stacked on mobile.
  1. Logo, then circular LinkedIn (dark blue) and WhatsApp (green) icons.
  2. QUICK LINKS (bold, uppercase): chevron-prefixed list: Home, About, Services,
     Who We Serve, Areas of Experience, Contact Us, Terms & Conditions, Privacy Policy.
  3. CONTACT US (bold, uppercase): house icon + address, phone icon + phone,
     envelope icon + email.
  4. Work hours: "Monday to Friday: 9 am - 5pm", "Saturday & Sunday: Closed"
     (SiteText `footer.work_hours`).
- Full-width thin blue bar, white centered text: "Copyright © <current year> V2R All
  Rights Reserved." (V2R bold).
- Small blue circular "back to top" up-arrow button at the bottom.

## Responsive summary
- Cards: 3 columns on desktop, 2 on tablet, 1 on mobile.
- Mosaic: 2 columns, with the featured tile full width.
- Careers and footer: stacked.
- One breakpoint at 900px for the header and menu behavior, about 600px for grid collapse.