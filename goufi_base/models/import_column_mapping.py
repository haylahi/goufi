# -*- coding: utf-8 -*-
'''
Created on 23 deb. 2018

@author: C. Guychard
@copyright: ©2018 Article 714
@license: AGPL v3
'''

import logging

from odoo import models, fields, _, api


class ColumnGroup(models.Model):
    """
    A Column group is a way to define a set of mapping rules that will apply
    to several columns at the same time.
    Processors can support iteration over column groups also, in order to
    provide users with a way to easily import several instances of the same kind of data
    related to the same 'line'
    """
    _name = 'goufi.column_mapping_group'
    _description = _(u"Group of columns, used to defined advanced mapping")
    _rec_name = "name"

    # Column Group
    name = fields.Char(string = _(u'Columns Group name'),
                       help = _(u"Name of the group to map"),
                       required = True, track_visibility = 'onchange')


class ColumnMapping(models.Model):
    _name = 'goufi.column_mapping'
    _description = _(u"Mappings configuration for a given column")
    _rec_name = "name"
    _order = "sequence"

    # Column mapping
    # name of the column
    name = fields.Char(string = _(u'Column name'),
                       help = _(u"Name of the column to map"),
                       required = True, track_visibility = 'onchange')

    sequence = fields.Integer(string = _(u'Sequence'),
                              default = 1, help = _(u"Used to order mappings. Lower is better."))

    # expression
    mapping_expression = fields.Char(string = _(u'Mapping Expression'),
                                     help = _(u"Expression used to process column content, meaning depends on chosen processor."),
                                     required = False, track_visibility = 'onchange')

    # is column part of a group

    member_of = fields.Many2one(string = _(u"Group"),
                                    help = _(u"Set of columns this one belongs to"),
                                    comodel_name = 'goufi.column_mapping_group',
                                    required = False)

    col_group_support = fields.Boolean(string = _(u"Supports column groups"),
                                    help = _(u"Does the processor can process (iterable) group of columns"),
                                    related = "parent_configuration.col_group_support",
                                    required = True, default = False, store = False)

    # is column part of identifier
    is_identifier = fields.Boolean(string = _(u"Is column part of identifiers?"),
                                   help = _(u"""The value of the mapping is used to find existing records in Odoo database.
If a record is found with given value in 'key field' (i.e. field given in expression), the record is updated with data.
If no record is found, a new one is created.

There can be several columns used as criteria
"""),
                                   required = True, default = False)

    # is column a deletion marker
    is_deletion_marker = fields.Boolean(string = _(u"Does column contain a deletion marker?"),
                                        help = _(u"If True, the selected record (if found) will be deleted"),
                                   required = True, default = False)

    delete_if_expression = fields.Char(string = _(u"Delete if value matches"),
                                       help = _(u"Must contain a regular expression that the column value must match to be evaluated as True and the record be deleted"),
                                       required = False, default = _(u"Yes"), size = 64)

    archive_if_not_deleted = fields.Boolean(string = _(u"Archive if not deleted?"),
                                            help = _(u"Should we archive record if deletion fail?"),
                                   required = True, default = False)

    # is column an archival marker
    is_archival_marker = fields.Boolean(string = _(u"Does column contain an archival marker?"),
                                        help = _(u"If True, the selected record (if found) will be archived"),
                                   required = True, default = False)

    archive_if_expression = fields.Char(string = _(u"Archive if value matches"),
                                       help = _(u"Must contain a regular expression that the column value must match to be evaluated as True and the record be archived"),
                                       required = False, default = _(u"Yes"), size = 64)

    # target object (when relevant)
    target_object = fields.Many2one(string = _(u"Target object"),
                                    help = _(u"Odoo object that will be targeted by import: create, update or delete instances"),
                                    comodel_name = "ir.model",
                                    required = False)

    # Info about parent configuration and parent tab (if relevant)

    parent_configuration = fields.Many2one(string = _(u"Parent configuration"),
                                      comodel_name = "goufi.import_configuration")

    tab_support = fields.Boolean(string = _(u"Supports multi tabs"),
                                    help = _(u"Does the selected parent configuration's pocessor can process multiple tabs"),
                                    related = "parent_configuration.tab_support",
                                    required = True, default = False, store = False)

    parent_tab = fields.Many2one(string = _(u"Parent Tab (when multi tabs)"),
                                      comodel_name = "goufi.tab_mapping")

