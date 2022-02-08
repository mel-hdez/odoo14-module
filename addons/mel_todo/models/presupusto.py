# -*- coding:utf-8 -*-

import string
import logging
from email.policy import default
from attr import field
from odoo import fields, models, api 

#variables globales
logger = logging.getLogger(__name__)

class Presupuesto(models.Model):
    _name = "Presupuesto"
    _inherit = ['image.mixin'] #modelo para cargar imagenes

    name = fields.Char(string = 'Pelicula')

    clasificacion = fields.Selection(selection=[
        ('G','G'), #publico general
        ('PG','PG'), #se recomienda la compañia de un adulto
        ('PG-13','PG-13'), #mayores de 13 años
        ('R','R'), #en compañia de un adulto obligatorio
        ('NC-17','NC-17') #mayores de 18
    ], string = 'Clasificación')

    fch_estreno = fields.Date(
        string = 'Fecha de estreno'
        )

    puntuacion = fields.Integer(
        string = 'Puntuación',
        related="puntuacion2"
        )

    puntuacion2 = fields.Integer(
        string = 'Puntuación2'
        )

    active = fields.Boolean(
        string = 'Activo', 
        default=True
        )
    #relacion en la bd 1:1, 1:n, M:N
    director_id = fields.Many2one(
        comodel_name = 'res.partner',
        string = 'Director'
    )

    categoria_director_id = fields.May2one(
        comodel_name = 'res.partner.category',
        string = 'Categoria Director',
        default = lambda self: self.env['res.partner.category'].search([('name','=','Director')])
    )
    genero_ids = fields.Many2many(
        comodel_name = 'genero',
        string = 'Generos'
    )

    vista_general = fields.Text(
        string = 'Descripción'
        )

    link_trailer = fields.Char(
        string = 'Trailer'
        )

    es_libro = fields.Boolean(
        string = 'Version libro'
    )

    libro = fields.Binary(
        string = 'Libro'
    )

    libro_filename = fields.Char(
        string = 'Nombre del libro'
    )

    state = field.Selection(selection=[
        ('borrador','Borrador'),
        ('aprobado','Aprobado'),
        ('cancelado','Cancelado'),
    ],default = 'borrador', string = 'Estado', copy = False)

    fch_aprobado = fields.Datetime(
        string = 'Fecha aprobado',
        copy = False)

    def aprobar_presupuesto(self):
        self.state = 'aprobado'
        self.fch_aprobado = fields.Datetime.now()

    def cancelar_presupuesto(self):
        self.state = 'cancelado'