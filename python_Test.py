from PySide.QtGui import *
from PySide.QtCore import *
import os
import sys

 
class Panel(QWidget):
    def __init__(self):
        super(Panel, self).__init__()


        ###### Shot and project info
        self.project = QComboBox()
        self.sequence = QComboBox()
        self.shot = QComboBox()
        self.task = QComboBox()
        self.step = QComboBox()
        self.publishFolder = QLabel()

        self.projectId = None
        self.sequenceId = None
        self.shotId = None
        self.taskId = None

        # self.fill_project()
        # self.fill_step()

        # Signals
        self.project.currentIndexChanged.connect(self.fill_sequence)
        self.sequence.currentIndexChanged.connect(self.fill_shot)
        self.shot.currentIndexChanged.connect(self.fill_task)


        projLab = QLabel('Project')
        seqLab = QLabel('Sequence')
        shotLab = QLabel('Shot')
        taskLab = QLabel('Task')
        stepLab = QLabel('Step')
        foldLab = QLabel('Publish folder')

        shotInfoLay = QGridLayout()
        shotInfoLay.addWidget(projLab, 0, 0)
        shotInfoLay.addWidget(self.project, 0, 1)
        shotInfoLay.addWidget(seqLab, 1, 0)
        shotInfoLay.addWidget(self.sequence, 1, 1)
        shotInfoLay.addWidget(shotLab, 2, 0)
        shotInfoLay.addWidget(self.shot, 2, 1)
        shotInfoLay.addWidget(taskLab, 3, 0)
        shotInfoLay.addWidget(self.task, 3, 1)
        shotInfoLay.addWidget(stepLab, 4, 0)
        shotInfoLay.addWidget(self.step, 4, 1)
        shotInfoLay.addWidget(foldLab, 5, 0)
        shotInfoLay.addWidget(self.publishFolder, 5, 1)

        ##### Other stuff
        self.comment = QTextEdit('Comment here')
        comLab = QLabel('Comment')

        ##### Create and add to main layout
        info_layout = QVBoxLayout()   
        info_layout.addLayout(shotInfoLay)   
        info_layout.addWidget(comLab) 
        info_layout.addWidget(self.comment) 

        ##### List renders
        renders_label = QLabel('Renders:')
        self.render_list = QListWidget()
        renders_lay = QVBoxLayout()
        renders_lay.addWidget(renders_label)
        renders_lay.addWidget(self.render_list)

        main_layout = QHBoxLayout()
        main_layout.addLayout(renders_lay)
        main_layout.addLayout(info_layout)

        ##### Set stuff
        self.setAcceptDrops(True)
        self.setLayout(main_layout)
        self.setWindowTitle('Publish renders')
        self.set_style()

    def dragEnterEvent(self, e):
        path = e.mimeData().urls()[0].path()
        if os.path.isdir(path[1:]):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        try:
            path = e.mimeData().urls()[0].path()[1:]
            self.publishFolder.setText(path)
            split = path.split('/')
            self.projTry = split[1] 
            self.seqTry = split[3] 
            self.shotTry = split[4] 
            self.comment.setText('%s %s %s' % (self.projTry, self.seqTry, self.shotTry))
            self.fill_project()
        except:
            pass

    def fill_project(self):
        
        allProjs = query.get_all_projects(active=True)
        self.project.blockSignals(True)

        self.project.clear()
        
        projectNames = []
        for project in allProjs:
            projectNames.append(unicode(project['name']))

        self.project.addItem('--Select project--')

        for proj in sorted(projectNames, key=lambda v: v.upper()):
            self.project.addItem(proj.lower())

        try:
            index = self.project.findText(self.projTry.lower())

        except Exception,e:
            index = None
            print 'Error setting project', e
            pass

        if index == -1 or index == None:
            self.project.setCurrentIndex(1)
            self.project.blockSignals(False)
            self.project.setCurrentIndex(0)
            
        else:
            self.project.blockSignals(False)
            self.project.setCurrentIndex(index)
            self.projTry = None
            
    def fill_sequence(self):
        print "SEQ"
        return
        self.sequence.clear()
        try:
            self.projectId = query.get_project_id_by_name(self.project.currentText())['id']
        except Exception,e:
            print 'Error getting projectId',e
            return

        self.sequence.blockSignals(True)

        self.sequence.clear()

        allSeqs = query.get_all_sequences_by_project_id(self.projectId)

        sequenceNames = []
        for sequence in allSeqs:
            sequenceNames.append(unicode(sequence['code']))

        for seq in sorted(sequenceNames, key=lambda v: v.upper()):
            self.sequence.addItem(seq)


        try:
            index = self.sequence.findText(self.seqTry)

        except Exception,e:
            index = None
            print 'Error setting sequence', e
            pass

        if index == -1 or index == None:
            self.sequence.setCurrentIndex(1)
            self.sequence.blockSignals(False)
            self.sequence.setCurrentIndex(0)
        else:
            self.sequence.setCurrentIndex(-1)
            self.sequence.blockSignals(False)
            self.sequence.setCurrentIndex(index)
            self.seqTry = None

    def fill_shot(self):
        print "SHOT"
        return
        self.shot.clear()
        try:
            query.get_sequence_id_by_name(self.projectId, self.sequence.currentText())['id']
        except Exception,e:
            print 'Error getting seq id', e
            return

        self.shot.blockSignals(True)
            
        self.shot.clear()
        self.sequenceId = query.get_sequence_id_by_name(self.projectId, self.sequence.currentText())['id']
        allShots = query.get_all_shots_by_sequence_id(self.projectId, self.sequenceId)

        shotNames = []
        for shot in allShots:
            shotNames.append(unicode(shot['code']))

        for shot in sorted(shotNames, key=lambda v: v.upper()):
            self.shot.addItem(shot)


        try:
            index = self.shot.findText(self.shotTry)

        except Exception,e:
            index = None
            print 'Error setting shot', e
            pass

        if index == -1 or index == None:
            self.shot.setCurrentIndex(1)
            self.shot.blockSignals(False)
            self.shot.setCurrentIndex(0)
        else:
            self.shot.blockSignals(False)
            self.shot.setCurrentIndex(index)
            self.shotTry = None

    def fill_task(self):
        print "TASK"
        return
        self.task.clear()
        try:
            query.get_shot_id_by_name(self.projectId, self.sequenceId, self.shot.currentText())['id']
        except Exception, e:
            print 'Error getting shot id', e
            return

            
        self.task.clear()
        self.shotId = query.get_shot_id_by_name(self.projectId, self.sequenceId, self.shot.currentText())['id']
        allTasks = query.get_all_tasks_by_shot_id(self.projectId, self.sequenceId, self.shotId)

        taskNames = []
        for task in allTasks:
            taskNames.append(task['content'])

        for task in sorted(taskNames, key=lambda v: v.upper()):
            self.task.addItem(task)

    def fill_step(self):
        print "STEP"
        return
        stepList = sorted(['Mm', 'Lgt', 'Anim', 'Layout', 'Comp', 'Fx'])
        for step in stepList:
            self.step.addItem(step)

    def set_style(self):
        text = open('Y:/CHIMNEY_CONFIG/nuke/projects/stockholm/chimneyPySide/style_dark.txt').read()
        self.setStyleSheet(text)

def run():
    app = QApplication(sys.argv)
    run.panel = Panel()
    run.panel.show()
    app.exec_()
run()