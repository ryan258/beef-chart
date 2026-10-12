# Atlas artwork, prompts, and verification

## Current asset inventory

All 24 catalog cuts have transparent 1024 × 1024 WebP illustrations, connected by `CUT_IMAGE_MAP` in `index.html`. The set serves the cut dossiers, six popular cards, and four specialty cards. The cow hero and pasture are opaque halftone illustrations; interactive cow maps are native SVG with cut-paper geometry. Raster prompts and the separate SVG design record follow below.

There are 27 cut WebP files because three filename pairs intentionally share pixels: `cut_chuck.webp` / `cut_aguja.webp`, `cut_nystrip.webp` / `cut_bife_chorizo.webp`, and `cut_sirloin.webp` / `cut_cuadril.webp`. Card and dossier references retain those aliases. The redrawn ribeye is distinct from sirloin. `favicon.svg` and `favicon-32.png` reuse the header cow motif. `vintage_barn.webp` is not referenced by the page and remains a reserved older asset.

| Cut ID | Dossier asset |
|---|---|
| `bife-ancho` | [`cut_ribeye.webp`](../assets/cut_ribeye.webp) |
| `bife-angosto` | [`cut_bife_chorizo.webp`](../assets/cut_bife_chorizo.webp) |
| `aguja` | [`cut_aguja.webp`](../assets/cut_aguja.webp) |
| `vacio` | [`cut_vacio.webp`](../assets/cut_vacio.webp) |
| `entrana` | [`cut_entrana.webp`](../assets/cut_entrana.webp) |
| `matambre` | [`cut_matambre.webp`](../assets/cut_matambre.webp) |
| `costillar` | [`cut_asado_tira.webp`](../assets/cut_asado_tira.webp) |
| `cuadril` | [`cut_cuadril.webp`](../assets/cut_cuadril.webp) |
| `peceto` | [`cut_peceto.webp`](../assets/cut_peceto.webp) |
| `nalga` | [`cut_nalga.webp`](../assets/cut_nalga.webp) |
| `bife-costilla` | [`cut_bife_costilla.webp`](../assets/cut_bife_costilla.webp) |
| `molleja` | [`cut_molleja.webp`](../assets/cut_molleja.webp) |
| `rinon` | [`cut_rinon.webp`](../assets/cut_rinon.webp) |
| `lengua` | [`cut_lengua.webp`](../assets/cut_lengua.webp) |
| `pecho` | [`cut_brisket.webp`](../assets/cut_brisket.webp) |
| `lomo` | [`cut_tenderloin.webp`](../assets/cut_tenderloin.webp) |
| `paleta` | [`cut_paleta.webp`](../assets/cut_paleta.webp) |
| `colita` | [`cut_colita_cuadril.webp`](../assets/cut_colita_cuadril.webp) |
| `tapa` | [`cut_tapa_cuadril.webp`](../assets/cut_tapa_cuadril.webp) |
| `brazuelo` | [`cut_brazuelo.webp`](../assets/cut_brazuelo.webp) |
| `garron` | [`cut_garron.webp`](../assets/cut_garron.webp) |
| `cogote` | [`cut_cogote.webp`](../assets/cut_cogote.webp) |
| `bola` | [`cut_bola_lomo.webp`](../assets/cut_bola_lomo.webp) |
| `cuadrada` | [`cut_cuadrada.webp`](../assets/cut_cuadrada.webp) |

The earliest 14-cut illustration pass preceded the retained prompts below; its exact prompts are not reconstructed here. This record describes generation inputs and implementation evidence, not a completed rights manifest or specialist anatomical sign-off. Earlier statements that HTML/CSS were unchanged apply only to the named image-replacement round; later rounds changed integration, layout, and diagram code.

## Tenderloin and brisket replacement round

