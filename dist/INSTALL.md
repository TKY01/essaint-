# Essaint Atelier — Shopify theme

A native Shopify Online Store 2.0 theme, plus a private static design preview. The theme reads live Shopify products, variants, availability, prices, currency and cart data. The preview uses the public storefront snapshot from September 10, 2026 and a local demonstration bag. It does not process payments.

## Install on the existing Essaint store

1. In Shopify Admin, open **Online Store → Themes → Add theme → Upload ZIP file** and upload `essaint-shopify-theme.zip`.
2. Keep it unpublished and open **Customize**. Set the featured collection under **Essentials**. Edit the hero image and headline as desired.
3. Check the three **Outfit bundles** blocks. Each contains two editable product references with defaults matching the existing Essaint handles. Choose a different product if a reference is missing.
4. Assign the `contact` template to your Contact page. Review shipping/refund policies and newsletter settings in Shopify Admin.
5. Preview desktop and mobile, select multiple sizes/colors, verify unavailable variants, add a two-piece set, change quantities, and complete a test checkout using the store's payment test mode. Confirm tax, shipping, payment, currency and exchange settings before publishing.
6. Publish from the Shopify theme library when the store checks are complete. Your previous theme remains available for rollback.

No product import is needed on essaint.com. Product data is independent of the theme.

## Bundles and discounts

The outfit builder adds both selected live variants in one Shopify Ajax Cart API request, preserving Shopify inventory checks. Components remain individual cart lines and share an `Outfit edit` line property. This is a curated set, not a fixed-price inventory bundle. No discount is invented or applied by JavaScript. Create an eligible automatic discount in Shopify Admin if wanted; verify its rules at checkout. For fixed-price bundles and bundle inventory grouping, configure Shopify Bundles separately.

## Product export

`data/products.json`: original public source response; `data/catalog.json`: enriched source with downloaded-image filenames; `data/products.csv`: Shopify-format draft import for a different store; `data/provenance.json`: retrieval details. All 12 public products, 66 variants and 27 product images are included. The export does not contain stock quantities, costs, private metafields, customer records, or private admin data.

The CSV intentionally creates drafts and omits unknown inventory quantities. Before importing into another store, verify inventory, tax, SKUs, shipping, prices and publication status. Do not use it to overwrite existing inventory. Original Shopify variant IDs are used only by the preview; the production theme resolves IDs from its own store.

## Local development

- `python scripts/build.py` regenerates Liquid sections, templates and the catalog export, downloading missing original product images.
- `python scripts/preview.py` builds `dist/` from the theme's layout sections, images, shared CSS and shared commerce JavaScript.
- `npx shopify theme check --path theme` validates theme syntax and Shopify compatibility.
- `python scripts/package.py` packages the theme ZIP and refreshes the preview download.
- `python -m http.server 4173 --directory dist` serves the static preview.
- `npx shopify theme dev --path theme --store YOUR-STORE.myshopify.com` runs Shopify's authenticated theme preview.

The Shopify theme is the deployment artifact. Sites hosts the review preview only. No Shopify store credentials were provided, so installation, actual checkout, admin discount setup and live Shopify rendering must be verified in the destination store.

Source: https://essaint.com/products.json?limit=250 and https://essaint.com/ . Shopify references: https://shopify.dev/docs/storefronts/themes/architecture and https://shopify.dev/docs/api/ajax/reference/cart .
