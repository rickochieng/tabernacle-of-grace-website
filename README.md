# Tabernacle of Grace City of Hope Church: Website + Church Manager

Django project. Public site at `/`, staff admin at `/manage/`.

## First-time setup (developer)
```
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser        # your own admin login
python manage.py setup_staff_group      # creates the simple "Church Staff" group
python manage.py runserver
```
Staff accounts: log in at `/manage/` → Users → Add user → tick **Staff status** → add to group **Church Staff**.

## Going live: environment variables
`DEBUG=0`, `SECRET_KEY=<long random string>`, `ALLOWED_HOSTS=yourdomain.com`, `CSRF_TRUSTED_ORIGINS=https://yourdomain.com`,
`DATABASE_URL=postgres://...` (SQLite is used if omitted), `MEDIA_ROOT=<persistent disk path for uploads>`,
and for email: `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`.
Then: `python manage.py collectstatic --noinput` and run `gunicorn church.wsgi`.
Uploaded photos live in `MEDIA_ROOT`: it must be on persistent storage and backed up.

## Staff guide (plain English)
Go to `yourwebsite.com/manage/` and log in.
- **Sermons → Add:** title, speaker, date, topic, a short summary, paste the YouTube link. Untick *Show on website* to hide one.
- **Events → Add:** title, date, time, place. Past events disappear from the site by themselves.
- **Photos → Add:** choose a photo and type a caption.
- **Prayer requests / Contact messages:** read them here. Tick the box or use the Action menu to mark *Prayed for* / *Replied*.
- **Church details:** change the phone number, address, and the email that receives new prayer requests and messages.
Always click **Save** at the bottom of the page.

## Not included yet
M-Pesa giving. The "Moments of Grace" mosaic and gallery-1…6 photos on the home page still come from `static/images/`.