Generated October 12, 2026 using the built-in image-generation tool. These replace the previous photos at `assets/cut_tenderloin.webp` and `assets/cut_brisket.webp`. Both retain transparent backgrounds and are encoded as 1024 × 1024 WebP using cwebp (quality 90, alpha quality 100).

The original photos supplied the subject and composition. Existing `assets/cut_nystrip.webp` and `assets/cut_chuck.webp` supplied the illustration style. Existing card references and `CUT_IMAGE_MAP` entries use the same replacement files.

These are stylized illustrations, not reviewed anatomical specifications.

## Display verification

Local Chrome checks on October 12, 2026 confirmed both assets decode at 1024 × 1024, preserve transparent backgrounds, and appear in their existing popular cards and dossiers. Desktop checks used a 1280px viewport; narrow card checks used 390px and 320px viewports; both dossiers were visually checked at 320px. The images fit their containers without clipping or horizontal overflow. HTML and CSS were unchanged in this two-image replacement round. This was local browser verification, not real-device or assistive-technology acceptance.

## Tenderloin prompt

Use case: style-transfer.
Asset type: transparent cut illustration for the Beef Chart website's small cards and dossier banner.
Input image 1 (cut_tenderloin.webp) is the edit target and subject/composition reference. Input images 2 and 3 (cut_nystrip.webp and cut_chuck.webp) are the exact existing illustration style references.
Replace the tenderloin photograph with a drawn illustration of the SAME single raw beef tenderloin medallion, preserving its thick compact cylindrical shape and three-quarter view, oval top face and visible side. Match the references' vintage pop-art halftone lithograph/comic screentone technique: bold near-black ink contours, confident irregular black hatching, terracotta brick-red ink areas, clearly visible dense regular halftone dot patterns, warm creamy sparse fat/marbling highlights, subtle printed-ink character. The tenderloin should remain mostly lean with sparse fine marbling, no thick strip-steak fat cap.
Square 1024x1024 composition, entire cut centered, approximately 82% of canvas width and height with comfortable transparent margins; clean strong silhouette readable at 90px high. Flat limited ink palette like the references. No photographic shading, no photorealistic texture or glossy rendering, no gradients, no text, no labels, no plate, no garnish, no drop shadow. Truly transparent background outside the cut, preserve opaque cream highlights inside it. Output only the single tenderloin medallion illustration.

## Brisket prompt

Use case: style-transfer.
Asset type: transparent cut illustration for the Beef Chart website's small cards and dossier banner.
Input image 1 (cut_brisket.webp) is the edit target and subject/composition reference. Input images 2 and 3 (cut_nystrip.webp and cut_chuck.webp) are the exact existing illustration style references.
Replace the brisket photograph with a drawn illustration of the SAME single raw beef brisket slab, preserving its broad elongated tapered wedge shape, three-quarter view, long parallel coarse muscle grain and creamy fat cap. Match the references' vintage pop-art halftone lithograph/comic screentone technique: bold near-black ink contours, confident irregular black hatching emphasizing the long grain, terracotta brick-red ink areas, clearly visible dense regular halftone dot patterns, warm creamy fat accents, subtle printed-ink character. Keep a recognizable broad lean cut face with coarse lengthwise grain and one fat cap; no ribeye-like round muscle clusters.
Square 1024x1024 composition, entire cut centered, approximately 86% of canvas width, with balanced transparent margins; strong silhouette readable at 90px high. Flat limited ink palette like the references. No photographic shading, no photorealistic texture or glossy rendering, no gradients, no text, no labels, no plate, no garnish, no drop shadow. Truly transparent background outside the cut, preserve opaque cream highlights inside it. Output only the single brisket illustration.

## Remaining eight cuts — October 12, 2026

Created with the built-in image-generation tool using `assets/cut_nystrip.webp` and `assets/cut_chuck.webp` as style references. The shared prompt below was followed by the individual subject prompt for each image. Each final asset is a transparent 1024 × 1024 WebP, encoded with cwebp at quality 90 and alpha quality 100.

