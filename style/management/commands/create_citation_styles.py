#
# This file is part of Fidus Writer <http://www.fiduswriter.org>
#
# Copyright (C) 2013 Johannes Wilm
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os

from fiduswriter.settings import PROJECT_PATH
from style.models import CitationStyle, CitationLocale

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    args = ''
    help = 'Creates CSS files with the style definitions of all the document styles'

    def handle(self, *args, **options):

        output_js = u'/** @file Makes a list of available styles and locals for the citation style menus. \n This file is automatically created using ./manage.py create_citation_styles\n*/\n'
        output_js += u'(function () {\n'
        output_js += u'    var exports = this, citeproc = {};\n'
        output_js += '\n'        
        
        output_js += u'    citeproc.locals = {\n'
        for cl in CitationLocale.objects.order_by('language_code'):
            output_js += '        "' + cl.display_language_code() + '": "' + cl.contents.replace('\r','').replace('\n','').replace('"','\\"') + '",\n'
        output_js += '    };'
        output_js += '\n'
        
        output_js += '    citeproc.styles = {\n'
        
        for cs in CitationStyle.objects.order_by('short_title'):
            output_js += '        "' + cs.short_title + '": {\n'
            output_js += '            definition: "' + cs.contents.replace('\r','').replace('\n','').replace('"','\\"') + '",\n'
            output_js += '            name: "' + cs.title + '"},\n'
        output_js += '    };'
        output_js += '\n'
        
        output_js += '    exports.citeproc = citeproc;\n'
        output_js += '}).call(this);'
            
        d = os.path.dirname(PROJECT_PATH+'/style/static/js/citation/definitions.js')
        if not os.path.exists(d):
            os.makedirs(d)
        js_file = open(PROJECT_PATH+'/style/static/js/citation/definitions.js', "w")
        js_file.write(output_js.encode('utf8'))
        
        js_file.close()