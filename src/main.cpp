#include <QApplication>
#include <QMainWindow>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QTextEdit>
#include <QProgressBar>
#include <QGraphicsView>
#include <QGraphicsScene>
#include <QGraphicsPixmapItem>
#include <QTimer>
#include <QPropertyAnimation>
#include <QGraphicsOpacityEffect>
#include <QProcess>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <QFile>
#include <QDir>
#include <QStandardPaths>
#include <QMessageBox>
#include <QDebug>
#include <QThread>
#include <QFont>
#include <QFontDatabase>
#include <QPalette>
#include <QStyleFactory>

class StoryEngineInterface : public QObject
{
    Q_OBJECT

public:
    explicit StoryEngineInterface(QObject *parent = nullptr);
    
    struct SceneData {
        int sceneId;
        QString background;
        QString dialogue;
        QList<QPair<QString, QString>> choices; // text, memory_type
        QString audioTrack;
    };
    
    struct MemoryData {
        double kindness;
        double obsession;
        double truth;
        double trust;
        QString alignment;
    };
    
    SceneData getCurrentScene();
    MemoryData getMemoryData();
    bool makeChoice(int choiceIndex);
    bool resetGame();
    
signals:
    void sceneChanged();
    void memoryUpdated();
    void errorOccurred(const QString &message);

private:
    QProcess *m_pythonProcess;
    QString m_pythonScriptPath;
    QString m_savePath;
    
    bool executePythonCommand(const QString &command, QJsonObject &result);
    QString getPythonScriptPath();
};

StoryEngineInterface::StoryEngineInterface(QObject *parent)
    : QObject(parent)
    , m_pythonProcess(nullptr)
    , m_savePath("save/save.json")
{
    m_pythonScriptPath = getPythonScriptPath();
}

QString StoryEngineInterface::getPythonScriptPath()
{
    QDir appDir(QApplication::applicationDirPath());
    QString scriptPath = appDir.absoluteFilePath("../python_backend/story_engine.py");
    
    if (!QFile::exists(scriptPath)) {
        // Try relative to current working directory
        scriptPath = "python_backend/story_engine.py";
    }
    
    return scriptPath;
}

bool StoryEngineInterface::executePythonCommand(const QString &command, QJsonObject &result)
{
    if (!m_pythonProcess) {
        m_pythonProcess = new QProcess(this);
        m_pythonProcess->setProcessChannelMode(QProcess::MergedChannels);
    }
    
    QStringList args;
    args << m_pythonScriptPath << command;
    
    m_pythonProcess->start("python3", args);
    
    if (!m_pythonProcess->waitForFinished(5000)) {
        emit errorOccurred("Python process timeout");
        return false;
    }
    
    if (m_pythonProcess->exitCode() != 0) {
        QString error = m_pythonProcess->readAllStandardError();
        emit errorOccurred(QString("Python error: %1").arg(error));
        return false;
    }
    
    QByteArray output = m_pythonProcess->readAllStandardOutput();
    QJsonParseError parseError;
    QJsonDocument doc = QJsonDocument::fromJson(output, &parseError);
    
    if (parseError.error != QJsonParseError::NoError) {
        emit errorOccurred(QString("JSON parse error: %1").arg(parseError.errorString()));
        return false;
    }
    
    result = doc.object();
    return true;
}

StoryEngineInterface::SceneData StoryEngineInterface::getCurrentScene()
{
    SceneData scene;
    QJsonObject result;
    
    if (executePythonCommand("get_scene", result)) {
        scene.sceneId = result["scene_id"].toInt();
        scene.background = result["background"].toString();
        scene.dialogue = result["dialogue"].toString();
        scene.audioTrack = result["audio_track"].toString();
        
        QJsonArray choicesArray = result["choices"].toArray();
        for (const QJsonValue &value : choicesArray) {
            QJsonObject choiceObj = value.toObject();
            scene.choices.append(qMakePair(
                choiceObj["text"].toString(),
                choiceObj["memory_type"].toString()
            ));
        }
    }
    
    return scene;
}

