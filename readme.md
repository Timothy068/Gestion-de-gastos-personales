# Gestión de gastos personales

El objetivo de nuestro proyecto es:

Desarrollar una aplicación que permita a los usuarios llevar un 
control detallado de sus finanzas personales, registrando ingresos, gastos y analizando su situación 
financiera.

La aplicación debe tener las siguientes funcionalidades:

1. Registrar una transacción: El sistema debe poder permitir a los usuarios registrar una 
transacción de dinero, sea un ingreso o egreso de su cuenta.  
2. Actualizar transacción: El sistema debe permitir a los usuarios modificar una transacción 
existente 
3. Visualizar transacciones: El sistema debe permitir graficar la cantidad de dinero ingresado 
y gastado en un rango de fechas dado, agrupando por categorías.  
4. Iniciar sesión: La aplicación debe permitir a los usuarios iniciar sesión en el sistema con un 
usuario ya existente 
5. Crear cuenta: Los usuarios deben poder darse de alta en el sistema 
6. Cambiar contraseña: El sistema debe permitir a los usuarios cambiar sus contraseñas 
cuando ellos lo deseen.  

Una transacción debe estar compuesta por los siguientes datos: 

1. Cantidad de dinero implicado en la transacción 
2. Categoría de la transacción 
3. Fecha y hora de la transacción  
4. Usuario que creó la transacción 

Nota: Cada usuario al crear su cuenta e iniciar sesión debe poder ver sus transacciones y solo sus 
transacciones, no las transacciones creadas por los otros usuarios. 

## Diagrama UML

![alt text](<assets/gestion de recursos personales.png>)

## Implementacion de las pruebas

### **Registrar transaccion**

Pruebas Normales

| #  | Descripción                                       | Datos de entrada                                         | Resultado esperado        |
|----|-------------------------------------------------|---------------------------------------------------------|---------------------------|
| 1  | Registrar una transacción válida               | Cantidad: 100.0, Tipo: "Ingreso", Categoría: "Alimentación" | Transacción | 
|    |                                                |                                                             | registrada   |
| 2  | Registrar un gasto válido                      | Cantidad: 50.0, Tipo: "Egreso", Categoría: "Transporte" | Transacción |
|    |                                                |                                                         | registrada   |
| 3  | Registrar transacción sin categoría específica | Cantidad: 75.0, Tipo: "Ingreso", Categoría: None       | Transacción |
|                                                     |                                                         registrada   |

Pruebas Extremas

| #  | Descripción                                      | Datos de entrada                     | Resultado esperado        |
|----|------------------------------------------------|--------------------------------------|---------------------------|
| 4  | Registrar transacción con cantidad extrema      | Cantidad: 1,000,000,000.0           | Transacción registrada   |
| 5  | Registrar transacción con cantidad negativa     | Cantidad: -500.0                    | Lanza CantidadNegativaError |
| 6  | Registrar transacción con fecha futura         | Fecha: 2050-01-01                   | Lanza FechaFuturaError   |

Pruebas de Error

| #  | Descripción                                  | Datos de entrada                           | Resultado esperado            |
|----|--------------------------------------------|------------------------------------------|-------------------------------|
| 7  | Registrar transacción con tipo inválido   | Cantidad: 100.0, Tipo: "Donación"        | Lanza TipoTransaccionInvalidoError |
| 8  | Registrar transacción sin cantidad        | Cantidad: None, Tipo: "Ingreso"          | Lanza CamposVaciosError       |
| 9  | Registrar transacción sin usuario         | Usuario: None, Cantidad: 50.0, Tipo: "Egreso" | Lanza UsuarioNoEncontradoError |


### **Actualizar transaccion**

Pruebas Normales

| #  | Descripción                                  | Datos de entrada                                   | Resultado esperado        |
|----|--------------------------------------------|--------------------------------------------------|---------------------------|
| 1  | Actualizar la cantidad de una transacción | Nueva cantidad: 200.0                            | Transacción actualizada   |
| 2  | Cambiar la categoría de la transacción    | Nueva categoría: "Transporte"                    | Transacción actualizada   |
| 3  | Cambiar el tipo de la transacción         | Nuevo tipo: "Egreso"                             | Transacción actualizada   |

Pruebas Extremas

| #  | Descripción                                      | Datos de entrada                           | Resultado esperado        |
|----|------------------------------------------------|------------------------------------------|---------------------------|
| 4  | Actualizar cantidad con un valor extremo       | Nueva cantidad: 1,000,000,000.0         | Transacción actualizada   |
| 5  | Actualizar fecha a una fecha futura           | Nueva fecha: 2050-01-01                 | Lanza FechaFuturaError    |
| 6  | Actualizar cantidad a un valor negativo       | Nueva cantidad: -300.0                  | Lanza CantidadNegativaError |

