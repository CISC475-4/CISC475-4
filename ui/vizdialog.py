from PySide import QtGui, QtCore
from PySide.QtCore import SIGNAL, SLOT


class AddGraphDialog(QtGui.QDialog):

    child_ids = []
    session_ids = []
    behaviors = []

    def __init__(self, parent=None):
        super(AddGraphDialog, self).__init__(parent)
        self.setup()

    def setup(self):

        # set title
        self.setWindowTitle('Add Graph')

        # ----------------------------------------------------------------------------
        # child id combobox
        # ----------------------------------------------------------------------------
        
        # child choicebox
        self.combobox_child = QtGui.QComboBox(self)
        # attach handler for when child id combobox is changed
        self.combobox_child.activated[str].connect(self.on_child_id_change)
        # combobox label
        self.child_label = QtGui.QLabel('Child:', self)

        # ----------------------------------------------------------------------------
        # session id combobox
        # ----------------------------------------------------------------------------

        # session choicebox
        self.combobox_session = QtGui.QComboBox(self)
        # self.combobox_session.addItems(self.spam_list)
        # session label
        self.session_label = QtGui.QLabel('Session:', self)

        # ----------------------------------------------------------------------------
        # behavior combobox
        # ----------------------------------------------------------------------------

        # behavior choicebox
        self.combobox_behavior = QtGui.QComboBox(self)
        # behavior label
        self.behavior_label = QtGui.QLabel('Behavior:', self)

        # ----------------------------------------------------------------------------
        # Ok Button
        # ----------------------------------------------------------------------------

        # ok button
        self.ok_button = QtGui.QPushButton('OK', self)
        self.ok_button.clicked.connect(self.ok_on_click)

        # ----------------------------------------------------------------------------
        # Cancel button
        # ----------------------------------------------------------------------------

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

        # ----------------------------------------------------------------------------
        # Data initialization
        # ----------------------------------------------------------------------------
        # get child ids from the DB
        child_ids_int = self.parent().controller.get_all_child_ids()
        # convert ids from int to str
        self.child_ids = [str(child_id) for child_id in child_ids_int]
        # add child ids to combobox
        self.combobox_child.addItems(self.child_ids)
        # set the session id based on the first child id
        if len(self.child_ids) > 0:
            self.on_child_id_change(self.child_ids[0]) 

        # TODO: get the behaviors dynamically
        self.behaviors = ['1', '2', '3', 'combo (1 + 2 + 3)']
        self.combobox_behavior.addItems(self.behaviors)

    def ok_on_click(self):
        child_id = self.combobox_child.currentText()
        session_id = self.combobox_session.currentText()
        behavior = self.combobox_behavior.currentText()

        print (child_id, session_id, behavior)
        # TODO: 
        # self.parent.graph_area.add_graph()
        self.close()
    
    def on_child_id_change(self, child_id):
        """
        Called when the child id combobox value changes
        """
        # query the db for the session ids
        session_ids_int = self.parent().controller.get_all_sessions_for_child(child_id)
        self.session_ids = [str(session_id) for session_id in session_ids_int]
        self.combobox_session.clear()
        self.combobox_session.addItems(self.session_ids)