StoryEngineInterface::MemoryData StoryEngineInterface::getMemoryData()
{
    MemoryData memory;
    QJsonObject result;
    
    if (executePythonCommand("get_memory", result)) {
        memory.kindness = result["kindness"].toDouble();
        memory.obsession = result["obsession"].toDouble();
        memory.truth = result["truth"].toDouble();
        memory.trust = result["trust"].toDouble();
        memory.alignment = result["alignment"].toString();
    }
    
    return memory;
}

bool StoryEngineInterface::makeChoice(int choiceIndex)
{
    QJsonObject result;
    return executePythonCommand(QString("make_choice %1").arg(choiceIndex), result);
}

bool StoryEngineInterface::resetGame()
{
    QJsonObject result;
    return executePythonCommand("reset_game", result);
}

class CutsceneWidget : public QGraphicsView
{
    Q_OBJECT

public:
    explicit CutsceneWidget(QWidget *parent = nullptr);
    void setCutscene(const QString &imagePath);
    void fadeIn();
    void fadeOut();

private:
    QGraphicsScene *m_scene;
    QGraphicsPixmapItem *m_pixmapItem;
    QGraphicsOpacityEffect *m_opacityEffect;
    QPropertyAnimation *m_fadeAnimation;
};

CutsceneWidget::CutsceneWidget(QWidget *parent)
    : QGraphicsView(parent)
    , m_scene(new QGraphicsScene(this))
    , m_pixmapItem(nullptr)
    , m_opacityEffect(new QGraphicsOpacityEffect(this))
    , m_fadeAnimation(new QPropertyAnimation(m_opacityEffect, "opacity", this))
{
    setScene(m_scene);
    setRenderHint(QPainter::Antialiasing);
    setRenderHint(QPainter::SmoothPixmapTransform);
    setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    
    // Set up fade animation
    m_fadeAnimation->setDuration(1000);
    m_fadeAnimation->setEasingCurve(QEasingCurve::InOutQuad);
    
    setGraphicsEffect(m_opacityEffect);
    m_opacityEffect->setOpacity(0.0);
}

void CutsceneWidget::setCutscene(const QString &imagePath)
{
    QPixmap pixmap(imagePath);
    
    if (pixmap.isNull()) {
        // Create placeholder if image doesn't exist
        pixmap = QPixmap(800, 600);
        pixmap.fill(QColor(40, 40, 40));
        
        QPainter painter(&pixmap);
        painter.setPen(QPen(QColor(100, 100, 100), 2));
        painter.setFont(QFont("Arial", 24));
        painter.drawText(pixmap.rect(), Qt::AlignCenter, 
                        QString("Cutscene: %1\n(Placeholder)").arg(QFileInfo(imagePath).baseName()));
    }
    
    if (m_pixmapItem) {
        m_scene->removeItem(m_pixmapItem);
        delete m_pixmapItem;
    }
    
    m_pixmapItem = m_scene->addPixmap(pixmap);
    m_scene->setSceneRect(pixmap.rect());
    
    // Scale to fit widget
    fitInView(m_scene->sceneRect(), Qt::KeepAspectRatio);
}

void CutsceneWidget::fadeIn()
{
    m_fadeAnimation->setStartValue(0.0);
    m_fadeAnimation->setEndValue(1.0);
    m_fadeAnimation->start();
}

void CutsceneWidget::fadeOut()
{
    m_fadeAnimation->setStartValue(1.0);
    m_fadeAnimation->setEndValue(0.0);
    m_fadeAnimation->start();
}

class MemoryBar : public QWidget
{
    Q_OBJECT

public:
    explicit MemoryBar(QWidget *parent = nullptr);
    void updateMemory(const StoryEngineInterface::MemoryData &data);

private:
    QVBoxLayout *m_layout;
    QLabel *m_alignmentLabel;
    QProgressBar *m_kindnessBar;
    QProgressBar *m_obsessionBar;
    QProgressBar *m_truthBar;
    QProgressBar *m_trustBar;
};

