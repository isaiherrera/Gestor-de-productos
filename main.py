from tkinter import ttk
from tkinter import *
import sqlite3

class Producto:

    db = 'database/productos.db'
    def __init__(self, root):
        self.ventana = root
        self.ventana.title('Gestor de Productos')
        self.ventana.resizable(1,1) # Esto permite redimensionar la app tanto hacia los lados, como arriba o abajo.
                                    # Por defecto está activado en (1,1)

        # Creación del contenedor Frame principal
        frame = LabelFrame(self.ventana, text = 'Registrar un nuevo Producto')
        frame.grid (row = 0, column = 0, columnspan = 3, pady = 20)

        # Label Nombre
        self.etiqueta_nombre = Label (frame, text = 'Nombre: ')
        self.etiqueta_nombre.grid(row = 1, column = 0)
        # Entry nombre
        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)

        # Label precio
        self.etiqueta_precio = Label (frame, text = 'Precio: ')
        self.etiqueta_precio.grid(row = 2, column = 0)
        # Entry precio
        self.precio = Entry(frame)
        self.precio.grid(row=2, column=1)

        # Botón de Añadir Producto
        self.boton_aniadir = ttk.Button(frame, text = 'Guardar Producto', command = self.add_producto) #En este caso va
        ## sin paréntesis !!!!!!
        self.boton_aniadir.grid(row=3, columnspan = 2, sticky = W + E)

        self.mensaje = Label(text = '', fg  = 'red')
        self.mensaje.grid(row=3, columnspan=2, sticky=W + E)

        # Tabla de Productos
        # Estilo personalizado para la tabla
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri',11))
        # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))
        # Se modifica la fuente de las cabeceras
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky':'nswe'})])
        # Eliminamos los bordes

        #Estructura de la tabla
        self.tabla = ttk.Treeview(height = 20, columns = 2, style = 'mystile.Treeview')
        self.tabla.grid(row=4, column=0, columnspan = 2)
        #Cabeceras
        self.tabla.heading('#0', text='Nombre', anchor=CENTER)
        self.tabla.heading('#1', text='Precio', anchor=CENTER)

        # Botones de Eliminar y Editar
        s = ttk.Style()
        s.configure('my.TButton', font= ( 'Calibri', 14, 'bold'))

        boton_eliminar = ttk.Button(text='ELIMINAR', style= 'my.TButton', command = self.del_producto)
        boton_eliminar.grid(row=5, column=0, sticky=W + E)
        boton_editar = ttk.Button(text='EDITAR', style= 'my.TButton', command = self.edit_producto)
        boton_editar.grid(row=5, column=1, sticky=W + E)

        self.get_productos()

    def db_consulta(self, consulta, parametros = ()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta,parametros)
            con.commit()
        return resultado

    def get_productos(self):

        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)

        query = 'SELECT * FROM producto ORDER BY nombre DESC'
        registros = self.db_consulta(query)


        for fila in registros:
            print(fila)
            self.tabla.insert('', 0, text = fila[1], values = fila[2])

    def validacion_nombre(self):
        nombre_introducido_por_usuario = self.nombre.get()
        return len(nombre_introducido_por_usuario) != 0

    def validacion_precio(self):
        precio_introducido_por_usuario = self.precio.get()
        return len(precio_introducido_por_usuario) != 0


    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio():
            query = 'INSERT INTO producto VALUES(NULL, ?, ?)' #Se añade el null, porque es un valor
            # autoincrementado
            parametros = (self.nombre.get(), self.precio.get()) # Tenemos que pasarle un tupla
            self.db_consulta(query, parametros)
            print('Datos guardados')
            # Para debug
            #print(self.nombre.get())
            #print(self.precio.get())
        elif self.validacion_nombre() and self.validacion_precio() == False:
            print('Error. El precio es obligatorio')
            self.mensaje['text'] = 'Error. El precio es obligatorio'

        elif self.validacion_nombre() == False and self.validacion_precio():
            print('Error. El nombre es obligatorio')
            self.mensaje['text'] = 'Error. El nombre es obligatorio'

        else:
            print('Error. El nombre y precio son obligatorios')
            self.mensaje['text'] = 'Error. El nombre y precio son obligatorios'

        self.get_productos()

    def del_producto(self):
        print(self.tabla.item(self.tabla.selection()))
        nombre = self.tabla.item(self.tabla.selection())['text']
        query = 'DELETE FROM producto WHERE nombre = ?'  # Consulta SQL
        self.db_consulta(query, (nombre,))  # Ejecutar la consulta
        self.mensaje['text'] = 'Producto {} eliminado con éxito'.format(nombre)
        self.get_productos()  # Actualizar la tabla de productos

    def edit_producto(self):
        self.mensaje['text'] = ''  # Mensaje inicialmente vacio
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return
        nombre = self.tabla.item(self.tabla.selection())['text']
        old_precio = self.tabla.item(self.tabla.selection())['values'][0]  # El precio se encuentra dentro de una lista
        self.ventana_editar = Toplevel()  # Crear una ventana por delante de la principal
        self.ventana_editar.title = "Editar Producto"  # Titulo de la ventana
        self.ventana_editar.resizable(1, 1)  # Activar la redimension de la ventana. Para desactivarla: (0, 0)
        self.ventana_editar.wm_iconbitmap('recursos/M6_P2_icon.ico')  # Icono de la ventana

        titulo = Label(self.ventana_editar, text='Edición de Productos', font=('Calibri', 50, 'bold'))
        titulo.grid(column=0, row=0)

        # Creacion del contenedor Frame de la ventana de Editar Producto
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto")
        #frame_ep: Frame Editar Producto
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # Label Nombre antiguo
        self.etiqueta_nombre_anituguo = Label(frame_ep, text="Nombre antiguo: ")
        # Etiqueta de texto ubicada en el frame
        self.etiqueta_nombre_anituguo.grid(row=2, column=0)  # Posicionamiento a traves de grid

        # Entry Nombre antiguo (texto que no se podra modificar)
        self.input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre),
                                        state='readonly')
        self.input_nombre_antiguo.grid(row=2, column=1)

        # Label Nombre nuevo
        self.etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo: ")
        self.etiqueta_nombre_nuevo.grid(row=3, column=0)

        # Entry Nombre nuevo (texto que si se podra modificar)
        self.input_nombre_nuevo = Entry(frame_ep)
        self.input_nombre_nuevo.grid(row=3, column=1)
        self.input_nombre_nuevo.focus()  # Para que el foco del raton vaya a este Entry al inicio

        # Label Precio antiguo
        self.etiqueta_precio_anituguo = Label(frame_ep, text="Precio antiguo: ")  #Etiqueta de texto ubicada en el frame
        self.etiqueta_precio_anituguo.grid(row=4, column=0)  # Posicionamiento a traves de grid
        # Entry Precio antiguo (texto que no se podra modificar)
        self.input_precio_antiguo = Entry(frame_ep,textvariable=StringVar(self.ventana_editar, value=old_precio),
                                          state='readonly')
        self.input_precio_antiguo.grid(row=4, column=1)

        # Label Precio nuevo
        self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ")
        self.etiqueta_precio_nuevo.grid(row=5, column=0)
        # Entry Precio nuevo (texto que si se podra modificar)
        self.input_precio_nuevo = Entry(frame_ep)
        self.input_precio_nuevo.grid(row=5, column=1)
        # Boton Actualizar Producto
        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto",command=lambda:
        self.actualizar_productos(self.input_nombre_nuevo.get(),self.input_nombre_antiguo.get(),self.input_precio_nuevo.get(),
         self.input_precio_antiguo.get()))

        self.boton_actualizar.grid(row=6, columnspan=2, sticky=W + E)
    def actualizar_productos(self, nuevo_nombre, antiguo_nombre, nuevo_precio, antiguo_precio):
        producto_modificado = False
        query = 'UPDATE producto SET nombre = ?, precio = ? WHERE nombre = ? AND precio = ?'
        if nuevo_nombre != '' and nuevo_precio != '':
                # Si el usuario escribe nuevo nombre y nuevo precio, se cambian ambos
            parametros = (nuevo_nombre, nuevo_precio, antiguo_nombre, antiguo_precio)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '':
            # Si el usuario deja vacio el nuevo precio, se mantiene el pecio anterior
            parametros = (nuevo_nombre, antiguo_precio, antiguo_nombre,
                              antiguo_precio)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '':
            # Si el usuario deja vacio el nuevo nombre, se mantiene el nombre anterior
            parametros = (antiguo_nombre, nuevo_precio, antiguo_nombre,
                              antiguo_precio)
            producto_modificado = True
        if (producto_modificado):
            self.db_consulta(query, parametros)  # Ejecutar la consulta
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} ha sido actualizado con éxito'.format(antiguo_nombre)
            # Mostrar mensaje para el usuario
            self.get_productos()  # Actualizar la tabla de productos
        else:
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} NO ha sido actualizado'.format(antiguo_nombre)
            # Mostrar mensaje para el usuario

if __name__ == '__main__':
    root = Tk() #nstancia de la ventana principal
    app = Producto(root)
    root.mainloop() # Esta línea mantiene la ventana abierta hasta que la cerremos nosotros