Pruebas de Error

| #  | Descripción                                  | Datos de entrada                           | Resultado esperado               |
|----|--------------------------------------------|------------------------------------------|---------------------------------|
| 7  | Intentar actualizar una transacción inexistente | ID de transacción: 9999                 | Lanza TransaccionNoEncontradaError |
| 8  | Intentar actualizar sin proporcionar datos  | Ningún cambio realizado                  | Lanza CamposVaciosError        |
| 9  | Intentar cambiar a una categoría inválida   | Nueva categoría: None                    | Lanza CategoriaInvalidaError   |

### **Visualizar transacciones**

Pruebas Normales

| #  | Descripción                                      | Datos de entrada                             | Resultado esperado        |
|----|------------------------------------------------- |--------------------------------------------------------------------------|
| 1  | Visualizar transacciones en un rango válido  |  Fecha inicio: "2024-01-01", Fecha fin: "2024-01-31" | Transacciones |
|    |                                              |                                                      | mostradas   |
| 2  | Filtrar por categoría específica               | Categoría: "Alimentación"                           | Transacciones |
|    |                                                |                                                     |mostradas   |
| 3  | Visualizar solo transacciones de hoy          | Fecha: "2024-06-10" ("hoy")                          | Transacciones |
|    |                                               |                                                      |mostradas   |

Pruebas Extremas

| #  | Descripción                                      | Datos de entrada                     | Resultado esperado        |
|----|------------------------------------------------|--------------------------------------|---------------------------|
| 4  | Visualizar en un rango extremadamente amplio  | Fecha inicio: "2000-01-01", Fecha fin: "2100-12-31" | Transacciones mostradas   |
| 5  | Visualizar transacciones de un solo día       | Fecha inicio y fin: "2024-06-01"          | Transacciones mostradas   |
| 6  | Consultar con fechas invertidas               | Fecha inicio: "2024-06-10", Fecha fin: "2024-06-01" | Lanza 
|    |                                               |                                                     | RangoFechasInvalidoError |

Pruebas de Error

| #  | Descripción                                     | Datos de entrada                                  | Resultado esperado             |
|----|-----------------------------------------------|-------------------------------------------------|-------------------------------|
| 7  | Intentar visualizar con fechas inválidas     | Fecha inicio: "fecha_invalida", Fecha fin: "2024-06-01" | Lanza 
|    |                                              |                                                         |FechaInvalidaError     |
| 8  | Intentar visualizar sin proporcionar fechas  | Fecha inicio y fin: None                        | Lanza CamposVaciosError       |
| 9  | Intentar visualizar con caracteres especiales | Fecha inicio: "@#$$%", Fecha fin: "2024-06-01" | Lanza FechaInvalidaError     |

### **Iniciar sesion**

Pruebas Normales

| #  | Descripción                                 | Datos de entrada                                | Resultado esperado        |
|----|-------------------------------------------|------------------------------------------------|---------------------------|
| 1  | Iniciar sesión con credenciales válidas  | Correo: "juan@example.com", Contraseña: "1234" | Sesión iniciada           |
| 2  | Iniciar sesión con otro usuario          | Correo: "maria@example.com", Contraseña: "abcd"| Sesión iniciada           |
| 3  | Iniciar sesión inmediatamente después de registrarse | Correo: "carlos@example.com", Contraseña: "xyz" | Sesión 
|    |                                                      |                                                 |iniciada           |

Pruebas Extremas

| #  | Descripción                                      | Datos de entrada                           | Resultado esperado        |
|----|------------------------------------------------|------------------------------------------|-------------------------------|
| 4  | Iniciar sesión con contraseña extremadamente larga | Contraseña: "A" * 100                 | Sesión iniciada           |
| 5  | Iniciar sesión con caracteres especiales        | Correo: "user!@example.com", Contraseña: "Clave$123" | Sesión 
|    |                                                 |                                                      | iniciada         |
| 6  | Iniciar sesión con nombre de usuario largo     | Correo: "usuario_largo@example.com", Contraseña: "pass" | Sesión 
|    |                                                |                                                         |iniciada           |

Pruebas de Error

