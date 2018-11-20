#include "fenprincipale.h"

FenPrincipale::FenPrincipale() : QWidget()
{
    setFixedSize(450,600);

    // Principal layout
    m_principalLayout = new QVBoxLayout(this);
    createDefClassBox();
    createOptionsBox();

    m_principalLayout->addWidget(m_groupDef);
    m_principalLayout->addWidget(m_groupOptions);

    setLayout(m_principalLayout);
}

void FenPrincipale::createDefClassBox()
{
    m_groupDef = new QGroupBox;
    m_VDef = new QVBoxLayout;

    m_formDef = new QFormLayout;

    m_nom = new QLineEdit;
    m_classMere = new QLineEdit;

    m_formDef->addRow("Nom :", m_nom);
    m_formDef->addRow("Classe mère :", m_classMere);

    m_groupDef->setLayout(m_VDef);
}

void FenPrincipale::createOptionsBox()
{
    m_groupOptions = new QGroupBox;
    m_VOptions = new QVBoxLayout;

    m_checkHeader = new QCheckBox;
    m_checkCons = new QCheckBox;
    m_checkDestruc = new QCheckBox;

    m_VOptions->addWidget(m_checkHeader);
    m_VOptions->addWidget(m_checkCons);
    m_VOptions->addWidget(m_checkDestruc);

    m_groupOptions->setLayout(m_VOptions);
}
