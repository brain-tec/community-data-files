#!/usr/bin/env python
# Copyright 2011 Numérigraphe SARL.
# Copyright 2022 brain-tec AG
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


import csv
import logging

_logger = logging.getLogger(__name__)

# List of languages to generate translations for
LANGS = [
    "bg",
    "cs",
    "da",
    "de",
    "et",
    "en",
    "es",
    "el",
    "fi",
    "fr",
    "hr",
    "hu",
    "it",
    "lt",
    "lv",
    "mt",
    "nl",
    "no",
    "pl",
    "pt",
    "ro",
    "ru",
    "sk",
    "sl",
    "sv",
    "tr",
]

# We dont need everything
LANGS = [
    "en",
    "de",
    # "fr",
]

# All the generated record ids will be in this forms
ID_TEMPLATE = "nace_%s"

_logger.info("Generating the English CSV file...")
src = csv.reader(open("NACE_REV2_en.csv", "r+"))
dest = csv.writer(open("res.partner.nace.csv", "w"), quoting=csv.QUOTE_ALL)
# Write the file header
dest.writerow(["id", "parent_id:id", "code", "name"])
# Write the root category
parent_ids = {0: ID_TEMPLATE % "root"}
dest.writerow([parent_ids[0], "", "", "NACE"])
# Skip first line
next(src)
english = {}
for row in src:
    xml_id = ID_TEMPLATE % row[9]
    code = row[2]
    name = row[4]
    # determine the parent
    level = int(row[1])
    parent_id = parent_ids[level - 1]
    # Remember the current id as a parent
    parent_ids[level] = xml_id
    # Remember the English name and the id
    english[xml_id] = name
    dest.writerow([xml_id, parent_id, code, name])
_logger.info("Done.\n")

for lang in LANGS:
    filename = lang != "en" and ("%s.po" % lang) or "l10n_eu_nace.pot"
    _logger.info("Generating %s..." % filename)
    src = csv.reader(open("NACE_REV2_%s.csv" % lang, "r+"))
    # Skip first line
    next(src)
    # Write file header
    dest = open("../i18n/%s" % filename, "w")
    dest.write(
        """# Translation of Odoo Server.
# This file contains the translation of the following modules:
#    * l10n_eu_nace
#
msgid ""
msgstr ""
"Project-Id-Version: Odoo Server 15.0\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2022-07-15 11:00+0000\\n"
"PO-Revision-Date: 2022-07-15 11:00+0000\\n"
"Last-Translator: <>\\n"
"Language-Team: \\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: \\n"
"Plural-Forms: \\n"

"""
    )
    for row in src:
        name = "%s" % ( row[4])
        xml_id = ID_TEMPLATE % row[9]
        dest.write(
            """#. module: l10n_eu_nace
#: model:res.partner.nace,name:l10n_eu_nace.%s
msgid "%s"
msgstr "%s"

"""
            % (xml_id, english[xml_id], lang != "en" and name or "")
        )
_logger.info("Done.\n")
