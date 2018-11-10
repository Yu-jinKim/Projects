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

void ZFraction::display() const
{
    cout << m_numerator << "/" << m_denominator;
}

int ZFraction::getNum()
{
    return m_numerator;
}

int ZFraction::getDenom()
{
    return m_denominator;
}

ZFraction& ZFraction::operator+=(const ZFraction& a)
{
    m_numerator = m_numerator*a.m_denominator + m_denominator*a.m_numerator;
    m_denominator *= a.m_denominator;
    int div = pgcd(m_numerator, m_denominator);
    m_numerator/=div;
    m_denominator/=div;

    return *this;
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
