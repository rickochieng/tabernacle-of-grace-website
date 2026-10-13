from django.db import models


class SiteDetails(models.Model):
    phone = models.CharField('Church phone number', max_length=40, default='0740 181262')
    address = models.CharField('Church address', max_length=200, default='Wambiri Rd, Opposite Lenana School Primary, Nairobi')
    notification_email = models.EmailField('Send prayer requests & messages to this email', blank=True,
                                           help_text='Leave empty to receive nothing by email (they still appear in the inbox here).')

    class Meta:
        verbose_name = verbose_name_plural = 'Church details'

    def save(self, *a, **k):
        self.pk = 1
        super().save(*a, **k)

    @classmethod
    def load(cls):
        return cls.objects.get_or_create(pk=1)[0]

    def __str__(self):
        return 'Church details'


class Sermon(models.Model):
    title = models.CharField(max_length=150)
    speaker = models.CharField(max_length=100, default='Pastor')
    date = models.DateField('Date preached')
    category = models.CharField('Topic', max_length=60, blank=True, help_text='e.g. Faith & Healing')
    description = models.TextField('Short summary', blank=True)
    video_url = models.URLField('YouTube link', blank=True, help_text='Paste the full link of the video.')
    thumbnail = models.ImageField('Picture (optional)', upload_to='sermons/', blank=True)
    published = models.BooleanField('Show on website', default=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=150)
    date = models.DateField()
    time_text = models.CharField('Time', max_length=60, blank=True, help_text='e.g. 9:00 AM – 12:00 PM')
    location = models.CharField(max_length=120, blank=True)
    description = models.CharField('Short description', max_length=250, blank=True)
    category = models.CharField('Label', max_length=30, blank=True, help_text='e.g. Youth, Outreach, Weekly')
    published = models.BooleanField('Show on website', default=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f'{self.title} ({self.date})'


class Photo(models.Model):
    image = models.ImageField('Photo', upload_to='gallery/')
    caption = models.CharField(max_length=100, blank=True)
    uploaded = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded']

    def __str__(self):
        return self.caption or f'Photo {self.pk}'


class PrayerRequest(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField('Phone / email', max_length=150, blank=True)
    category = models.CharField(max_length=60, blank=True)
    request = models.TextField()
    created = models.DateTimeField('Received', auto_now_add=True)
    prayed_for = models.BooleanField('Prayed for', default=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.name} – {self.category}'


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField('Phone / email', max_length=150, blank=True)
    subject = models.CharField(max_length=150, blank=True)
    message = models.TextField()
    created = models.DateTimeField('Received', auto_now_add=True)
    handled = models.BooleanField('Replied / done', default=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.name}: {self.subject}'


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created = models.DateTimeField('Joined', auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.email
