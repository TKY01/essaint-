# Essaint / Off Duty — Shopify theme

A native Shopify Online Store 2.0 theme, plus a private static design preview. The revised art direction combines campaign-led streetwear typography and a restrained essentials shop, informed by Imanuel and Irrelevant Living. The theme reads live Shopify products, variants, availability, prices, currency and cart data. The preview uses the public storefront snapshot from September 10, 2026 and a local demonstration bag. It does not process payments.

## Install on the existing Essaint store

1. In Shopify Admin, open **Online Store → Themes → Add theme → Upload ZIP file** and upload `essaint-shopify-theme.zip`.
2. Keep it unpublished and open **Customize**. Set the featured collection under **Essentials**. Edit the hero image and headline as desired.
3. Under **Bundles**, set the tops and bottoms collections (both default to all products). The outfit studio allows shoppers to select a T-shirt and a trouser style, then each variant. Check the three suggested outfit blocks, which contain editable product references matching existing Essaint handles.
   Under **Product packs**, choose the available-products collection. Shoppers can select 1, 3, or 6 units and configure the size/color of each separately. Under **In the Wild**, edit the five photo cards, their image pickers, captions and linked products.
4. Assign the `contact` template to your Contact page. Review shipping/refund policies and newsletter settings in Shopify Admin.
5. Preview desktop and mobile, select multiple sizes/colors, verify unavailable variants, add a two-piece set, change quantities, and complete a test checkout using the store's payment test mode. Confirm tax, shipping, payment, currency and exchange settings before publishing.
6. Publish from the Shopify theme library when the store checks are complete. Your previous theme remains available for rollback.

No product import is needed on essaint.com. Product data is independent of the theme.

## Bundles and discounts

The inline outfit studio previews each selected product, updates the combined live price and adds both selected variants in one Shopify Ajax Cart API request, preserving Shopify inventory checks. Sold-out styles cannot be added; product changes invalidate stale selections while new options load. Components remain individual cart lines and share an `Outfit edit` line property. This is a curated set, not a fixed-price inventory bundle. No discount is invented or applied by JavaScript. Create an eligible automatic discount in Shopify Admin if wanted; verify its rules at checkout. For fixed-price bundles and bundle inventory grouping, configure Shopify Bundles separately.

Product packs use the same live cart API and include one selected variant per piece. Quantity cards show 1 / 3 / 6 units; the final total reflects each chosen variant. Unavailable combinations block the add button. Variant-linked photography updates when a piece's color or size changes. Pack savings are not advertised because no destination-store discount rules have been configured.

## Design assets

The campaign hero `theme/assets/campaign-off-duty.png` is an AI-generated editorial scene based on Essaint's original outfit photography. It is not a claim about a real campaign location. The lookbook includes Essaint's original poolside campaign image; all product catalog images are unchanged. Competing brands' images were inspected for art direction only and are not included in the storefront. The hero can be replaced with an image picker in Shopify Customize.

The staggered **In the Wild** cards use four photos already published in Essaint's Shop the Look section plus its original poolside campaign. Source URLs are in `data/wild.json`. Photo-card settings are in `data/wild-cards.json` and the homepage JSON template. The purple trouser photo links to the purple product; the sold-out state is retained.

## Product export

`data/products.json`: original public source response; `data/catalog.json`: enriched source with downloaded-image filenames; `data/products.csv`: Shopify-format draft import for a different store; `data/provenance.json`: retrieval details. All 12 public products, 66 variants and 27 product images are included. The export does not contain stock quantities, costs, private metafields, customer records, or private admin data.

The CSV intentionally creates drafts and omits unknown inventory quantities. Before importing into another store, verify inventory, tax, SKUs, shipping, prices and publication status. Do not use it to overwrite existing inventory. Original Shopify variant IDs are used only by the preview; the production theme resolves IDs from its own store.

## Local development

- `python scripts/build.py` regenerates the base theme and catalog export, then applies the current art direction using `scripts/redesign.py`.
- `python scripts/redesign.py` reapplies the Off Duty sections without rescraping products.
- `python scripts/preview.py` builds `dist/` from the theme's layout sections, images, shared CSS and shared commerce JavaScript.
- `npx shopify theme check --path theme` validates theme syntax and Shopify compatibility.
- `npm test` checks product availability, outfit-studio selection and totals, bag updates, filtering and product routing using a simulated DOM.
- `python scripts/package.py` packages the theme ZIP and refreshes the preview download.
- `python -m http.server 4173 --directory dist` serves the static preview.
- `npx shopify theme dev --path theme --store YOUR-STORE.myshopify.com` runs Shopify's authenticated theme preview.

The Shopify theme is the deployment artifact. Sites hosts the review preview only. No Shopify store credentials were provided, so installation, actual checkout, admin discount setup and live Shopify rendering must be verified in the destination store.

Source: https://essaint.com/products.json?limit=250 and https://essaint.com/ . Shopify references: https://shopify.dev/docs/storefronts/themes/architecture and https://shopify.dev/docs/api/ajax/reference/cart .