MemoryBar::MemoryBar(QWidget *parent)
    : QWidget(parent)
    , m_layout(new QVBoxLayout(this))
    , m_alignmentLabel(new QLabel("Alignment: Neutral", this))
    , m_kindnessBar(new QProgressBar(this))
    , m_obsessionBar(new QProgressBar(this))
    , m_truthBar(new QProgressBar(this))
    , m_trustBar(new QProgressBar(this))
{
    m_layout->setContentsMargins(5, 5, 5, 5);
    m_layout->setSpacing(5);
    
    // Set up alignment label
    m_alignmentLabel->setStyleSheet("color: #E0E0E0; font-weight: bold;");
    m_layout->addWidget(m_alignmentLabel);
    
    // Set up progress bars
    QList<QProgressBar*> bars = {m_kindnessBar, m_obsessionBar, m_truthBar, m_trustBar};
    QStringList labels = {"Kindness", "Obsession", "Truth", "Trust"};
    QList<QColor> colors = {
        QColor(100, 200, 100),  // Kindness - Green
        QColor(200, 100, 100),  // Obsession - Red
        QColor(100, 100, 200),  // Truth - Blue
        QColor(200, 200, 100)   // Trust - Yellow
    };
    
    for (int i = 0; i < bars.size(); ++i) {
        QHBoxLayout *barLayout = new QHBoxLayout();
        
        QLabel *label = new QLabel(labels[i] + ":", this);
        label->setStyleSheet("color: #E0E0E0; min-width: 80px;");
        label->setAlignment(Qt::AlignRight | Qt::AlignVCenter);
        
        bars[i]->setRange(0, 100);
        bars[i]->setValue(0);
        bars[i]->setStyleSheet(QString(
            "QProgressBar {"
            "    border: 1px solid #666;"
            "    border-radius: 3px;"
            "    text-align: center;"
            "    background-color: #333;"
            "}"
            "QProgressBar::chunk {"
            "    background-color: %1;"
            "    border-radius: 2px;"
            "}"
        ).arg(colors[i].name()));
        
        barLayout->addWidget(label);
        barLayout->addWidget(bars[i]);
        m_layout->addLayout(barLayout);
    }
    
    setFixedWidth(250);
    setStyleSheet("background-color: #2A2A2A; border: 1px solid #666; border-radius: 5px;");
}

void MemoryBar::updateMemory(const StoryEngineInterface::MemoryData &data)
{
    m_alignmentLabel->setText(QString("Alignment: %1").arg(data.alignment));
    m_kindnessBar->setValue(static_cast<int>(data.kindness));
    m_obsessionBar->setValue(static_cast<int>(data.obsession));
    m_truthBar->setValue(static_cast<int>(data.truth));
    m_trustBar->setValue(static_cast<int>(data.trust));
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);

private slots:
    void onChoiceClicked();
    void onSceneChanged();
    void onMemoryUpdated();
    void onErrorOccurred(const QString &message);
    void onResetGame();

private:
    void setupUI();
    void updateScene();
    void updateMemory();
    void setupDarkTheme();
    
    StoryEngineInterface *m_storyEngine;
    CutsceneWidget *m_cutsceneWidget;
    QTextEdit *m_dialogueText;
    QList<QPushButton*> m_choiceButtons;
    MemoryBar *m_memoryBar;
    QPushButton *m_resetButton;
    
    StoryEngineInterface::SceneData m_currentScene;
};

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , m_storyEngine(new StoryEngineInterface(this))
    , m_cutsceneWidget(nullptr)
    , m_dialogueText(nullptr)
    , m_memoryBar(nullptr)
    , m_resetButton(nullptr)
{
    setupDarkTheme();
    setupUI();
    
    // Connect signals
    connect(m_storyEngine, &StoryEngineInterface::sceneChanged, this, &MainWindow::onSceneChanged);
    connect(m_storyEngine, &StoryEngineInterface::memoryUpdated, this, &MainWindow::onMemoryUpdated);
    connect(m_storyEngine, &StoryEngineInterface::errorOccurred, this, &MainWindow::onErrorOccurred);
    
    // Load initial scene
    updateScene();
    updateMemory();
}

