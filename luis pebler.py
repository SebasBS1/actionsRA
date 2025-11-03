import unittest

class Item:
    def __init__(self, price, name, amount):
        self.price = price
        self.name = name
        self.amount = amount

    '''def add(self, item): 
        return Item(self.amount + item.amount)

    def sub(self, items_to_remove): 
        return Item(self.amount - items_to_remove)'''

class ShoppingCart: 
    def __init__(self):
        self.total_price = 0
        self.items = []
        self.discount = 0.0

    def add_item(self, new_item: Item):
        if not isinstance(new_item, Item):
            raise ValueError("Este producto no existe")
    
        for item in self.items: 
            if new_item.name == item.name:
                item.amount += new_item.amount
                return
        self.total_price = self.total_price + new_item.price
        self.items.append(new_item)
        return

    def remove_item(self, item_to_remove, amount): 
        for item in self.items:
            if item.name == item_to_remove:
                if amount >= item.amount:
                    self.items.remove(item)
                else:
                    item.amount -= amount
                return
        raise ValueError("No está el item que se quiere eliminar")

    def show_total_price(self): 
        subtotal = sum(item.price * item.amount for item in self.items)
        return subtotal - (subtotal * self.discount)

    def discount_overall(self, discount): 
        self.discount = abs(discount/100.0)
        
    def discount_product(self, item_to_discount, discount):
        for item in self.items: 
            if item.name == item_to_discount:
                item.price -= (item.price * abs(discount/100.0))
                return
        raise ValueError("No existe el producto al que se le quiere poner el descuento")
                
                


class TestShoppingCart(unittest.TestCase):
    
    def setUp(self):
        self.cafe = Item(50, "Cafe", 5)
        self.amogus = Item(1, "Amogus", 1)
        self.pan = Item(10, "Pan", 1)
        self.nuggetsDeDinosaurio = Item(75, "Nuggets de dinosaurio", 1)
        
        
        self.carro1 = ShoppingCart()
        self.carro2 = ShoppingCart()
    
    def test_AddItem(self):
        #Agregar productos a un carrito
        self.carro1.add_item(self.amogus)
        self.carro1.add_item(self.pan)
        #Verificación
        self.assertEqual(len(self.carro1.items), 2)
        
        #Agregar productos del mismo nombre
        self.carro1.add_item(self.amogus)
        
        #Verificación, al ser un producto repetido debería de dar igual ya que solo aumenta su cantidad
        self.assertEqual(len(self.carro1.items), 2)
        
        #Agregar producto que no exite
        with self.assertRaises(ValueError):
            self.assertEqual(self.carro1.add_item("Felipe"))
            
    def test_removeItem(self):
        #Quitar un producto al carro
        self.carro1.add_item(self.cafe)
        self.carro1.remove_item("Cafe", 1)
        #Verificar, puesto a que existen 5 de ese producto y solo quitamos 1, aun deben de quedar 4
        for item in self.carro1.items:
            if item.name == "Cafe":
                self.assertEqual(item.amount, 4)
        #Quitar toda la cantidad de un item
        self.carro1.add_item(self.pan)
        self.carro1.remove_item("Pan", 1)
        #Verificar, puesto a que la cantidad queda en 0, el producto se elimina de la lista, dejando solo el cafe
        self.assertEqual(len(self.carro1.items), 1)
        #Eliminar una cantidad de productos más grande de la que ya hay en la lista
        self.carro1.remove_item("Cafe", 100)
        #Verificar, al querer borrar más de lo que ya hay, instantaneamente debería de quedar en 0 por lo que se borra de la lista
        self.assertEqual(len(self.carro1.items), 0)
        #Eliminar un producto que no esta en la lista
        with self.assertRaises(ValueError):
            self.assertEqual(self.carro1.remove_item("Leche", 1))
            
    def test_totalPrices(self):
        #Probar el total de un carro vacío
        self.assertEqual(self.carro1.show_total_price(), 0)
        #Probar el total de un carro con un producto
        self.carro1.add_item(self.pan)
        #Verificar, ahora que hay un pan debe de haber un total de 10
        self.assertEqual(self.carro1.show_total_price(), 10)
        #Probar el total de un carro con más de un mismo producto
        self.carro1.add_item(self.pan)
        #Verificar, como ahora hay 2 panes deben de costar 20 pesos
        self.assertEqual(self.carro1.show_total_price(), 20)
        #Probar el total de un carro con distintos productos
        self.carro1.add_item(self.amogus)
        #Ahora hay tanto 2 panes (10 cada 1) como un amogus (1 cada 1), por lo que el total debe de ser 21
        self.assertEqual(self.carro1.show_total_price(), 21)
        
    def test_discountTotal(self):
        #Agregar descuento a un carrito con productos
        self.carro1.add_item(self.pan)
        self.carro1.add_item(self.nuggetsDeDinosaurio)
        self.carro1.add_item(self.amogus)
        self.carro1.discount_overall(10)
        #Verificar, al agregar un 10% a la compra final el precio debería pasar de 86 a 77.4
        self.assertEqual(self.carro1.show_total_price(), 77.4)
        #Cambiar el valor del descuento por otro
        self.carro1.discount_overall(50)
        #Se cambia el 10% de descuento por 50%
        self.assertEqual(self.carro1.show_total_price(), 43)
        #Agregar un descuento negativo
        self.carro1.discount_overall(-40)
        #Verificar, a pesar de ser un número negativo, el total del carrito debe de ser positivo
        self.assertEqual(self.carro1.show_total_price(), 51.6)
    
    def test_descuentoIndividual(self):
        #Probar agregar descuento a un producto
        self.carro1.add_item(self.nuggetsDeDinosaurio)
        self.carro1.discount_product("Nuggets de dinosaurio", 20)
        #Verificar, ahora el producto debe de pasar de 75 a 60
        self.assertEqual(self.carro1.show_total_price(), 60)
        #Agregar descuento a un producto inexistente
        with self.assertRaises(ValueError):
            self.assertEqual(self.carro1.discount_product("Mayonesa", 20))
    
    
if __name__ == '__main__': 
    unittest.main(verbosity=2)
        

