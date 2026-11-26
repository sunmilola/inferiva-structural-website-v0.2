# Offline viewing

Extract the entire ZIP and open index.html. Keep the folders together. The skyline and overview film are local. DM Sans is bundled and loads offline. Its licence is in media/fonts/OFL.txt. Sending an enquiry requires connectivity.

# INFERIVA customer website

Open `index.html` for the customer homepage or preview the site locally:

```bash
python3 -m http.server 8000
```

The archive includes the generated HTML, all eight original films and their
caption tracks, and the Python generator. Edit page content in `pages.py`
and shared layout in `build.py`, then run `python3 build.py` to regenerate.

The homepage opens with buyer workflows, followed by the integrated platform,
a customer journey, institution pages and engagement options. Detailed product
pages and the assurance specimen are available from their respective sections.

## Enquiry delivery

The supplied HTML opens a prefilled email draft addressed to
`enquiries@inferivastructural.com`. The visitor reviews and sends it in their
email app.

To enable web submission, rebuild the site with an HTTPS form endpoint that
you control and that accepts multipart POST requests from the deployed origin.
The endpoint should return an HTTP 2xx response only when it has accepted the
enquiry. Set the recipient and spam protection with your form provider.

```bash
INFERIVA_ENQUIRY_ENDPOINT='https://your-configured-endpoint' python3 build.py
```

Deploy the regenerated HTML and media together. Submit a test enquiry from
the deployed site and confirm that it reaches the intended inbox.

## Website photography

The photos illustrate ordinary work and payment settings.

| Asset | Photographer and source |
| --- | --- |
| Homepage hero | [Alexander Suhorucov](https://www.pexels.com/photo/young-asian-woman-explaining-business-strategy-to-colleague-6457508/) |
| Platform card, Singapore waterfront | [Arian Fernandez](https://www.pexels.com/photo/skyline-of-singapore-with-iconic-marina-bay-buildings-37182562/) |
| Diagnostics and assurance | [Edmond Dantès](https://www.pexels.com/photo/people-brainstorming-at-the-office-8550845/) |
| Commercial banking, London financial district | [Samuel Phillips](https://www.pexels.com/photo/skyscrapers-in-london-s-financial-district-36920205/) |
| Payments and mobile money | [Pavel Danilyuk](https://www.pexels.com/photo/a-person-tapping-the-phone-on-a-payment-terminal-6612717/) |
| Microfinance | [Mikhail Nilov](https://www.pexels.com/photo/a-woman-holding-laptop-8872695/) |
| Development finance | [Mikhail Nilov](https://www.pexels.com/photo/woman-working-on-her-laptop-8938355/) |

Source terms are available under the [Pexels License](https://www.pexels.com/license/).
