# -*- coding: utf-8 -*-
'''
Created on 23 deb. 2018

@author: C. Guychard
@copyright: ©2018 Article 714
@license: AGPL v3
'''

import logging

from odoo import models, fields, _, api


class ColumnMapping(models.Model):
    _name = 'goufi.column_mapping'
    _description = u"Import File"
    _rec_name = "name"

    # Column mapping
    # name of the column
    name = fields.Char(string = _(u'Name'), required = True, track_visibility = 'onchange')

    # expression
    mapping_expression = fields.Char(string = _(u'Mapping Expression'), required = True, track_visibility = 'onchange')

    # is column part of identifier
    is_identifier = fields.Boolean(string = _(u"Is column part of identifiers?"),
                                   required = True, default = False)

    target_object = fields.Many2one(comodel_name = 'ir.model')

    parent_configuration = fields.Many2one(string = _(u"Parent configuration"),
                                      comodel_name = "goufi.import_configuration")

    tab_support = fields.Boolean(string = _(u"Supports multi tabs"),
                                    help = _(u"Does the selected parent configuration's pocessor can process multiple tabs"),
                                    related = "parent_configuration.tab_support",
                                    required = True, default = False)

    parent_tab = fields.Many2one(string = _(u"Parent Tab (when multi tabs"),
                                      comodel_name = "goufi.tab_mapping")
