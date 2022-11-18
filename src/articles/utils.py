from PIL import Image
from io import BytesIO

from .settings import RATIO_HEIGHT, RATIO_WIDTH

from django.core.files import File
from django.http import Http404

class HtmxOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.htmx: 
            raise Http404
        return super().dispatch(request, *args, **kwargs)

def make_thumbnail(image):
    im = Image.open(image)
    width, height = im.size
    # Crop image
    if width/height > RATIO_WIDTH/RATIO_HEIGHT:
        offset  = int(abs(width-RATIO_WIDTH/RATIO_HEIGHT*height)/2)
        image_crop = im.crop([offset,0,width-offset,height])
    else:
        offset  = int(abs(RATIO_HEIGHT/RATIO_WIDTH*width-height)/2)
        image_crop = im.crop([0,offset,width,height-offset])
    # Convert cropped image to a django friendly File object
    thumb_io = BytesIO() 
    image_crop.save(thumb_io, im.format, quality=100)
    thumbnail = File(thumb_io, name=image.name)
    return thumbnail