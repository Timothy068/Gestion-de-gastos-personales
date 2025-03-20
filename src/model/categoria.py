class Categoria:
    def __init__(self, id: int, nombre: str, descripcion: str):
        if not nombre or not nombre.isalnum():
            raise ValueError("El nombre de la categoría no puede estar vacío y debe ser alfanumérico")
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion


