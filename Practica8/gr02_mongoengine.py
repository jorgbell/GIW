from mongoengine import *


class Tarjeta(EmbeddedDocument):

    nombre = StringField(required=True, min_length=2)
    numero = StringField(required=True, min_length=16, max_length=16)
    mes = StringField(required=True, min_length=2, max_length=2)
    año = StringField(required=True, min_length=2, max_length=2)
    ccv = StringField(required=True, min_length=3, max_length=3)

    def __init__(self, nombre, numero, mes, año, ccv):
        self.nombre = nombre
        self.numero = numero
        self.mes = mes
        self.año = año
        self.ccv = ccv


class Producto(Document):

    codigo_barras = StringField(required=True, unique=True, min_length=13, max_length=13)
    nombre = StringField(required=True, min_length=2)
    categoria_principal = IntField(required=True)
    categorias_secundarias = ListField(IntField())

    def __init__(self, codigo_barras, nombre, categoria_principal, categorias_secundarias):
        self.codigo_barras = codigo_barras
        self.nombre = nombre
        self.categoria_principal = categoria_principal
        self.categorias_secundarias = categorias_secundarias

    def clean(self):
        self.validate(clean=False)

        # Validar codigo de barras
        weights = [1,3]*6
        checkSum = sum([x * w for x, w in zip(self.codigo_barras[:-1], weights)])
        if 10 - (checkSum % 10) != self.codigo_barras[-1]:
            raise ValidationError('El codigo de barras no es valido')

        if len(self.categorias_secundarias) != 0 and self.categoria_principal != self.categorias_secundarias[0]:
            raise ValidationError('La categoria principal debe aparecer como la primera categoria secundaria')


class Linea(EmbeddedDocument):

    num_items = IntField(required=True)
    precio_item = FloatField(required=True) # >0
    nombre_item = StringField(required=True, min_length=2)
    total = FloatField(required=True) # >0
    ref = ReferenceField(document_type=Producto, required=True)

    def __init__(self, num_items, precio_item, nombre_item, total, ref):
        self.num_items = num_items
        self.precio_item = precio_item
        self.nombre_item = nombre_item
        self.total = total
        self.ref = ref

    def clean(self):
        self.validate(clean=False)

        if self.precio_item <= 0:
            raise ValidationError('El precio del item debe ser mayor que cero')

        if self.total <= 0:
            raise ValidationError('El precio total debe ser mayor que cero')

        if self.total != self.precio_item * self.num_items:
            raise ValidationError('El precio total debe ser igual al producto de precio y numero de items')

        if self.nombre_item != self.ref.nombre:
            raise ValidationError('El nombre de la linea debe ser el mismo que el del producto')


class Pedido(Document):
    
    total = FloatField(required=True) # >0
    fecha = ComplexDateTimeField(required=True)
    lineas = ListField(field=Linea, required=True)

    def __init__(self, total, fecha, lineas):
        self.total = total
        self.fecha = fecha
        self.lineas = lineas        

    def clean(self):
        self.validate(clean=False)

        if self.total <= 0:
            raise ValidationError('El precio total debe ser mayor que cero')

        if self.total != sum([l.total for l in self.lineas]):
            raise ValidationError('El precio total debe ser igual a la suma de los precios de las lineas')

        if len(set([l.ref.codigo_barras for l in self.lineas])) != len(self.lineas):
            raise ValidationError('No puede haber dos líneas diferentes asociadas a un mismo producto')


class Usuario(Document):

    dni = StringField(required=True, unique=True, regex='[0-9]{8}[A-Z]', min_length=9, max_length=9)
    nombre = StringField(required=True, min_length=2)
    apellido1 = StringField(required=True, min_length=2)
    apellido2 = StringField()
    f_nac = ComplexDateTimeField(required=True, separator='-')
    tarjetas = ListField(Tarjeta)
    pedidos = ReferenceField(document_type=Pedido, reverse_delete_rule=PULL)

    def __init__(self, dni, nombre, apellido1, apellido2, f_nac, tarjetas, pedidos):
        self.dni = dni
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.f_nac = f_nac
        self.tarjetas = tarjetas
        self.pedidos = pedidos
        

    def clean(self):
        self.validate(clea=False)

        rem_to_letter = 'TRWAGMYFPDXBNJZSQVHLCKE'
        if rem_to_letter[int(self.dni[:-1]) % 23] != self.dni[-1]: # El resto del numero del dni / 23 se convierte en letra y debe ser la misma que lleva el dni
            raise ValidationError('DNI no valido')


connect('giw_mongoengine')