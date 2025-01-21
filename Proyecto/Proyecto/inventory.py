from tkinter import*
from PIL import Image,ImageTk  
class IMS:
    def __init__(self,root):    #ventana
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Atlas | Gestor de Inventario")
        self.root.config(bg="white")
 
      #======titulo===================
        self.icon_title=PhotoImage(file="") #=====se necesita un icono bonito
        title=Label(self.root,text="Atlas",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)
 
      #=====boton de logout==========
        btn_logout=Button(self.root,text="Logout",font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1150,y=10,height=50,width=150)
      
      #=====clock/reloj=====================
        self.lbl_clock=Label(self.root,text="Bienvenido a Atlas\t\t Date:DD-MM-YYYY\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
        
      #======Menu izquierdo=============
        self.MenuLogo=Image.open("logo.png") ##====otra imagen
        self.MenuLogo=self.MenuLogo.resize((200,200),Image.Resampling.LANCZOS)
        self.MenuLogo=ImageTk.PhotoImage( self.MenuLogo)
        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=102,width=200,height=565)
        
        lbl_menulogo=Label(LeftMenu,image=self.MenuLogo)
        lbl_menulogo.pack(side=TOP,fill=X)

        #==========botones izquierdos=========
        lbl_menu=Label(LeftMenu,text="Menu",font=("times new roman",20),bg="#009688").pack(side=TOP,fill=X)
        
        btn_empleados=Button(LeftMenu,text="Empleados",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_proveedor=Button(LeftMenu,text="Proveedor",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_categoria=Button(LeftMenu,text="Categorias",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_productos=Button(LeftMenu,text="Productos",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_ventas=Button(LeftMenu,text="Ventas",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_salir=Button(LeftMenu,text="salir",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)

        #=========Contenido================
        self.lbl_empleados=Label(self.root,text="Total de Empleados\n [ 0 ]",bd=5,relief=RIDGE,bg="#607d8d",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_empleados.place(x=300,y=120,height=150,width=300)
        
        self.lbl_proveedor=Label(self.root,text="Total de Proveedores\n [ 0 ]",bd=5,relief=RIDGE,bg="#607d8d",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_proveedor.place(x=650,y=120,height=150,width=300)
        
        self.lbl_categoria=Label(self.root,text="Catedoria\n [ 0 ]",bd=5,relief=RIDGE,bg="#607d8d",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_categoria.place(x=1000,y=120,height=150,width=300)
        
        self.lbl_productos=Label(self.root,text="Productos\n [ 0 ]",bd=5,relief=RIDGE,bg="#607d8d",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_productos.place(x=300,y=300,height=150,width=300)
        
        self.lbl_ventas=Label(self.root,text="Total de Ventas\n [ 0 ]",bd=5,relief=RIDGE,bg="#607d8d",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_ventas.place(x=650,y=300,height=150,width=300)
        
        
        #=====pie de pagina=====================
        lbl_footer=Label(self.root,text="Tu gestor de inventario preferido | Developed By fulanito y mangito\n For any Technical Issue Contact: 987xx00",font=("times new roman",12),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)
      
        
root=Tk()
obj=IMS(root)
root.mainloop()