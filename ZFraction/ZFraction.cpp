#include "ZFraction.h"

using namespace std;

ZFraction::ZFraction() : m_numerator(0), m_denominator(1)
{

}

ZFraction::ZFraction(int numerator) : m_numerator(numerator), m_denominator(1)
{

}

ZFraction::ZFraction(int numerator, int denominator) : m_numerator(numerator), m_denominator(denominator)
{
    m_numerator /= pgcd(m_numerator, m_denominator);
    m_denominator /= pgcd(m_numerator, m_denominator);
}

ZFraction::ZFraction(ZFraction const& autre) : m_numerator(autre.m_numerator), m_denominator(autre.m_denominator)
{

}

int ZFraction::getNum()
{
    return m_numerator;
}

int ZFraction::getDenom()
{
    return m_denominator;
}

void ZFraction::display(ostream &flux) const
{
    flux << m_numerator << "/" << m_denominator;
}

bool ZFraction::isEgal(ZFraction const& b) const
{
    return (m_numerator == b.m_numerator && m_denominator == b.m_denominator);
}

bool ZFraction::isSmallerThan(ZFraction const& b) const
{
    int comp_num1 = m_numerator*b.m_denominator;
    int comp_num2 = b.m_numerator*m_denominator;

    if (comp_num1 < comp_num2)
        return true;
    else
        return false;
}

ZFraction& ZFraction::operator+=(const ZFraction& a)
{
    m_numerator = m_numerator*a.m_denominator + m_denominator*a.m_numerator;
    m_denominator *= a.m_denominator;
    int div = pgcd(m_numerator, m_denominator);
    m_numerator/=div;
    m_denominator/=div;

    return *this; // this == pointeur vers l'objet, *this == l'objet
}

ZFraction& ZFraction::operator*=(const ZFraction& a)
{
    m_numerator *= a.m_numerator;
    m_denominator *= a.m_denominator;
    int div = pgcd(m_numerator, m_denominator);
    m_numerator/=div;
    m_denominator/=div;

    return *this;
}

ostream& operator<<(ostream &flux, ZFraction const& fraction)
{
    fraction.display(flux);
    return flux;
}

ZFraction operator+(ZFraction const& a, ZFraction const& b)
{
    ZFraction copie(a);
    copie += b;
    return copie;
}

ZFraction operator*(ZFraction const& a, ZFraction const& b)
{
    ZFraction copie(a);
    copie *= b;
    return copie;
}

bool operator==(ZFraction const& a, ZFraction const& b)
{
    return a.isEgal(b);
}

bool operator<(ZFraction const& a, ZFraction const& b)
{
    return a.isSmallerThan(b);
}

int pgcd(int a, int b)
{
    while (b != 0)
    {
        const int t = b;
        b = a%b;
        a=t;
    }
    return a;
}
