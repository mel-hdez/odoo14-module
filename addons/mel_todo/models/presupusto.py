# -*- coding:utf-8 -*-

import string
import logging
from email.policy import default
from attr import field
from odoo import fields, models, api 
from odoo.exceptions import UserError

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

    dsc_clasificacion = fields.Char(
        string = 'Descripción Clasificación'
        )

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

    #sobre escribir funciones odoo
    def unlink(self):

        if self.state != 'cancelado':
            raise UserError ('No se puede eliminar el regitro porque no se encuentra en el estado CANCELADO')
        super(Presupuesto, self).unlink()

    #funciones propias de odoo
    @api.model
    def create(self, variables):
        logger.info('***** variables: {0}'.format(variables))
        return super(Presupuesto, self).create(variables)

    def write (self, variables):
        logger.info('***** variables: {0}'.format(variables))
        if 'clasificacion' in variables:
            raise UserError('¡La clasificación no se puede editar!')
        return super(Presupuesto, self).write(variables)
    
    def copy(self, default = None):
        default =  dict(default or {})
        default ['name'] = self.name + '(Copia)'
        default ['puntuacion2'] = 1
        return super(Presupuesto, self).copy(default)
       
    @api.onchange('clasificacion')
    def _onchange_clasificacion (self):
        if self.clasificacion:
            if self.clasificacion == 'G':
                self.dsc_clasificacion = 'Publico General'
            if self.clasificacion == 'PG':
                self.dsc_clasificacion = 'Se recomienda la compañia de un adulto'
            if self.clasificacion == 'PG-13':
                self.dsc_clasificacion = 'Mayores de 13'
            if self.clasificacion == 'R':
                self.dsc_clasificacion = 'En compañia de un adulto obligatorio'
            if self.clasificacion == 'NC-17':
                self.dsc_clasificacion = 'Mayores de 18'
        else:
            self.dsc_clasificacion = False
            
