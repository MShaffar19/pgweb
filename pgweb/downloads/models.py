from django.db import models

from pgweb.core.models import Organisation
from pgweb.util.moderation import TwostateModerateModel


class Category(models.Model):
    catname = models.CharField(max_length=100, null=False, blank=False)
    blurb = models.TextField(null=False, blank=True)

    def __str__(self):
        return self.catname

    class Meta:
        ordering = ('catname',)


class LicenceType(models.Model):
    typename = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.typename

    class Meta:
        ordering = ('typename',)


class Product(TwostateModerateModel):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    org = models.ForeignKey(Organisation, db_column="publisher_id", null=False, verbose_name="Organisation", on_delete=models.CASCADE)
    url = models.URLField(null=False, blank=False)
    category = models.ForeignKey(Category, null=False, on_delete=models.CASCADE)
    licencetype = models.ForeignKey(LicenceType, null=False, verbose_name="Licence type", on_delete=models.CASCADE)
    description = models.TextField(null=False, blank=False)
    price = models.CharField(max_length=200, null=False, blank=True)
    lastconfirmed = models.DateTimeField(null=False, blank=False, auto_now_add=True)

    account_edit_suburl = 'products'
    markdown_fields = ('description', )
    moderation_fields = ('org', 'url', 'category', 'licencetype', 'description', 'price')

    def __str__(self):
        return self.name

    @property
    def title(self):
        return self.name

    def verify_submitter(self, user):
        return (len(self.org.managers.filter(pk=user.pk)) == 1)

    class Meta:
        ordering = ('name',)

    @classmethod
    def get_formclass(self):
        from pgweb.downloads.forms import ProductForm
        return ProductForm


class StackBuilderApp(models.Model):
    textid = models.CharField(max_length=100, null=False, blank=False)
    version = models.CharField(max_length=20, null=False, blank=False)
    platform = models.CharField(max_length=20, null=False, blank=False,
                                choices=(
                                    ('windows', 'Windows (32-bit)'),
                                    ('windows-x64', 'Windows (64-bit)'),
                                    ('osx', 'Mac OS X'),
                                    ('linux', 'Linux (32-bit)'),
                                    ('linux-x64', 'Linux (64-bit)'),
                                ))
    secondaryplatform = models.CharField(max_length=20, null=False, blank=True,
                                         choices=(
                                             ('', 'None'),
                                             ('windows', 'Windows (32-bit)'),
                                             ('windows-x64', 'Windows (64-bit)'),
                                             ('osx', 'Mac OS X'),
                                             ('linux', 'Linux (32-bit)'),
                                             ('linux-x64', 'Linux (64-bit)')
                                         ))
    name = models.CharField(max_length=500, null=False, blank=False)
    active = models.BooleanField(null=False, blank=False, default=True)
    description = models.TextField(null=False, blank=False)
    category = models.CharField(max_length=100, null=False, blank=False)
    pgversion = models.CharField(max_length=5, null=False, blank=True)
    edbversion = models.CharField(max_length=5, null=False, blank=True)
    format = models.CharField(max_length=5, null=False, blank=False,
                              choices=(
                                  ('bin', 'Linux .bin'),
                                  ('app', 'Mac .app'),
                                  ('pkg', 'Mac .pkg'),
                                  ('mpkg', 'Mac .mpkg'),
                                  ('exe', 'Windows .exe'),
                                  ('msi', 'Windows .msi')
                              ))
    installoptions = models.CharField(max_length=500, null=False, blank=True)
    upgradeoptions = models.CharField(max_length=500, null=False, blank=True)
    checksum = models.CharField(max_length=32, null=False, blank=False)
    mirrorpath = models.CharField(max_length=500, null=False, blank=True)
    alturl = models.URLField(max_length=500, null=False, blank=True)
    txtdependencies = models.CharField(max_length=1000, null=False, blank=True,
                                       verbose_name='Dependencies',
                                       help_text='Comma separated list of text dependencies, no spaces!')
    versionkey = models.CharField(max_length=500, null=False, blank=False)
    manifesturl = models.URLField(max_length=500, null=False, blank=True)

    purge_urls = ('/applications-v2.xml', )

    def __str__(self):
        return "%s %s %s" % (self.textid, self.version, self.platform)

    class Meta:
        unique_together = ('textid', 'version', 'platform', )
        ordering = ('textid', 'name', 'platform', )
