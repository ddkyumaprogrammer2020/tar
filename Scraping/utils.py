import jdatetime
from django.utils.text import slugify


def get_image_path(instance, filename):
    title = instance.id
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    date = jdatetime.datetime.now().date()
    new_filename = "%s.%s" % (slug , file_extension)
    # return  os.path.join("/","images", "%s" %new_filename)
    return "%s" %new_filename
    # return os.path.join(settings.MEDIA_ROOT, new_filename)