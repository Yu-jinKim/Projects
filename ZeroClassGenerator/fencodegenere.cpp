#include "fencodegenere.h"

FenCodeGenere::FenCodeGenere(QString classe) : QDialog(), m_classe(classe)
{
    setMinimumSize(QSize(400,500));
    m_layout = new QVBoxLayout(this);

    m_textClass = new QTextEdit(m_classe);
    m_textClass->setReadOnly(true);
    m_buttonClose = new QPushButton("Fermer", this);

    m_layout->addWidget(m_textClass);
    m_layout->addWidget(m_buttonClose);

    setLayout(m_layout);

    QObject::connect(m_buttonClose, SIGNAL(clicked()), this, SLOT(quit()));

    FenCodeGenere::exec();
}
