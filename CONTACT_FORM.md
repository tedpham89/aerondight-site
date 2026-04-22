# Contact Form Setup

## Environment Variables

Set these in the Cloudflare Pages dashboard under **Settings → Environment variables**:

| Variable | Purpose |
|---|---|
| `RESEND_API_KEY` | API key from [resend.com/api-keys](https://resend.com/api-keys) |
| `CONTACT_FROM_EMAIL` | Sender address. Use `onboarding@resend.dev` while testing, then switch to your verified domain address (e.g. `contact@aerondight.systems`) |
| `CONTACT_TO_EMAIL` | Where submissions are delivered (your inbox) |

## Local Testing

The Pages Function (`functions/api/contact.js`) only runs on Cloudflare Pages. During local Astro dev (`npm run dev`), the `/api/contact` endpoint won't exist.

To test locally, use Wrangler:

```bash
npx wrangler pages dev -- npx astro dev
```

You'll need a `.dev.vars` file in the repo root with the three env vars:

```
RESEND_API_KEY=re_...
CONTACT_FROM_EMAIL=onboarding@resend.dev
CONTACT_TO_EMAIL=you@example.com
```

(`.dev.vars` is already gitignored by default in Wrangler.)

## Verifying Your Domain with Resend

To send from `contact@aerondight.systems` instead of `onboarding@resend.dev`:

1. Go to [resend.com/domains](https://resend.com/domains) and add `aerondight.systems`
2. Add the DNS records Resend provides (MX, TXT/SPF, DKIM CNAME records) in your domain registrar / Cloudflare DNS
3. Wait for verification (usually a few minutes)
4. Update `CONTACT_FROM_EMAIL` in Cloudflare Pages env vars to `contact@aerondight.systems`
