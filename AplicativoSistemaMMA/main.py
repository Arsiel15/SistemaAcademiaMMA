from database.database import crear_base_datos
from views.login import LoginWindow

crear_base_datos()

app = LoginWindow()
app.run()