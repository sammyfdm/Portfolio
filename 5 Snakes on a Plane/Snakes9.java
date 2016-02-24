import java.lang.Math;
import java.io.*;

public class Snakes9
{
    static double t;       //temp variable
    static double d;
    static int N;       //N-1 possible turning sequence between segments
    static double D;    //diameter of circle
    static double angles [];
    static int sequence [];  //number sequence to be entered as solution
    static int max;
    static point P[];
    static double radius;

    //always returns positive angle, between 0 - Pi
    public static double angle (int p1, int p2, int p3)
    {
        double ax = P [p1].x - P [p2].x; //-1
        double ay = P [p1].y - P [p2].y; //-1
        double bx = P [p3].x - P [p2].x; //-0.5
        double by = P [p3].y - P [p2].y; //1
        ax = (ax * bx + ay * by) / Math.sqrt (sqr (ax) + sqr (ay)) / Math.sqrt (sqr (bx) + sqr (by));
        if (ax >= 1)
            return(0);
        else if (ax <= -1)
            return(Math.PI);
        else
            return (Math.acos (ax));
    }

    public static boolean sameside (point L1, point L2, point p1, point p2)
    {
        double dx = L2.x - L1.x;
        double dy = L2.y - L1.y;
        return (((dx * (p1.y - L1.y) - dy * (p1.x - L1.x)) * (dx * (p2.y - L2.y) - dy * (p2.x - L2.x))) >= 0);
    }


    public static point check2 (int i1, int i2, int pos)
    {
        //System.out.println ("Check 2:   i1 = " + i1 + "   i2 = " + i2);
        boolean inside = true;
        point cen = new point ((P [i1].x + P [i2].x) / 2, (P [i1].y + P [i2].y) / 2); //circle centre
        radius = sqr (cen.x - P [i1].x) + sqr (cen.y - P [i1].y);   //this is actually r^2
        int z = 0;
        while (z < pos + 2 && inside)
        {
            inside = sqr (P [z].x - cen.x) + sqr (P [z].y - cen.y) <= radius + d;
            z++;
        }
        if (!inside)
            cen = check3 (i1, i2, z - 1, pos);
        return (cen);
    }



    public static point check3 (int i1, int i2, int i3, int pos)
    {
        point cen = new point ();
        //System.out.println ("Check 3:   i1 = " + i1 + "   i2 = " + i2 + "    i3 = " + i3);
        if (angle (i1, i2, i3) >= Math.PI / 2 - d) //obtuse/right triangle
            cen = check2 (i1, i3, pos);
        else if (angle (i2, i1, i3) >= Math.PI / 2 - d) //obtuse/right triangle
            cen = check2 (i2, i3, pos);
        else //acute triangle
        {
            boolean inside = true;
            double m1, b1, m2, b2;  //find cen:
            if (Math.abs (P [i1].y - P [i2].y) > d)
            {
                m1 = -(P [i1].x - P [i2].x) / (P [i1].y - P [i2].y); //perpendicular
                b1 = (P [i1].y + P [i2].y) / 2 - (P [i1].x + P [i2].x) / 2 * m1;
            }
            else
            {
                m1 = -(P [i2].x - P [i3].x) / (P [i2].y - P [i3].y);
                b1 = (P [i2].y + P [i3].y) / 2 - (P [i2].x + P [i3].x) / 2 * m1;
            }
            if (Math.abs (P [i1].y - P [i3].y) > d)
            {
                m2 = -(P [i1].x - P [i3].x) / (P [i1].y - P [i3].y); //perpendicular
                b2 = (P [i1].y + P [i3].y) / 2 - (P [i1].x + P [i3].x) / 2 * m2;
            }
            else
            {
                m2 = -(P [i2].x - P [i3].x) / (P [i2].y - P [i3].y);     //perpendicular
                b2 = (P [i2].y + P [i3].y) / 2 - (P [i2].x + P [i3].x) / 2 * m2;
            }
            cen.x = (b2 - b1) / (m1 - m2);
            cen.y = m1 * cen.x + b1;
            //distance from one point to cen = radius
            radius = sqr (cen.x - P [i1].x) + sqr (cen.y - P [i1].y); //actually r squared
            //check each point
            int z = 0;
            while (z < pos + 2 && inside)
            {
                inside = sqr (P [z].x - cen.x) + sqr (P [z].y - cen.y) <= radius + d;
                z++;
            }
            //reassign & repeat || finished
            if (!inside)
            { //step 4:
                point pl = new point (P [z - 1]);
                int Q = i1;
                int R = i1;
                double dis = sqr (pl.x - P [i1].x) + sqr (pl.y - P [i1].y);
                if (sqr (pl.x - P [i2].x) + sqr (pl.y - P [i2].y) > dis)
                {
                    Q = i2;

                    if (sameside (cen, P [Q], P [i1], pl))
                        R = i3;
                    else
                        R = i1;
                    dis = sqr (pl.x - P [i2].x) + sqr (pl.y - P [i2].y);
                }
                if (sqr (pl.x - P [i3].x) + sqr (pl.y - P [i3].y) > dis)
                {
                    Q = i3;
                    if (sameside (cen, P [Q], P [i1], pl))
                        R = i2;
                    else
                        R = i1;
                }
                if (Q == i1)    //if preceding if statements false
                {
                    if (sameside (cen, P [Q], P [i2], pl))
                        R = i3;
                    else
                        R = i2;
                }
                cen = check3 (R, Q, z - 1, pos);
            }
        }
        return (cen);
    }

