#include <QApplication>
#include <QWidget>

#include "fencodegenere.h"
#include "fenprincipale.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    FenPrincipale fenetre;

    fenetre.show();

    return app.exec();
}