void MainWindow::setupDarkTheme()
{
    QPalette darkPalette;
    darkPalette.setColor(QPalette::Window, QColor(53, 53, 53));
    darkPalette.setColor(QPalette::WindowText, QColor(255, 255, 255));
    darkPalette.setColor(QPalette::Base, QColor(25, 25, 25));
    darkPalette.setColor(QPalette::AlternateBase, QColor(53, 53, 53));
    darkPalette.setColor(QPalette::ToolTipBase, QColor(0, 0, 0));
    darkPalette.setColor(QPalette::ToolTipText, QColor(255, 255, 255));
    darkPalette.setColor(QPalette::Text, QColor(255, 255, 255));
    darkPalette.setColor(QPalette::Button, QColor(53, 53, 53));
    darkPalette.setColor(QPalette::ButtonText, QColor(255, 255, 255));
    darkPalette.setColor(QPalette::BrightText, QColor(255, 0, 0));
    darkPalette.setColor(QPalette::Link, QColor(42, 130, 218));
    darkPalette.setColor(QPalette::Highlight, QColor(42, 130, 218));
    darkPalette.setColor(QPalette::HighlightedText, QColor(0, 0, 0));
    
    qApp->setPalette(darkPalette);
    qApp->setStyle(QStyleFactory::create("Fusion"));
}

void MainWindow::setupUI()
{
    setWindowTitle("Into the Dark");
    setMinimumSize(1200, 800);
    resize(1400, 900);
    
    QWidget *centralWidget = new QWidget(this);
    setCentralWidget(centralWidget);
    
    QHBoxLayout *mainLayout = new QHBoxLayout(centralWidget);
    mainLayout->setContentsMargins(10, 10, 10, 10);
    mainLayout->setSpacing(10);
    
    // Left side - Cutscene and dialogue
    QVBoxLayout *leftLayout = new QVBoxLayout();
    
    // Cutscene widget
    m_cutsceneWidget = new CutsceneWidget(this);
    m_cutsceneWidget->setMinimumSize(800, 600);
    leftLayout->addWidget(m_cutsceneWidget);
    
    // Dialogue text
    m_dialogueText = new QTextEdit(this);
    m_dialogueText->setMaximumHeight(150);
    m_dialogueText->setReadOnly(true);
    m_dialogueText->setStyleSheet(
        "QTextEdit {"
        "    background-color: rgba(0, 0, 0, 150);"
        "    color: #E0E0E0;"
        "    border: 1px solid #666;"
        "    border-radius: 5px;"
        "    padding: 10px;"
        "    font-size: 14px;"
        "}"
    );
    leftLayout->addWidget(m_dialogueText);
    
    // Choice buttons
    QHBoxLayout *choiceLayout = new QHBoxLayout();
    for (int i = 0; i < 4; ++i) {
        QPushButton *button = new QPushButton(this);
        button->setMinimumHeight(50);
        button->setStyleSheet(
            "QPushButton {"
            "    background-color: #444;"
            "    color: #E0E0E0;"
            "    border: 1px solid #666;"
            "    border-radius: 5px;"
            "    padding: 10px;"
            "    font-size: 12px;"
            "}"
            "QPushButton:hover {"
            "    background-color: #555;"
            "    border-color: #888;"
            "}"
            "QPushButton:pressed {"
            "    background-color: #333;"
            "}"
        );
        connect(button, &QPushButton::clicked, this, &MainWindow::onChoiceClicked);
        m_choiceButtons.append(button);
        choiceLayout->addWidget(button);
    }
    leftLayout->addLayout(choiceLayout);
    
    mainLayout->addLayout(leftLayout, 3);
    
    // Right side - Memory bar and controls
    QVBoxLayout *rightLayout = new QVBoxLayout();
    
    // Memory bar
    m_memoryBar = new MemoryBar(this);
    rightLayout->addWidget(m_memoryBar);
    
    rightLayout->addStretch();
    
    // Reset button
    m_resetButton = new QPushButton("Reset Game", this);
    m_resetButton->setStyleSheet(
        "QPushButton {"
        "    background-color: #666;"
        "    color: #E0E0E0;"
        "    border: 1px solid #888;"
        "    border-radius: 5px;"
        "    padding: 10px;"
        "    font-size: 14px;"
        "}"
        "QPushButton:hover {"
        "    background-color: #777;"
        "}"
    );
    connect(m_resetButton, &QPushButton::clicked, this, &MainWindow::onResetGame);
    rightLayout->addWidget(m_resetButton);
    
    mainLayout->addLayout(rightLayout, 1);
}