    public static double sqr (double a)
    {
        return(a*a);
    }

    public static boolean checkI (int pos)
    {
        boolean good = true;
        //solve for last segment's equation:
        double m = (P [pos + 1].y - P [pos].y) / (P [pos + 1].x - P [pos].x);
        double b = P [pos + 1].y - m * P [pos + 1].x;
        double xi; //x of intersection of lines/equations
        double m2, b2; //used for each other segment
        int z = 1;
        while (z < pos && good)
        {
            m2 = (P [z].y - P [z - 1].y) / (P [z].x - P [z - 1].x); //solve for this segment's equation:
            b2 = P [z].y - m2 * P [z].x;
            xi = (b2 - b) / (m - m2);   //x-coordinate of intersection
            good = (xi < P [pos].x - d && xi < P [pos + 1].x - d) || (xi > P [pos].x + d && xi > P [pos + 1].x + d) || (xi < P [z - 1].x - d && xi < P [z].x - d) || (xi > P [z - 1].x + d && xi > P [z].x + d);
            z++;
        }
        return (good);
     }

    /* xs,ys is where new segment continues from */
    public static void recursion (int pos, double a, point cen)
    {
        point c = new point ();
        for (int k = 1 ; k < N ; k++)
        {
            sequence [pos - 1] = k;
            t = a + angles [k - 1];
            P [pos + 1] = new point (P [pos].x + Math.cos (t), P [pos].y + Math.sin (t));
            if (checkI (pos))
            {   //if the new point is not within the previous circle:
                if (sqr (P [pos + 1].x - cen.x) + sqr (P [pos + 1].y - cen.y) > D * D / 4 - 0.1)
                {
                    c = check2 (0, 1, pos);
                    radius = Math.sqrt (radius);
                    if (radius <= D / 2 + d)
                    {
                        if (pos > max)
                        {
                            max = pos;
                            //writeS ();
                            System.out.print ("\nnew Max @ " + (pos + 1) + "::: ");
                            for (int z = 0 ; z < max ; z++)
                            System.out.print (sequence [z] + " ");
                        }
                        else if (pos == max)
                        {
                            System.out.print ("\nMax tie @ " + (pos + 1) + "    ");
                            for (int z = 0 ; z < pos ; z++)
                            System.out.print (sequence [z] + " ");
                        }
                        recursion (pos + 1, t, c);
                    }
                }
                else
                {
                    if (pos > max)
                    {
                        max = pos;
                        //writeS ();
                        System.out.print ("\nnew Max @ " + (pos + 1) + "::: ");
                        for (int z = 0 ; z < max ; z++)
                            System.out.print (sequence [z] + " ");
                    }
                    else if (pos == max)
                    {
                        System.out.print ("\nMax tie @ " + (pos + 1) + "    ");
                        for (int z = 0 ; z < pos ; z++)
                            System.out.print (sequence [z] + " ");
                    }
                    recursion (pos + 1, t, cen);
                }
            }
        }
    }


