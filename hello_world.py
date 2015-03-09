# s placed into public domain by anatoly techtonik
# Feel free to copy/paste wherever you like

# Absolutely minimal example of PySide application with button

from PySide.QtGui import QApplication, QPushButton

app = QApplication([])

# Create button (which is also top level window)
button = QPushButton('Exit')
# app.exit() is a method called to terminate application for
# whatever reason you like. Here we instruct to call this method
# when the button is clicked
button.clicked.connect(app.exit)
# 'clicked' is a _signal_, which we _connect_ to a method that we
# want to be called when signal fires
button.show()

# IMPORTANT: remember to assign GUI elements to variables or they
# will be destroyed by PySide automatically

app.exec_()
