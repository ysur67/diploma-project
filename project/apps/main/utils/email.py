from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from project import settings
from apps.main.models import SiteSettings


def template_email_message(template, subject, to, data, file='', contentSubtype='html'):
    try:
        template = get_template(template)
        site_name = SiteSettings.objects.first().site_name
        from_email = "<" + settings.DEFAULT_FROM_EMAIL + ">"
        data['site_name'] = site_name
        data['site_url'] = 'trak35.ru'
        data['shop_address'] = SiteSettings.objects.first().shop_address
        email = EmailMultiAlternatives(subject, template.render(
            data), from_email, to)
        email.content_subtype = contentSubtype

        mime = (
            "application/pdf",
            "image/jpg",
            "image/jpeg",
            "image/png",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.template",
            "application/vnd.ms-word.document.macroEnabled.12",
            "application/vnd.ms-word.template.macroEnabled.12",
            "application/vnd.ms-word.document.macroEnabled.12",
            "application/vnd.ms-word.template.macroEnabled.12",
            "application/msexcel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/msexcel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.template",
            "application/msexcel",
            "application/msexcel",
            "application/vnd.ms-excel.sheet.macroEnabled.12",
            "application/vnd.ms-excel.sheet.binary.macroEnabled.12",
            "application/vnd.ms-excel.template.macroEnabled.12",
            "application/vnd.ms-excel.addin.macroEnabled.12",
            "application/vnd.stardivision.chart",
            "application/vnd.stardivision.calc",
            "application/vnd.stardivision.writer",
            "application/vnd.stardivision.writer-global",
            "application/vnd.stardivision.draw",
            "application/vnd.stardivision.impress",
            "application/vnd.stardivision.math ",
            "application/vnd.sun.xml.writer",
            "application/vnd.sun.xml.writer.template",
            "application/vnd.sun.xml.writer.global",
            "application/vnd.sun.xml.calc",
            "application/vnd.sun.xml.calc.template",
            "application/vnd.sun.xml.impress",
            "application/vnd.sun.xml.impress.template",
            "application/vnd.sun.xml.draw",
            "application/vnd.sun.xml.draw.template",
            "application/vnd.sun.xml.math",
            "application/vnd.oasis.opendocument.text",
            "application/vnd.oasis.opendocument.text-template",
            "application/vnd.oasis.opendocument.text-web",
            "application/vnd.oasis.opendocument.text-master",
            "application/vnd.oasis.opendocument.graphics",
            "application/vnd.oasis.opendocument.graphics-template",
            "application/vnd.oasis.opendocument.presentation",
            "application/vnd.oasis.opendocument.presentation-template",
            "application/vnd.oasis.opendocument.spreadsheet",
            "application/vnd.oasis.opendocument.spreadsheet-template",
            "application/vnd.oasis.opendocument.chart",
            "application/vnd.oasis.opendocument.formula",
            "application/vnd.oasis.opendocument.database",
            "application/vnd.oasis.opendocument.image"
        )

        if file:
            email.attach(file.name, file.read(), "image/png")
        email.send()
    except AttributeError:
        return 'Отсутствуют настройки smtp в system.settings'