    public static void main (String [] args)
    {
        point cen = new point(0.5,0);
        max = 0;
        d = 0.00000001;   //error distance
        D = 4;
        N = 9;
        sequence = new int [200];
        P = new point [200];
        P [0] = new point (0,0);
        P [1] = new point (1,0);
        System.out.println ("N: " + N + "   D: " + D);
        angles = new double [N-1];
        for (int k = 1; k < N; k++)
            angles[k-1] = (Math.PI * (2 * (double) k / N - 1)); //radians
        for (int z = 1; z < N/2+1; z++)
        {
            sequence[0] = z;
            P[2] = new point (1+Math.cos(angles[z-1]),Math.sin(angles[z-1]));
            recursion (2,angles[z-1],cen);
            System.out.println("\nDone: " + z);
        }
        System.out.print ("\n@ " + (max+1) + " Finished");
        System.out.println ();
    } // main method
} // Snakes class

/*
    N                   D                                  Possible Angles 
(Degrees)
    5     3 4 5 6 7 8 9 10 11 12 13 14          -108    -36    36   108
    7   2 3 4 5 6 7 8 9 10 11                   -129    -77   -26    26    77   129
    8   2 3 4 5 6 7 8 9 10                      -135    -90   -45     0   45    90   135
    9   2 3 4 5 6 7 8 9                         -140   -100   -60   -20    20    60   100   140
    10  2 3 4 5 6 7 8                           -144   -108   -72   -36     0    36    72   108   144
    11  2 3 4 5 6 7                             -147   -115   -82   -49   -16    16    82   115   147
    12    3 4 5 6 7                             -150   -120   -90   -60   -30     0    30    60    90   120   150

    Total Score: 23.353 / 27 Ranking: 23   Average: 0.8649
    Scores:
    5,3     1           17      ==> 17
    5,4     1           33      ==> 33
    5,5     0.9298      53      ==> 57
    5,6     0.8589      73      ==> 85
    5,7     0.8205      96      ==> 117
    5,8     0.7267      117     ==> 161
    5,9     0.6838      147     ==> 215
    5,10    0.7427      179     ==> 241
    5,11
    5,12
    5,13
    5,14
        Score N=5:  6.7624 / 8
    7,2     1           7       ==> 7
    7,3     1           20      ==> 20
    7,4     0.8837      38      ==> 43
    7,5
    7,6
    7,7
    7,8
    7,9
    7,10
    7,11
        Score N=7:  2.8837 / 3
    8,2     1           8       ==> 8
    8,3     0.8636      19      ==> 22
    8,4     0.7500      33      ==> 44
    8,5     0.6389      46      ==> 72
    8,6
    8,7
    8,8
    8,9
    8,10
        Score N=8:  3.2525 / 4
    9,2     0.9166      11      ==> 12
    9,3     0.9630      26      ==> 27
    9,4     0.7457      44      ==> 59
    9,5     0.6832      69      ==> 101
    9,6
    9,7
    9,8
    9,9
        Score N=9:  3.3085 / 4
    10,2    1           9       ==> 9
    10,3    1           23      ==> 23
    10,4    0.8367      41      ==> 49
    10,5
    10,6
    10,7
    10,8
        Score N=10: 2.8367 / 3
    11,2    1           11      ==> 11
    11,3    0.9118      31      ==> 34
    11,4    0.6184      47      ==> 76
    11,5
    11,6
    11,7
        Score N=11: 2.5302 / 3
    12,3    0.9696      32      ==> 33
    12,4    0.8182      54      ==> 66
    12,5
    12,6
    12,7
        Score N=12: 1.7878 / 2
*/

