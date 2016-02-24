import java.lang.Math;
import java.io.*;

public class Snakes3
{
//    static long update;
    static double t;       //temp variable
    static double d;
    static int N;       //N-1 possible turning sequence between segments
    static double D;    //diameter of circle
    static double angles [];
    static int sequence [];  //number sequence to be entered as solution
    static int max;
    static point cen;
    static double radius;
    static point P[];
    
    /* writes sequence & number of segments to a text file 
    public static void writeS () throws IOException
    {
        String file = "N" + N + "D" + D + ".txt";
        PrintWriter output = new PrintWriter (new FileWriter (file));
        output.println ("# Segments: " + (max + 1));
        for (int z = 0 ; z < max ; z++)
            output.print ("" + sequence [z] + ' ');
        output.close ();
    }

    /* reads sequence & number of segments to a text file 
    public static void readS () throws IOException
    {
        String file = "N" + N + "D" + D + ".txt";
        BufferedReader input = new BufferedReader (new FileReader (file));   //connects input to the input file
        max = Integer.parseInt (input.readLine ().substring (12)) - 1;
        start = new int [max];
        String seq = input.readLine ();
        for (int z = 0 ; z < max ; z++)
            start [z] = Integer.parseInt ("" + seq.charAt (z * 2));
    }*/
    
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
    
    //always returns positive angle, between 0 - Pi
    public static double angle (point p1, point p2, point p3)
    {
        double ax = p1.x -  p2.x; //-1
        double ay = p1.y -  p2.y; //-1
        double bx = p3.x -  p2.x; //-0.5
        double by = p3.y -  p2.y; //1
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
        double dx1 = p1.x - L1.x;
        double dy1 = p1.y - L1.y;
        double dx2 = p2.x - L2.x;
        double dy2 = p2.y - L2.y;
        return (((dx * dy1 - dy * dx1) * (dx * dy2 - dy * dx2)) >= 0);
    }


    public static void check2 (int i1, int i2)
    {
        //System.out.println ("Check 2:   i1 = " + i1 + "   i2 = " + i2);
        boolean inside = true;
        cen = new point ((P [i1].x + P [i2].x) / 2, (P [i1].y + P [i2].y) / 2); //circle centre
        radius = sqr (cen.x - P [i1].x) + sqr (cen.y - P [i1].y);   //this is actually r^2
        int z = 0;
        while (z < P.length && inside)
        {
            if (z != i1 && z != i2)
            inside = sqr (P [z].x - cen.x) + sqr (P [z].y - cen.y) <= radius + d;
            z++;
        }
        if (!inside)
            check3 (i1, i2, z - 1);
        else
            radius = Math.sqrt (radius); //avoids sqrt in above calculations
    }


    public static void check3 (int i1, int i2, int i3)
    {
        //System.out.println ("Check 3:   i1 = " + i1 + "   i2 = " + i2 + "   i3 = " + i3);
        /*System.out.println ("Angle i1,i2,i3 = " + (180/Math.PI*angle (i1, i2, i3)));
        System.out.println ("Angle i2,i1,i3 = " + (180/Math.PI*angle (i2, i1, i3)));
        System.out.println ("Angle i1,i3,i2 = " + (180/Math.PI*angle (i1, i3, i2)));*/
        if (Math.abs (angle (i1, i2, i3)) >= Math.PI / 2 - d) //obtuse/right triangle
            check2 (i1, i3);
        else if (Math.abs (angle (i2, i1, i3)) >= Math.PI / 2 - d) //obtuse/right triangle
            check2 (i2, i3);
        else if (Math.abs (angle (i1, i3, i2)) >= Math.PI / 2 - d) //obtuse/right triangle
            check2 (i1, i2);
        else //acute triangle
        {
            boolean inside = true;
            //find cen
            double m1, b1, m2, b2;
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
            //System.out.println ("m1: " + m1 + " b1: " + b1 + " m2: " + m2 + " b2: " + b2);
            cen.x = (b2 - b1) / (m1 - m2);
            cen.y = m1 * cen.x + b1;
            //System.out.println ("cen.x " + cen.x + " cen.y " + cen.y);
            //distance from one point to cen = radius
            radius = sqr (cen.x - P [i1].x) + sqr (cen.y - P [i1].y); //actually r squared
            //check each point
            int z = 0;
            while (z < P.length && inside)
            {
                if (z != i1 && z != i2 && z != i3)
                    inside = sqr (P [z].x - cen.x) + sqr (P [z].y - cen.y) <= radius + d;
                z++;
            }
            //reassign & repeat || finished
            if (!inside)
            { //step 4:
                point pl = new point (P [z - 1]);
                int Q = i1;
                int R = i2;
                int R2 = i3;
                double dis = sqr (pl.x - P [i1].x) + sqr (pl.y - P [i1].y);
                if (sqr (pl.x - P [i2].x) + sqr (pl.y - P [i2].y) > dis)
                {
                    Q = i2;
                    R = i1;
                    R2 = i3;
                    dis = sqr (pl.x - P [i2].x) + sqr (pl.y - P [i2].y);
                }
                if (sqr (pl.x - P [i3].x) + sqr (pl.y - P [i3].y) > dis)
                {
                    Q = i3;
                    R = i1;
                    R2 = i2;
                }
                if (sameside (cen, P [Q], P [R], pl))
                    R = R2;
                check3 (R, Q, z - 1);
            }
            else
                radius = Math.sqrt (radius); //avoids sqrt in above calculations
        }
    }

    
    public static double sqr (double a)
    {
        return(a*a);
    }
    
