from django.db import models
from django.utils.safestring import mark_safe
from Scraping.utils import get_image_path
from django_jalali.db import models as jmodels



class Musicitems(models.Model):
    name = models.CharField(max_length=1024, null=True, blank=True, verbose_name='نام کالا')
    # your_link = models.CharField(max_length=1024, null=True, blank=True, verbose_name='آدرس شما')
    your_price = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name='قیمت شما (تومان)')
    is_active = models.BooleanField(default=True, verbose_name="فعال بودن")
    image = models.ImageField(null=True, blank=True,verbose_name='انتخاب عکس', upload_to=get_image_path)
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات')


    class Meta:
        verbose_name = 'کالا'
        verbose_name_plural = 'کالاها'

    def __str__(self):
        return '{}'.format(self.name)

    def _image(self):
        if self.name:
            _name = self.name
            if self.image:
                # return mark_safe('<img src="%s" style="object-fit:scale-down" width=180 height=240 alt="%s"/>'
                #                  % (("http://127.0.0.1:8001/static/uploads/%s" % (self.image)),name))
                return mark_safe('<img src="%s" width=150 height=200 alt="%s"/>'
                             % (("http://185.211.57.73/static/uploads/%s" % (self.image)), _name))
            else:
                return "بدون عکس"
        else:
            return "بدون عکس"
    _image.short_description = 'عکس'
    _image.allow_tags = True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()
        return


class Links(models.Model):
    url = models.CharField(max_length=1024, null=True, blank=True, verbose_name='آدرس')
    musicitem = models.ForeignKey(Musicitems,null=True, blank=True, verbose_name='محصول',related_name='musicitem',
                                  on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'قیمت'
        verbose_name_plural = 'قیمت ها'
    def __str__(self):
        return '{}'.format(self.url)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()
        return

class Prices(models.Model):
    date = jmodels.jDateTimeField(null=True, blank=True, verbose_name='زمان')
    value = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name='قیمت فعلی(تومان)')
    link = models.ForeignKey(Links,null=True, blank=True, verbose_name='محصول',related_name='link',
                                  on_delete=models.CASCADE)
    un_seen_count = models.PositiveSmallIntegerField(default=0, null=True, blank=True, verbose_name="رویت")
    unit = models.CharField(max_length=1024, null=True, blank=True, verbose_name='واحد')
    class Meta:
        verbose_name = 'قیمت'
        verbose_name_plural = 'قیمت ها'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()
        return


