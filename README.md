# Prince Kumar — Portfolio

A simple, static portfolio site (no build step) — plain HTML, CSS, and JS.

## Files
- `index.html` — page content
- `style.css` — styling (dark theme by default, light toggle in the top-right)
- `script.js` — theme toggle + small terminal typing effect
- `images/profile.png` — your photo

## Run locally
Just open `index.html` in a browser, or serve it:
```
npx serve .
```

## Deploy: GitHub → Vercel

**1. Push to GitHub**
```
cd portfolio
git init
git add .
git commit -m "Initial portfolio"
git branch -M main
git remote add origin https://github.com/Prince9572/portfolio.git
git push -u origin main
```
(Create the empty `portfolio` repo on GitHub first at github.com/new — don't initialize it with a README, just create it empty, then run the commands above.)

**2. Deploy on Vercel**
1. Go to https://vercel.com and sign in with your GitHub account.
2. Click **Add New → Project**.
3. Select your `portfolio` repository and click **Import**.
4. Framework preset: choose **Other** (it's a static site, no build step needed).
5. Leave Build Command and Output Directory empty.
6. Click **Deploy**.

That's it — Vercel gives you a live URL (e.g. `portfolio-prince.vercel.app`) and will auto-redeploy every time you push to `main`. You can also add a custom domain later from the Vercel project settings.
# Prince-Kumar
