#include "fenprincipale.h"

FenPrincipale::FenPrincipale() : QWidget()
{
    setFixedSize(450,600);

    // Principal layout
    m_principalLayout = new QVBoxLayout(this);

}

QGroupBox FenPrincipale::createFirstGroupBox()
{
    m_groupDef = new QGroupBox;

    m_groupDef->setLayout(m_VDef);

    return m_groupDef;
}
