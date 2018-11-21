#include "fenprincipale.h"
#include "fencodegenere.h"

FenPrincipale::FenPrincipale() : QWidget()
{
    // Principal layout
    m_principalLayout = new QVBoxLayout(this);

    createDefClassBox();
    createOptionsBox();
    createCommBox();

    m_buttonGenerate = new QPushButton("Générer!", this);
    m_buttonQuit = new QPushButton("Quitter", this);

    m_gridButtons = new QGridLayout;
    m_gridButtons->setColumnStretch(0, 1);
    m_gridButtons->addWidget(m_buttonGenerate, 0, 2);
    m_gridButtons->addWidget(m_buttonQuit, 0, 3);

    m_principalLayout->addWidget(m_groupDef);
    m_principalLayout->addWidget(m_groupOptions);
    m_principalLayout->addWidget(m_groupComm);
    m_principalLayout->addLayout(m_gridButtons);

    setLayout(m_principalLayout);

    QObject::connect(m_buttonGenerate, SIGNAL(clicked()), this, SLOT(generateClass()));
    QObject::connect(m_buttonQuit, SIGNAL(clicked()), qApp, SLOT(quit()));
}

void FenPrincipale::createDefClassBox()
{
    m_groupDef = new QGroupBox;
    m_VDef = new QVBoxLayout;

    m_lineNom = new QLineEdit;
    m_lineClassMere = new QLineEdit;

    m_formDef = new QFormLayout;

    m_formDef->addRow("&Nom :", m_lineNom);
    m_formDef->addRow("Classe &mère :", m_lineClassMere);

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

    m_lineAuteur = new QLineEdit;
    m_date = new QDateEdit(QDate::currentDate());
    m_textComm = new QTextEdit;
    m_textComm->setMinimumHeight(200);
    m_textComm->setAcceptRichText(true);

    m_formComm = new QFormLayout;

    m_formComm->addRow("&Auteur :", m_lineAuteur);
    m_formComm->addRow("Da&te de création :", m_date);
    m_formComm->addRow("&Rôle de la classe :", m_textComm);

    m_VComm->addLayout(m_formComm);

    m_groupComm->setCheckable(true);
    m_groupComm->setTitle("Ajouter des commentaires");
    m_groupComm->setLayout(m_VComm);
}

void FenPrincipale::generateClass()
{
    // get data from the comm section
    QString auteur(m_lineAuteur->text());
    QDate time(m_date->date());
    QString date(time.toString());
    QString role(m_textComm->toPlainText());
    QStringList lines(role.split("\n"));

    // get data from the def section
    QString nom(m_lineNom->text());
    QString upperedNom = nom.toUpper();
    QString classeMere(m_lineClassMere->text());

    // get data from the option section
    bool header(m_checkHeader->isChecked());
    bool constructor(m_checkCons->isChecked());
    bool destructor(m_checkDestruc->isChecked());

    // Write the class
    QString classe;

    classe.append("/*<br>Auteur : "+auteur+"<br>Date de création : "+date+
                  "<br><br>Rôle :<br>");

    for(int i(0);i < lines.size(); i++)
    {
        classe.append(lines[i]+"<br>");
    }

    if(header == true)
    {
        classe.append("*/<br><br>#ifndef "+upperedNom+"_H<br>");
        classe.append("#define "+upperedNom+"_H<br><br><br>");
    }

    classe.append("class "+nom+" : public "+classeMere+"<br>{<br>");
    classe.append("<tab>public:<br>");

    if(constructor == true)
    {
        classe.append("<tab><tab>"+nom+"();");
    }

    if(destructor == true)
    {
        classe.append("<tab><tab>~"+nom+"();");
    }

    classe.append("<br><br><br><tab>protected:<br><br><br>");
    classe.append("<tab>private:<br><br><br>};");

    if(header == true)
    {
        classe.append("<br><br>#endif");
    }

    // Call the window
    FenCodeGenere generatedClass(classe);
}
