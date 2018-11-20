#include "fenprincipale.h"

FenPrincipale::FenPrincipale() : QWidget()
{
    // Principal layout
    m_principalLayout = new QVBoxLayout(this);
    createDefClassBox();
    createOptionsBox();
    createCommBox();

    m_generate = new QPushButton("Générer!", this);
    m_quit = new QPushButton("Quitter", this);

    m_gridButtons = new QGridLayout;
    m_gridButtons->setColumnStretch(0, 1);
    m_gridButtons->addWidget(m_generate, 0, 2);
    m_gridButtons->addWidget(m_quit, 0, 3);

    m_principalLayout->addWidget(m_groupDef);
    m_principalLayout->addWidget(m_groupOptions);
    m_principalLayout->addWidget(m_groupComm);
    m_principalLayout->addLayout(m_gridButtons);

    setLayout(m_principalLayout);

//    QObject::connect(m_quit, SIGNAL(clicked()), app, SLOT(quit()));
}

void FenPrincipale::createDefClassBox()
{
    m_groupDef = new QGroupBox;
    m_VDef = new QVBoxLayout;

    m_nom = new QLineEdit;
    m_classMere = new QLineEdit;

    m_formDef = new QFormLayout;

    m_formDef->addRow("&Nom :", m_nom);
    m_formDef->addRow("Classe &mère :", m_classMere);

    m_VDef->addLayout(m_formDef);
    m_groupDef->setTitle("Définition de la classe");
    m_groupDef->setLayout(m_VDef);
}

void FenPrincipale::createOptionsBox()
{
    m_groupOptions = new QGroupBox;
    m_VOptions = new QVBoxLayout;

    m_checkHeader = new QCheckBox("Protéger le &header contre les inclusions multiples");
    m_checkCons = new QCheckBox("Générer un &constructeur par défaut");
    m_checkDestruc = new QCheckBox("Générer un &destructeur");

    m_VOptions->addWidget(m_checkHeader);
    m_VOptions->addWidget(m_checkCons);
    m_VOptions->addWidget(m_checkDestruc);

    m_groupOptions->setTitle("Options");
    m_groupOptions->setLayout(m_VOptions);
}

void FenPrincipale::createCommBox()
{
    m_groupComm = new QGroupBox;
    m_VComm = new QVBoxLayout;

    m_auteur = new QLineEdit;
    m_date = new QDateEdit(QDate::currentDate());
    m_comm = new QTextEdit;
    m_comm->setMinimumHeight(200);

    m_formComm = new QFormLayout;

    m_formComm->addRow("&Auteur :", m_auteur);
    m_formComm->addRow("Da&te de création :", m_date);
    m_formComm->addRow("&Rôle de la classe :", m_comm);

    m_VComm->addLayout(m_formComm);

    m_groupComm->setCheckable(true);
    m_groupComm->setTitle("Ajouter des commentaires");
    m_groupComm->setLayout(m_VComm);
}
