#include "fenprincipale.h"

FenPrincipale::FenPrincipale() : QWidget()
{
    setFixedSize(450,600);

    // Principal layout
    m_principalLayout = new QVBoxLayout(this);
    createDefClassBox();
    createOptionsBox();
    createCommBox();

    m_generate = new QPushButton("Générer!");
    m_quit = new QPushButton("Quitter");

    m_HButtons = new QHBoxLayout;
    m_HButtons->addWidget(m_generate);
    m_HButtons->addWidget(m_quit);

    m_principalLayout->addWidget(m_groupDef);
    m_principalLayout->addWidget(m_groupOptions);
    m_principalLayout->addWidget(m_groupComm);
    m_principalLayout->addLayout(m_HButtons);

    setLayout(m_principalLayout);
}

void FenPrincipale::createDefClassBox()
{
    m_groupDef = new QGroupBox;
    m_VDef = new QVBoxLayout;

    m_formDef = new QFormLayout;

    m_nom = new QLineEdit;
    m_classMere = new QLineEdit;

    m_formDef->addRow("&Nom :", m_nom);
    m_formDef->addRow("Classe &mère :", m_classMere);

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

    m_formComm = new QFormLayout;

    m_auteur = new QLineEdit;
    m_date = new QDateEdit;
    m_comm = new QLineEdit;

    m_formComm->addRow("&Auteur :", m_auteur);
    m_formComm->addRow("Da&te de création :", m_date);
    m_formComm->addRow("&Rôle de la classe :", m_comm);

    m_groupComm->setCheckable(false);
    m_groupComm->setTitle("Ajouter des commentaires");
    m_groupComm->setLayout(m_VComm);
}
