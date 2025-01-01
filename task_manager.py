from datetime import datetime
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QListWidget, QVBoxLayout)

class TaskManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def add_task(self):
        task = self.task_input.text()
        deadline = self.deadline_input.text()
        importance = self.importance_input.text()
        if task and deadline and importance:
            priority = self.calculate_priority(deadline, importance)
            # Store the task, deadline, importance, and priority together (e.g., in a dictionary or a custom class)
            self.task_list.addItem(f"{task} (Priority: {priority})")  # Display priority for now
            self.task_input.clear()
        self.task_list.sortItems() 
            
    def calculate_priority(self, deadline, importance):
        today = datetime.now().date()
        deadline_date = datetime.strptime(deadline, '%Y-%m-%d').date()
        days_remaining = (deadline_date - today).days

        urgency_score = 10 - days_remaining  # Example urgency calculation
        importance_score = {'High': 3, 'Medium': 2, 'Low': 1}.get(importance, 1)

        priority = urgency_score * importance_score
        return priority
    
    def initUI(self):
        self.setWindowTitle('Agentic Task Manager')
        self.setGeometry(100, 100, 400, 300)

        self.task_label = QLabel('Enter new task:')
        self.task_input = QLineEdit()
        self.add_button = QPushButton('Add Task')
        self.task_list = QListWidget()
        
        self.deadline_label = QLabel('Deadline (YYYY-MM-DD):')
        self.deadline_input = QLineEdit()
        self.importance_label = QLabel('Importance (High, Medium, Low):')
        self.importance_input = QLineEdit()  # Or use a QComboBox for dropdown

        self.add_button.clicked.connect(self.add_task)

        vbox = QVBoxLayout()
        vbox.addWidget(self.task_label)
        vbox.addWidget(self.task_input)
        vbox.addWidget(self.add_button)
        vbox.addWidget(self.task_list)
        
        vbox.addWidget(self.deadline_label)
        vbox.addWidget(self.deadline_input)
        vbox.addWidget(self.importance_label)
        vbox.addWidget(self.importance_input)

        self.setLayout(vbox)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TaskManager()
    sys.exit(app.exec_())