from PySide import QtGui, QtCore
from PySide.QtCore import SIGNAL, SLOT

# Constant
COMBO_3_BEHAVIOR = "Multi System"


class AddGraphDialog(QtGui.QDialog):
    """
    The UI class for the dialog box used to add a graph.
    """

    # Lists to hold the options for the comboboxes
    child_ids = []
    session_ids = []
    behaviors = []

    def __init__(self, parent=None):
        super(AddGraphDialog, self).__init__(parent)
        self.setup()

    def setup(self):
        """
        Code to setup the initial add graph dialog
        """

        # set title of the dialog
        self.setWindowTitle('Add Graph')

        # ----------------------------------------------------------------------------
        # child id combobox
        # ----------------------------------------------------------------------------
        
        # child combobox
        self.combobox_child = QtGui.QComboBox(self)
        # attach handler to be called when child id combobox is changed
        self.combobox_child.activated[str].connect(self.on_child_id_change)
        # child id combobox label
        self.child_label = QtGui.QLabel('Child:', self)

        # ----------------------------------------------------------------------------
        # session id combobox
        # ----------------------------------------------------------------------------

        # session combobox
        self.combobox_session = QtGui.QComboBox(self)
        self.combobox_session.activated.connect(lambda: self.on_session_id_change(self.combobox_child.currentText(),
            self.combobox_session.currentText()))
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
        # attach event handler to the ok button
        self.ok_button.clicked.connect(self.ok_on_click)

        # ----------------------------------------------------------------------------
        # Cancel button
        # ----------------------------------------------------------------------------

        # cancel button
        self.cancel_button = QtGui.QPushButton('Cancel', self)
        # attach event handler to close the dialog when the cancel button is clicked        
        self.cancel_button.clicked.connect(self.close)

        # ----------------------------------------------------------------------------
        # Layout
        # ----------------------------------------------------------------------------

        # Setup the buttons section
        self.horizontal_layout = QtGui.QHBoxLayout()
        self.horizontal_layout.addStretch(1)
        self.horizontal_layout.addWidget(self.ok_button)
        self.horizontal_layout.addWidget(self.cancel_button)

        # add vertical layout
        self.vertical_layout = QtGui.QVBoxLayout()
        
        # Setup the main content of the dialog box
        self.vertical_layout.addWidget(self.child_label)
        self.vertical_layout.addWidget(self.combobox_child)
        self.vertical_layout.addWidget(self.session_label)
        self.vertical_layout.addWidget(self.combobox_session)
        self.vertical_layout.addWidget(self.behavior_label)
        self.vertical_layout.addWidget(self.combobox_behavior)
        self.vertical_layout.addStretch(1)

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
            # set the behaviors based on child_id and session_id
            if len(self.session_ids) > 0:
                self.on_session_id_change(self.child_ids[0], self.session_ids[0])


    def ok_on_click(self):
        """
        Steps to be performed when the okay button is clicked
        """
        # Get the values from the comboboxes
        child_id = self.combobox_child.currentText()
        session_id = self.combobox_session.currentText()
        behavior = self.combobox_behavior.currentText()

        # Add the graph
        # If we want all behaviors together
        if behavior == COMBO_3_BEHAVIOR:
            self.parent().graph_area.add_multisystem_graph(child_id, session_id)
        # If only one specific behavior was selected
        else:
            self.parent().graph_area.add_graph_with_ids(child_id, session_id, behavior)
        # Close the dialog
        self.close()
    
    def on_child_id_change(self, child_id):
        """
        Called when the child id combobox value changes.  Sets the session id combobox 
        appropriately.
        """
        # query the db for the session ids
        session_ids_int = self.parent().controller.get_all_sessions_for_child(child_id)
        self.session_ids = [str(session_id) for session_id in session_ids_int]
        self.combobox_session.clear()
        self.combobox_session.addItems(self.session_ids)

    def on_session_id_change(self, child_id, session_id):
        self.behaviors = self.parent().controller.get_behavior_types(child_id, session_id)
        self.behaviors.append(COMBO_3_BEHAVIOR)
        self.combobox_behavior.clear()
        self.combobox_behavior.addItems(self.behaviors)

