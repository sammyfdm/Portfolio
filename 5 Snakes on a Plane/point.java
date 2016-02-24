public class point
{
    protected double x;
    protected double y;
    
    public point ()
    {
        x = 0;
        y = 0;
    }
    
    public point (double xx, double yy)
    {
        x = xx;
        y = yy;
    }
    
    public point (point P)
    {
        x = P.x;
        y = P.y;
    }
}
