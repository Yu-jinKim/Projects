#include <QWidget>
#include <QApplication>
#include <QGroupBox>
#include <QCheckBox>
#include <QFormLayout>
#include <QVBoxLayout>
#include <QDateEdit>
#include <QPushButton>
#include <QLineEdit>
#include <QGridLayout>
#include <QTextEdit>

#ifndef FENPRINCIPALE_H
#define FENPRINCIPALE_H


class FenPrincipale : public QWidget
{
    Q_OBJECT

public:
    FenPrincipale();

private:
    void createDefClassBox();
    void createOptionsBox();
    void createCommBox();

    QVBoxLayout *m_principalLayout;
    QVBoxLayout *m_VDef;
    QVBoxLayout *m_VOptions;
    QVBoxLayout *m_VComm;

    QGridLayout *m_gridButtons;

    QGroupBox *m_groupDef;
    QGroupBox *m_groupOptions;
    QGroupBox *m_groupComm;

    QFormLayout *m_formDef;
    QFormLayout *m_formComm;

    QCheckBox *m_checkHeader;
    QCheckBox *m_checkCons;
    QCheckBox *m_checkDestruc;

    QLineEdit *m_nom;
    QLineEdit *m_classMere;
    QLineEdit *m_auteur;

    QTextEdit *m_comm;

    QDateEdit *m_date;

    QPushButton *m_generate;
    QPushButton *m_quit;
};

#endif // FENPRINCIPALE_H
