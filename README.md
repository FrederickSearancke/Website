# Frederick Searancke — portfolio

Personal projects and research portfolio, hosted on GitHub Pages at
https://www.fredericksearancke.com.

## Development

The current website is in `site/`. The HTML generator uses only Python's standard
library. The styles, JavaScript, images and PDFs are in `site/dist/`.

```sh
python site/build.py
cd site
node server.mjs
```

Open http://127.0.0.1:4173 to preview. Edit `site/build.py` for templates,
`site/profile.json` for profile details, and `site/dist/styles.css` or
`site/dist/app.js` for presentation and interactions. Project wording and approved
edits are recorded in `site/content/`.

## Publishing

Pushing to `main` runs `.github/workflows/static.yml`. The workflow rebuilds the
portfolio and publishes only `site/dist/` to GitHub Pages. GitHub Pages settings
use GitHub Actions and the custom domain `www.fredericksearancke.com`.

The earlier website's files remain at the repository root for reference and are
not included in the deployed artifact. DNS is managed in Squarespace: `www`
points to `fredericksearancke.github.io`, and the apex domain uses GitHub Pages'
four documented A records.