    public static boolean check (int pos)
    {
        if (pos > 1)    //initial segment & first segment can't intersect or be span more than D=2
        {
            boolean good = true;
            P = new point[pos+2];
            P[0] = new point (0,0);
            P[1] = new point (1,0);
            int z = 2;
            double a = 0;
            while(z < pos+2 && good)
            {
                a += angles[ sequence[z-2] - 1 ];
                P[z] = new point (P[z-1].x + Math.cos(a),P[z-1].y + Math.sin(a));
                //System.out.println ("P["+z+"] = new point (" + P[z].x + ","+P[z].y+");");
                z++;
            }                             
            check2 (0,1);
            good = radius <= D / 2;
            if (good) //check if intersection
            {
                //solve for last segment's equation:
                double m = (P [pos + 1].y - P [pos].y) / (P [pos + 1].x - P [pos].x);
                double b = P [pos + 1].y - m * P [pos + 1].x;
                double xi; //x of intersection of lines/equations
                double m2, b2; //used for each other segment
                z = 1;
                while (z < pos && good)
                {
                    m2 = (P [z].y - P [z - 1].y) / (P [z].x - P [z - 1].x); //solve for this segment's equation:
                    b2 = P [z].y - m2 * P [z].x;
                    xi = (b2 - b) / (m - m2);   //x-coordinate of intersection
                    good = (xi < P [pos].x - d && xi < P [pos + 1].x - d) || (xi > P [pos].x + d && xi > P [pos + 1].x + d) || (xi < P [z - 1].x - d && xi < P [z].x - d) || (xi > P [z - 1].x + d && xi > P [z].x + d);
                    //System.out.println("m2: " + m2 + "  b2: " + b2);
                    z++;
                }                    
            }
            return (good);
    }
    else
        return (true);
    }

    /* xs,ys is where new segment continues from */
    public static void recursion (int pos)
    {
        for (int k = 1 ; k < N ; k++)
        {
            sequence [pos - 1] = k;
            //System.out.println("\npos: " + pos + "  xn: " + xn + "  yn: " + yn);
            if (check (pos))
            {
                if (pos > max)
                {
                    max = pos;
                    //writeS ();
                    System.out.print ("\nMax:" + (pos + 1) + "::: ");                    
                    for (int z = 0; z < max; z++)
                       System.out.print (sequence[z] + " ");
                }
                else if (pos == max)
                {
                    System.out.print ("\nMax, tie: " + (pos + 1) + "    ");
                    for (int z = 0 ; z < pos ; z++)
                        System.out.print (sequence [z] + " ");
                }
                recursion (pos + 1);
            }
        }
    }

    public static void main (String [] args)
    {
        //update = 0;
        max = 0;
        d = 0.000001;   //error distance        
        D = 4;
        N = 7;
        sequence = new int [40];
        System.out.println ("N: " + N + "   D: " + D);
        angles = new double [N-1];
        for (int k = 1; k < N; k++)
            angles[k-1] = (Math.PI * (2 * (double) k / N - 1)); //radians
        for (int z = 1; z < N/2+1; z++)
        {
            sequence[0] = z;
            recursion (2);
            //System.out.println("\nDone: " + z);
        }
        /*point p1 = new point (-0.26604444311897835,0.223237794097899);
        point p2 = new point (2.2660444431189775,0.22323779409790012);
        point p3 = new point (-1.1454296846907956,0.22323779409790057);
        System.out.println ("Angle(3,7,11): " + angle(p1,p2,p3));
        System.out.println ("Angle(7,3,11): " + angle(p2,p1,p3));
        System.out.println ("Angle(3,11,7): " + angle(p1,p3,p2)); */       
        System.out.print (/*"\n@ " + (max+1) +*/ " Finished");
        System.out.println ();
    } // main method
} // Snakes class   2:16

/*
    N                   D                                  Possible Angles (Degrees)
    5     3 4 5 6 7 8 9 10 11 12 13 14          -108    -36    36   108
    7   2 3 4 5 6 7 8 9 10 11                   -129    -77   -26    26    77   129
    8   2 3 4 5 6 7 8 9 10                      -135    -90   -45     0    45    90   135
    9   2 3 4 5 6 7 8 9                         -140   -100   -60   -20    20    60   100   140
    10  2 3 4 5 6 7 8                           -144   -108   -72   -36     0    36    72   108   144
    11  2 3 4 5 6 7                             -147   -115   -82   -49   -16    16    82   115   147
    12    3 4 5 6 7                             -150   -120   -90   -60   -30     0    30    60    90   120   150

    Total Score: 23.353 / 27	Ranking: 23   Average: 0.8649
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