Catalog labels were cross-checked against the [SENASA beef-cut nomenclator](https://www.argentina.gob.ar/normativa/nacional/norma-60581/texto). The [IPCVA cut catalog](https://ipcva.agrositio.com/nomenclador2015/buscador.php) was also consulted. Whole-roast and shank presentations are illustrative choices rather than reviewed purchase specifications or visual proof of anatomical equivalence. Brazuelo is shown cross-cut with marrow, matching the existing dossier description; Garrón is shown as an elongated shank portion.

| Dossier ID | Cut | Asset |
| --- | --- | --- |
| `paleta` | Paleta | `assets/cut_paleta.webp` |
| `colita` | Colita de cuadril | `assets/cut_colita_cuadril.webp` |
| `tapa` | Tapa de cuadril | `assets/cut_tapa_cuadril.webp` |
| `brazuelo` | Brazuelo | `assets/cut_brazuelo.webp` |
| `garron` | Garrón | `assets/cut_garron.webp` |
| `cogote` | Cogote | `assets/cut_cogote.webp` |
| `bola` | Bola de lomo | `assets/cut_bola_lomo.webp` |
| `cuadrada` | Cuadrada | `assets/cut_cuadrada.webp` |

### Integration and verification

All 24 catalog cuts now have existing assets in `CUT_IMAGE_MAP`. The eight new files were checked for 1024 × 1024 dimensions, RGBA encoding, transparent exterior, and transparent corners. Inline JavaScript syntax and catalog-to-asset coverage checks passed.

Each of the eight new dossiers was opened through its directory button in local Chrome at 1280 × 900, 390 × 844, and 320 × 740. All 24 final viewport/cut combinations passed checks for the correct image and title, successful decoding, visible and contained artwork, title placement below the image, and absence of horizontal overflow. Representative desktop and mobile screenshots were visually inspected. No browser console errors or warnings were reported.

The 320px visual check exposed an existing overlap between the primal caption and close button. A `cut-dossier-heading` class now allows the header to wrap and reserves 52px for the close control. The final checks also confirmed that the header text stays clear of the close button. This is local browser emulation evidence; physical-device and assistive-technology behavior were not evaluated in this artwork task.

### Shared prompt

Use case: style-transfer.
Asset type: single transparent beef-cut illustration for the Beef Chart dossier banner.
The supplied cut_nystrip.webp and cut_chuck.webp images are STYLE REFERENCES ONLY. Create a different cut with the subject specified below, faithfully matching this existing illustration set.
Style: vintage pop-art halftone lithograph, comic-book screentone dot pattern, bold near-black irregular ink contour linework, short black hatching and cross-hatching, muted terracotta brick-red ink fields, warm creamy fat and connective-tissue accents. Dense visible regular dot pattern, flat limited print palette, subtle ink imperfections. Match the reference line weights, warmth and printed texture.
Composition: square 1024x1024, one isolated whole cut centered, entire silhouette visible with at least 8% clear margins on each edge; approximately 80–84% of the frame on its longest axis. Three-quarter view and clear readable silhouette at 160px display height.
Background: genuinely transparent alpha outside the cut; opaque cream highlights inside it. No opaque background rectangle, checkerboard drawing, drop shadow, plate, board, garnish, text, labels, border, logos or watermark. No photorealism, glossy rendering, gradients, cooking, or browned meat.

### Individual subject prompts

#### Paleta

One raw boneless beef shoulder-clod roast (Argentine paleta). A thick elongated, slightly triangular irregular shoulder roast, broader rounded heel at one end and gently tapering at the other; visible lean muscle lobes divided by just a few thin cream connective-tissue seams, modest surface fat. Show the whole clod portion in three-quarter view, a broad red face and one thick side. No bone, no butcher twine, no sliced flat-iron steak.

#### Colita de cuadril

One whole raw boneless beef tri-tip roast (Argentine colita de cuadril). A distinctive long triangular crescent/boomerang wedge with a thick broad rounded heel and a pronounced tapered pointed tail; lean exposed muscle, subtle two-direction muscle grain, a narrow cream fat seam along one edge only. Three-quarter view. The triangular silhouette is essential. No heavy fat cap, no bone, no slices.

#### Tapa de cuadril

One whole raw boneless beef rump-cap roast (tapa de cuadril, picanha/coulotte). A broad compact triangular wedge with a rounded broad heel and pointed end. Its defining feature is a continuous thick creamy fat cap across the upper surface, with a substantial terracotta lean-meat side/cut face visible below the cap in three-quarter view. Keep the fat cap unscored. No grill marks, no skewers, no bone, no slices.

#### Brazuelo

One raw bone-in fore-shank cross-cut slice (Argentine brazuelo prepared as osso buco). A compact irregular oval thick disk with a clearly visible small near-central cream bone ring containing pale marrow, surrounded by several lean terracotta muscle groups separated by thin cream tendon/connective tissue lines. Three-quarter view shows the cut top and thickness of the side. The marrow bone must be surrounded by meat and not resemble a large hole. No garnish, no second slice.

#### Garrón

One raw bone-in hind-shank portion (Argentine garrón), presented as an elongated whole shank section, not a round osso-buco slice. A tapered substantial muscle bundle wrapped around a lengthwise shin bone; one neatly sawn short exposed pale bone end with marrow, long sinewy muscle grain, several cream connective-tissue seams, very little outer fat. Three-quarter oblique view with the long axis angled across the square frame, whole piece comfortably in view. No hoof, no skin, no cooked meat, no detached bones.

#### Cogote

One raw boneless beef neck roast (Argentine cogote). A squat, roughly oblong, irregular multi-muscle block with visibly interlocking small muscle bundles, varied grain direction, abundant cream connective-tissue seams between bundles and modest marbling. Three-quarter view shows the uneven cut face and thick side. A neck-muscle roast, not a round ribeye or tenderloin medallion. No bone, no head, no butcher twine, no loose cubes.

#### Bola de lomo

One whole raw boneless beef knuckle roast (Argentine bola de lomo, sirloin-tip/knuckle context). A compact plump rounded oval multi-lobed roast with three or four broad lean muscle lobes and delicate cream seams between them; very little marbling or external fat, subtle silverskin accents. Three-quarter view, largely terracotta red. Its rounded whole-roast silhouette is essential. Not a cylindrical tenderloin medallion, not an eye-round log, no bone or twine, no slices.

#### Cuadrada

One whole raw boneless outside-round flat roast (Argentine cuadrada/carnaza de cola). An elongated broad flattened rectangular-to-trapezoid muscle slab with gently rounded corners, thicker at one end and tapering slightly at the other. Show uniform lean terracotta muscle with long parallel grain and sparse fine cream connective lines; only a very thin light membrane along one edge. Three-quarter view with a broad top surface and low sidewall. No thick fat cap, no circular steak shape, no eye-round cylinder, no bone, no slices.
## Ribeye and sirloin redraw; cow favicon — 2026-10-12

Generated with the built-in image generation tool and genuine transparent alpha. Style references: `assets/cut_tenderloin.webp` and `assets/cut_brisket.webp`. Original PNGs were converted with cwebp to 1024 × 1024 WebP at quality 90 and alpha quality 100.

- Ribeye: `assets/cut_ribeye.webp` serves both the popular card and Bife ancho dossier.
- Sirloin: `assets/cut_sirloin.webp` serves the popular card; the identical `assets/cut_cuadril.webp` serves the Cuadril dossier.
- Favicon: `assets/favicon.svg` reuses the header cow path, centered on a rounded cream square. `assets/favicon-32.png` is the browser-rendered 32 px fallback. Both are declared in the page head. The favicon was created from the existing SVG, without image generation.

### Ribeye final prompt

Use case: scientific-educational. Asset type: transparent cut illustration for a beef atlas card and dossier. The provided tenderloin and brisket images are STYLE REFERENCES ONLY. Match their vintage comic-book halftone lithograph style: bold clean near-black ink contours, fine directional hand hatching and dense deliberate screentone dots, muted terracotta-red flesh, warm cream fat, richly illustrated but readable at small size, no photographic texture. Square 1024x1024 composition. One raw boneless beef cut in a slightly elevated three-quarter view, centered with at least 10% transparent padding on all sides, full silhouette and visible thickness. True transparent alpha background, crisp antialiased edges, no white or grey matte, no shadow outside the silhouette, no plate, board, tools, garnishes, labels, lettering, or frame. Keep the meat primarily terracotta red; cream is limited to believable fat seams and marbling. Subject: a recognizably boneless RIBEYE STEAK, medium-thick and broadly rounded oval, horizontal orientation. Show a large central oval muscle eye, a distinct narrow crescent-shaped outer cap curving around the upper-left perimeter, and a clean curved warm-cream fat seam separating that cap from the eye. Fine branching cream marbling within the red central eye, not huge cream patches. Outer outline rounded and organic with a short tapered tail. Visible front edge about one-quarter the height of the top face. This must read as a steak slice, not a round cylindrical tenderloin medallion or a rectangular brisket roast. Freshly cut, uncooked.

### Sirloin final prompt

Use case: scientific-educational. Asset type: transparent cut illustration for a beef atlas card and dossier. The provided tenderloin and brisket images are STYLE REFERENCES ONLY. Match their vintage comic-book halftone lithograph style: bold clean near-black ink contours, fine directional hand hatching and dense deliberate screentone dots, muted terracotta-red flesh, warm cream fat, richly illustrated but readable at small size, no photographic texture. Square 1024x1024 composition. One raw boneless beef cut in a slightly elevated three-quarter view, centered with at least 10% transparent padding on all sides, full silhouette and visible thickness. True transparent alpha background, crisp antialiased edges, no white or grey matte, no shadow outside the silhouette, no plate, board, tools, garnishes, labels, lettering, or frame. Keep the meat primarily terracotta red; cream is limited to believable fat seams and marbling. Subject: a recognizably boneless TOP SIRLOIN / CUADRIL STEAK, a wide asymmetrical triangular-trapezoidal steak slice, broader at the left and subtly tapering toward a rounded right end, with a gently angular outline and broad relatively lean single red muscle face. A restrained thin cream fat strip only along one upper outer edge, subtle sparse marbling and fine directional muscle grain. NO circular central eye, NO crescent cap wrapping the perimeter, NO concentric fat seam: its anatomy and silhouette must be visually distinct from ribeye. Visible front edge about one-fifth the height of the top face. Not a whole triangular picanha roast; no thick white fat cap. Freshly cut, uncooked.
### Redraw verification

- Both cards opened their correct dossiers at 1280 × 900 desktop, 390 × 844 mobile, and 320 × 740 narrow-mobile viewports. All six cut/viewport checks passed: expected source and title, decoded 1024 px artwork, contain sizing, image within its card/hero and viewport, title below image, header clear of close control, and no horizontal overflow.
- Visually inspected both desktop dossiers, both 390 px mobile dossiers, the desktop card grid, and both affected cards at 320 px. Distinct silhouettes and transparent backgrounds display correctly.
- Both favicon declarations returned HTTP 200 with the expected image MIME types and decoded successfully; the PNG is 32 × 32. The existing cow silhouette is visible in the small icon.
- All three installed WebPs retain alpha 0–255 with transparent corners. Sirloin and Cuadril files are byte-identical; ribeye differs.
- No browser console errors or warnings were reported. `git diff --check` passed. No full test suite was run for this asset/head-metadata update.
- Checked in local Chromium desktop/mobile emulation, not on physical phones. Refreshed the existing in-app preview after restarting the local snapshot server.
## Cow hero and pasture scene — 2026-10-12

Created with the built-in image generation tool as opaque illustrations. For each call, the original photograph at the destination path was the subject/composition reference and `assets/cut_ribeye.webp` was the style reference. Each final asset is a 1024 × 1024 RGB WebP encoded with cwebp at quality 90.

- `assets/hero_cow.webp`: front-facing white-faced cow with terracotta coat and disk backdrop, cream highlights, black contours, hatching and halftone shading.
- `assets/pasture_fence.webp`: receding wooden pasture fence, fields, distant farm buildings and clouds in the same ink palette.
- Removed grayscale display filters; removed the pasture's faded treatment so its colors and ink remain visible. Added 4% inner space to the cow image so both horns fit the circular frame.
- Updated both image descriptions. On screens up to 800 px wide, reserved space below the quote for the pasture and used a responsive quote font size so the illustration does not overlap text or clip the final word. The existing partial circular pasture crop is intentional.

### Cow hero final prompt

Use case: style-transfer. Recreate the first reference image as a hand-drawn vintage pop-art halftone lithograph, matching the second reference image's style and palette ONLY. Bold near-black ink contour lines, fine directional hatching, crisp deliberate comic-book screentone dots, muted terracotta brick-red ink and warm cream highlights. Clearly an illustration, not a photograph run through a dot filter. Strong simplified shapes readable at small display sizes, with richer ink detail at full size. Limited flat ink palette, no smooth photographic shading or glossy rendering. Square 1024x1024 artwork, opaque background, no text, labels, lettering, watermark, border or frame. Asset type: homepage cow hero portrait, displayed inside a circular crop. Subject/composition reference is the existing cow photo: one calm front-facing horned white-faced Hereford-type cow, centered face and shoulders, dark eyes, broad muzzle, curly forelock, ears extending sideways, short outward-curving horns. Preserve its welcoming symmetrical portrait and recognizable facial structure. Use cream for the white face, terracotta for the brown coat, near-black shadows and contours. Draw curls and fur as confident engraved hatch marks and controlled dot shading, not individual photographic hairs. Keep both eyes, ears, muzzle and both horn tips safely INSIDE a central circular crop, with roughly 10% safe space at the left and right. Shoulders can extend off the lower edge. Background: a simple large flat terracotta-red disk behind the cow, warm cream outside that disk; no photographic grunge. Strong clean contrast between cream face, black details and terracotta surroundings.

### Pasture scene final prompt

Use case: style-transfer. Recreate the first reference image as a hand-drawn vintage pop-art halftone lithograph, matching the second reference image's style and palette ONLY. Bold near-black ink contour lines, fine directional hatching, crisp deliberate comic-book screentone dots, muted terracotta brick-red ink and warm cream highlights. Clearly an illustration, not a photograph run through a dot filter. Strong simplified shapes readable at small display sizes, with richer ink detail at full size. Limited flat ink palette, no smooth photographic shading or glossy rendering. Square 1024x1024 artwork, opaque background, no text, labels, lettering, watermark, border or frame. Asset type: pastoral editorial scene in a small circular accent on the website. Preserve the existing pasture photo's composition: a rustic wooden post-and-wire fence recedes diagonally from the lower-right foreground toward the upper-center-left distance through an open grassy field, a low tree line and small distant barn/farm buildings near the horizon, with open sky and a few clouds above. Use warm cream sky and highlights, terracotta field and barn accents, and near-black contours, cross-hatching and halftone dots. Translate grass into bold deliberate etched strokes and restrained screentone textures, not photographic detail. Make the closest wooden fence post and receding fence line especially clear and recognizable. Keep enough sky for breathing room and a quiet pastoral mood. No people, no animals, no extra props, no new text or decorative symbols.

### Hero and pasture verification

Verified at 1280 × 900 desktop, 390 × 844 mobile, and 320 × 740 narrow mobile. Both images decode at 1024 px with grayscale filters disabled and full opacity. The cow's circular container fits its panel, the visible pasture crop remains recognizable, every quote line fits, quote text is separated from the image, and there is no page horizontal overflow. Visually inspected both image placements at all three sizes. The quote-to-image gap is 65 px at both mobile widths and 112 px on desktop. No browser console errors or warnings were reported. `git diff --check` passed. Checks used local Chromium emulation, not physical devices.
## Interactive cow diagrams: cut-paper redesign — 2026-10-12

Redrew the existing native SVG maps in a Saul Bass-inspired cut-paper style. No raster generation was used: the regions remain interactive SVG paths.

- Angular shared cow silhouette with a horn, eye, offset far legs and a kinked tail; irregular regional polygons and wider cream seams replace fine white/dashed dividers.
- Retail map uses terracotta, oxblood, ochre and tan; U.S. map uses navy, muted blue and ochre. Display inks are separate from the market charts' existing data colors.
- Hatched overlays identify lomo, entraña and peceto. The map note explains that these are layered references. The shapes are an educational interpretation, not cutting or purchasing specifications.
- The U.S. map has permanent region labels. Both maps have country captions, region counts and a full-name readout on hover or keyboard focus. Both maps highlight related regions together.
- Twenty retail regions and nine U.S. region controls remain available, including the compound two-leg shank region. The existing full-name directory remains available for small targets.
- Stacked layouts through 800 px keep each map at the available column width.

### Anatomical reference pass

Used the [USDA Fresh Beef IMPS, primal diagram and cut descriptions](https://www.ams.usda.gov/sites/default/files/media/IMPS_100_Fresh_Beef%5B1%5D.pdf#page=25) for broad regional ordering, and IPCVA's Argentine nomenclature for the [forequarter](https://ipcva.agrositio.com/nomenclador2015/cortes.php?categoria_id=5) and [hindquarter](https://ipcva.agrositio.com/nomenclador2015/cortes.php?categoria_id=6). The overlay placement uses the descriptions of [lomo in the sublumbar region](https://ipcva.agrositio.com/nomenclador2015/cortes-detalle.php?categoria_id=6&corte_id=57), [entraña at the diaphragm's costal attachments](https://ipcva.agrositio.com/nomenclador2015/cortes-detalle.php?categoria_id=6&corte_id=91), and [peceto in the rear thigh](https://ipcva.agrositio.com/nomenclador2015/cortes-detalle.php?categoria_id=6&corte_id=80). The 2D polygons remain schematic and do not establish exact fabrication boundaries or translated equivalence.

### Diagram verification

- At 1280 × 900 and 320 × 740, all 29 regions had an exposed pointer-hit location found with SVG fill testing plus browser elementFromPoint. A synthetic click event on each region opened the expected dossier; this was browser integration testing, not a physical pointer/device test.
- All 29 regions at both sizes passed Enter/Space handler checks, button-role/tabindex checks and focus-name readout checks.
- A native browser Enter key opened Lomo, and Escape closed it and returned focus to the same region. The visible focus stroke was 9 SVG units. Lomo focus selected the two corresponding Argentine short-loin references and the U.S. Short Loin region.
- Visually inspected both diagrams at desktop, 390 px and 320 px widths. No page horizontal overflow or browser console errors/warnings were observed.
- Compared the pre-edit and final datasets: every field except display geometry (p/ps) is unchanged, including cut IDs/names, price mappings, chart colors, descriptions and teaching shares.
- Inline scripts parse and git diff --check passes. No full suite or index rebuild was run. Browser checks are local desktop/mobile emulation, not physical-device or assistive-technology acceptance.
- GitNexus reported file-level LOW impact with one documentation importer. Inline render functions were unresolved (UNKNOWN), so direct source inspection established the shared renderer's two consumers and the map renderer's setup call before editing.
