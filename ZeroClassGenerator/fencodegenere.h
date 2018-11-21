#include <QDialog>
#include <QTextEdit>
#include <QVBoxLayout>
#include <QPushButton>
#include <QString>

#ifndef FENCODEGENERE_H
#define FENCODEGENERE_H


class FenCodeGenere : public QDialog
{
public:
    FenCodeGenere(QString classe);

private:
    void writeClass();

    QString m_classe;

    QTextEdit *m_textClass;
    QVBoxLayout *m_layout;
    QPushButton *m_buttonClose;
};

#endif // FENCODEGENERE_H