| #  | Descripción                               | Datos de entrada                                | Resultado esperado           |
|----|-----------------------------------------|------------------------------------------------|-----------------------------|
| 7  | Intentar iniciar sesión con usuario inexistente | Correo: "desconocido@example.com", Contraseña: "1234" | Lanza 
|    |                                                 |                                                    | UsuarioNoEncontradoError |
| 8  | Intentar iniciar sesión con contraseña incorrecta | Correo: "juan@example.com", Contraseña: "claveErronea" | Lanza |
|    |                                                    |                                                 |ContrasenaIncorrectaError |
| 9  | Intentar iniciar sesión sin datos       | Correo: "", Contraseña: ""                      | Lanza CamposVaciosError      |

### **Crear cuenta**

Pruebas Normales

| #  | Descripción                             | Datos de entrada                                    | Resultado esperado        |
|----|----------------------------------------|---------------------------------------------------|---------------------------|
| 1  | Crear cuenta con datos válidos        | Nombre: "Juan", Correo: "juan@example.com"        | Cuenta creada            |
| 2  | Crear múltiples cuentas                | Nombres: "María", "Carlos", Correos diferentes   | Cuentas creadas          |
| 3  | Crear cuenta sin nombre               | Correo: "anonimo@example.com"                     | Cuenta creada            |

Pruebas Extremas

| #  | Descripción                                 | Datos de entrada                         | Resultado esperado        |
|----|-------------------------------------------|------------------------------------------|---------------------------|
| 4  | Crear cuenta con nombre muy largo        | Nombre: 300 caracteres                  | Cuenta creada            |
| 5  | Crear cuenta con correo muy largo       | Correo: 250 caracteres + "@example.com" | Cuenta creada            |
| 6  | Crear cuenta con caracteres especiales  | Nombre: "Usuario#1!", Correo: "user!@ex.com" | Cuenta creada            |


Pruebas de Error

| #  | Descripción                           | Datos de entrada                           | Resultado esperado               |
|----|-------------------------------------|------------------------------------------|---------------------------------|
| 7  | Intentar crear cuenta sin correo   | Nombre: "Juan", Correo: ""               | Lanza CamposVaciosError        |
| 8  | Intentar crear cuenta sin contraseña | Correo: "juan@example.com", Contraseña: "" | Lanza CamposVaciosError        |
| 9  | Intentar crear cuenta con correo ya registrado | Correo: "juan@example.com"            | Lanza CorreoYaRegistradoError  |

### **Cambiar contraseña**

Pruebas Normales

| #  | Descripción                                    | Datos de entrada                                     | Resultado |
|    |                                                |                                                      | esperado  |
|----|----------------------------------------------|----------------------------------------------------|---------------------------|
| 1  | Cambiar contraseña con datos válidos        | Correo: "juan@example.com", Nueva contraseña: "Segura1234" | Contraseña   |
|    |                                             |                                                            |actualizada   |
| 2  | Cambiar contraseña dos veces seguidas       | Correo: "juan@example.com", Nueva: "Clave1", Luego: "Clave2" | Contraseña |
|    |                                             |                                                              |actualizada   |
| 3  | Cambiar contraseña después de crear cuenta  | Correo: "maria@example.com", Nueva contraseña: "Clave789" | Contraseña |
|    |                                             |                                                           | actualizada   |

Pruebas Extremas

| #  | Descripción                                        | Datos de entrada                                 | Resultado esperado        |
|----|--------------------------------------------------|----------------------------------------------|---------------------------|
| 4  | Cambiar contraseña a una extremadamente larga   | Nueva contraseña: 100 caracteres            | Contraseña actualizada   |
| 5  | Cambiar contraseña con caracteres especiales    | Nueva contraseña: "Clave$%&/()=?"           | Contraseña actualizada   |
| 6  | Intentar cambiar contraseña a la misma          | Nueva contraseña: "Password123" (misma anterior) | Lanza |
|                                                      |                                             |  ContrasenaInseguraError |

Pruebas de Error

| #  | Descripción                                        | Datos de entrada                                 | Resultado 
|                                                         |                                                  |esperado               |
|----|--------------------------------------------------|----------------------------------------------------------------------------|
| 7  | Intentar cambiar contraseña de usuario inexistente | Correo: "desconocido@example.com", Nueva: "NuevaClave" | Lanza |
|    |                                                    |                                       |UsuarioNoEncontradoError  |
| 8  | Intentar cambiar contraseña sin ingresar datos    | Correo: "", Nueva contraseña: ""            | Lanza |
|    |                                                   |                                             |CamposVaciosError        |
| 9  | Intentar cambiar contraseña sin nueva contraseña  | Correo: "juan@example.com", Nueva: ""       | Lanza |
|    |                                                   |                                             |CamposVaciosError        |