void MainWindow::updateScene()
{
    m_currentScene = m_storyEngine->getCurrentScene();
    
    // Update cutscene
    QString imagePath = QString("assets/cutscenes/%1").arg(m_currentScene.background);
    m_cutsceneWidget->setCutscene(imagePath);
    m_cutsceneWidget->fadeIn();
    
    // Update dialogue
    m_dialogueText->setPlainText(m_currentScene.dialogue);
    
    // Update choice buttons
    for (int i = 0; i < m_choiceButtons.size() && i < m_currentScene.choices.size(); ++i) {
        const auto &choice = m_currentScene.choices[i];
        QString buttonText = QString("%1\n(+%2 %3)")
            .arg(choice.first)
            .arg(5) // Memory value is hardcoded in Python for now
            .arg(choice.second);
        m_choiceButtons[i]->setText(buttonText);
        m_choiceButtons[i]->setVisible(true);
    }
    
    // Hide unused buttons
    for (int i = m_currentScene.choices.size(); i < m_choiceButtons.size(); ++i) {
        m_choiceButtons[i]->setVisible(false);
    }
}

void MainWindow::updateMemory()
{
    StoryEngineInterface::MemoryData memoryData = m_storyEngine->getMemoryData();
    m_memoryBar->updateMemory(memoryData);
}

void MainWindow::onChoiceClicked()
{
    QPushButton *button = qobject_cast<QPushButton*>(sender());
    if (!button) return;
    
    int choiceIndex = m_choiceButtons.indexOf(button);
    if (choiceIndex >= 0 && choiceIndex < m_currentScene.choices.size()) {
        if (m_storyEngine->makeChoice(choiceIndex)) {
            updateScene();
            updateMemory();
        }
    }
}

void MainWindow::onSceneChanged()
{
    updateScene();
}

void MainWindow::onMemoryUpdated()
{
    updateMemory();
}

void MainWindow::onErrorOccurred(const QString &message)
{
    QMessageBox::warning(this, "Error", message);
}

void MainWindow::onResetGame()
{
    int ret = QMessageBox::question(this, "Reset Game", 
                                   "Are you sure you want to reset the game? All progress will be lost.",
                                   QMessageBox::Yes | QMessageBox::No);
    
    if (ret == QMessageBox::Yes) {
        if (m_storyEngine->resetGame()) {
            updateScene();
            updateMemory();
            QMessageBox::information(this, "Game Reset", "Game has been reset to the beginning.");
        } else {
            QMessageBox::warning(this, "Reset Failed", "Failed to reset the game.");
        }
    }
}

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    
    // Set application properties
    app.setApplicationName("Into the Dark");
    app.setApplicationVersion("1.0.0");
    app.setOrganizationName("Game Studio");
    
    MainWindow window;
    window.show();
    
    return app.exec();
}

#include "main.moc"
