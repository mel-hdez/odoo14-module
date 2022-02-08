{
    'name': "A Module Mel",
    'version': '1.0',
    'depends': [
        'contacts',#se instala el modulo de contacts y esté depende de base
    ],
    'author': "Melissa Hernández",
    'category': 'Category',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'views/menu.xml',
        'views/presupuesto.xml'
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        'demo/demo_data.xml',
    ],
}