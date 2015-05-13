from PySide import QtGui, QtCore

class AddGraphDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super(AddGraphDialog, self).__init__(parent)
        self.setup()

    def setup(self):

        # set title
        self.setWindowTitle('Add Graph')

        self.spam_list = ['cheese balls', 'fries', 'egg muffins']
        self.spam_list2 = ['cheese balls', 'fries', 'egg muffins']
        self.spam_list3 = ['cheese balls', 'fries', 'egg muffins']

        self.child_ids = self.parent().controller.get_all_child_ids()
        print(self.child_ids)
        
        # child choicebox
        self.combobox_child = QtGui.QComboBox(self)
        self.combobox_child.addItems(self.child_ids)
        # choicebox label
        self.child_label = QtGui.QLabel('Child:', self)

        # session choicebox
        self.combobox_session = QtGui.QComboBox(self)
        self.combobox_session.addItems(self.spam_list)
        # session label
        self.session_label = QtGui.QLabel('Session:', self)

        # behavior choicebox
        self.combobox_behavior = QtGui.QComboBox(self)
        self.combobox_behavior.addItems(self.spam_list)
        # behavior label
        self.behavior_label = QtGui.QLabel('Behavior:', self)

        # ok button
        self.ok_button = QtGui.QPushButton('OK', self)
        self.ok_button.clicked.connect(self.ok_on_click)

        # cancel button
        self.cancel_button = QtGui.QPushButton('Cancel', self)        
        self.cancel_button.clicked.connect(self.close)

        # ----------------------------------------------------------------------------
        # Layout
        # ----------------------------------------------------------------------------

        self.horizontal_layout = QtGui.QHBoxLayout()
        self.horizontal_layout.addStretch(1)
        self.horizontal_layout.addWidget(self.ok_button)
        self.horizontal_layout.addWidget(self.cancel_button)

        # add vertical layout
        self.vertical_layout = QtGui.QVBoxLayout()
        self.vertical_layout.addStretch(1)

        self.vertical_layout.addWidget(self.child_label)
        self.vertical_layout.addWidget(self.combobox_child)
        self.vertical_layout.addWidget(self.session_label)
        self.vertical_layout.addWidget(self.combobox_session)
        self.vertical_layout.addWidget(self.behavior_label)
        self.vertical_layout.addWidget(self.combobox_behavior)

        self.setLayout(self.vertical_layout)
        self.vertical_layout.addLayout(self.horizontal_layout)      

    def ok_on_click(self):
        child = self.combobox_child.currentText()
        session = self.combobox_session.currentText()
        behavior = self.combobox_behavior.currentText()

        # TODO: self.parent.graph_area.add_graph()
        


