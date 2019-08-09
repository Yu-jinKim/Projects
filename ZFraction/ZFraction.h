#ifndef ZFRACTION_H_INCLUDED
#define ZFRACTION_H_INCLUDED

class ZFraction
{
public:
    ZFraction();
    ZFraction(int numerator);
    ZFraction(int numerator, int denominator);
    ZFraction(ZFraction const& autre);

    int getNum();
    int getDenom();
    void display(std::ostream &flux) const;
    bool isEgal(ZFraction const& b) const;
    bool isSmallerThan(ZFraction const& b) const;

    ZFraction& operator+=(ZFraction const& a);
    ZFraction& operator*=(ZFraction const& a);

private:
    int m_numerator;
    int m_denominator;
};

int pgcd(int a, int b);

#endif // ZFRACTION_H_INCLUDED
