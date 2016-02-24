import java.lang.Math;
import java.io.*;

public class Snakes2
{
//    static long update;
    static double t;       //temp variable
    static double x1;      //used for display & check
    static double y1;
    static double xn;
    static double yn;
    static double d;
    static int N;       //N-1 possible turning sequence between segments
    static double D;    //diameter of circle
    static double angles [];
    static int sequence [];  //number sequence to be entered as solution
    static int max;

    public static double sqr (double a)
    {
        return(a*a);
    }
    
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
    
    public static boolean check (int pos, double xz, double yz, double xc, double yc)
    {
        if (pos > 1)    //initial segment & first segment can't intersect or be span more than D=2
        {
        xc = (xc*(pos+1)+xn)/(pos+2);
        yc = (yc*(pos+1)+yn)/(pos+2);
        if (xc*xc + yc*yc < D*D/4 + d)   //first point
        {
            if (sqr(1-xc) + yc*yc < D*D/4 + d)   //second point
            {
                boolean good = true;
                xn = 1;
                yn = 0;
                int z = 0;
                double a = 0;
                while(z < pos && good)
                {
                    a += angles[ sequence[z] - 1 ];
                    xn += Math.cos(a);
                    yn += Math.sin(a);
                    good = (sqr(xn-xc) + sqr(yn-yc) < D*D/4 + d);
                    z++;
                }                             
                if (good) //check if intersection
                {
                    double m = (yn - yz) / (xn - xz);
                    double b = yn - m * xn;
                    double m2, b2; //used for each other segment
                    double xi; //x of intersection of lines/equations
                    a = 0;
                    double x2 = 1;
                    double y2 = 0;
                    xi = -b / m;
                    good = (xi < xz - d && xi < xn - d) || (xi > xz + d && xi > xn + d) || (xi < - d && xi < 1 - d) || (xi > d && xi > 1 + d);
                    z = 0;
                    while (z < pos - 2 && good) //-2 because it's impossible to intersect with itself or the previous segment
                    {
                        a += angles[ sequence[z]-1 ];
                        x1 = x2;
                        y1 = y2;
                        x2 = x1 + Math.cos(a);
                        y2 = y1 + Math.sin(a);
                        if (sqr(x1-xn) + sqr(y1-yn) < 4 && sqr(x2-xn) + sqr(y2-yn) < 4)
                        {
                            //solve for this segment's equation
                            m2 = (y2 - y1) / (x2 - x1);
                            b2 = y2 - m2 * x2;
                            xi = (b2 - b) / (m - m2);
                            good = (xi < xz - d && xi < xn - d) || (xi > xz + d && xi > xn + d) || (xi < x1 - d && xi < x2 - d) || (xi > x1 + d && xi > x2 + d);
                        }
                        z++;
                    }
                }
                return (good);
            }
            else
                return (false);
        }
        else
            return (false);
    }
    else
        return (true);
    }

    /* xs,ys is where new segment continues from */
    public static void recursion (int pos, double xs, double ys, double a, double xc, double yc)
    {
        for (int k = 1 ; k < N ; k++)
        {
            sequence [pos - 1] = k;
            t = a + angles[k-1];
            xn = xs + Math.cos(t);
            yn = ys + Math.sin(t);
            //System.out.println("\npos: " + pos + "  xn: " + xn + "  yn: " + yn);
            if (check (pos, xs, ys,xc,yc))
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
                recursion (pos + 1, xn, yn, t,(xc*(pos+1)+xn)/(pos+2),(yc*(pos+1)+yn)/(pos+2));
            }
        }
    }

    public static void main (String [] args)
    {
        sequence = new int [500];
        //update = 0;
        max = 0;
        d = 0.000001;   //error distance        
        D = 4;
        N = 11;
        System.out.println ("N: " + N + "   D: " + D);
        angles = new double [N-1];
        for (int k = 1; k < N; k++)
            angles[k-1] = (Math.PI * (2 * (double) k / N - 1)); //radians
        /*for (int z = 1; z < N/2+1; z++)
        {
            sequence[0] = z;
            recursion (2, 1+Math.cos(angles[z-1]), Math.sin(angles[z-1]), angles[z-1], (2.5+Math.cos(angles[z-1]))/4, Math.sin(angles[z-1])/4);
            System.out.println("\nDone: " + z);
        }*/
        recursion (1,1,0,0,0.5,0);
        /*readS ();
        display (max);*/
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

    Total Score: 21.2128 / 26	Ranking: 20
    Scores:
    5,3     0.8824      15      ==> 17
    5,4     0.9697      32      ==> 33
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
        Score N=5:  6.6145 / 8
    7,2     1.0000      7       ==> 7
    7,3     0.8500      17      ==> 20
    7,4     0.8837      38      ==> 43
    7,5
    7,6
    7,7
    7,8
    7,9
    7,10
    7,11
        Score N=7:  2.7337 / 3
    8,2     0.8750      7       ==> 8
    8,3     0.7727      17      ==> 22
    8,4     0.7500      33      ==> 44
    8,5     0.6389      46      ==> 72
    8,6
    8,7
    8,8
    8,9
    8,10
        Score N=8:  3.0366 / 4
    9,2     0.6666      8       ==> 12
    9,3     0.9630      26      ==> 27
    9,4     0.7457      44      ==> 59
    9,5     0.6832      69      ==> 101
    9,6
    9,7
    9,8
    9,9
        Score N=9:  3.0585 / 4
    10,2    0.8889      8       ==> 9
    10,3    0.9131      21      ==> 23
    10,4    0.8367      41      ==> 49
    10,5
    10,6
    10,7
    10,8
        Score N=10: 2.6387 / 3
    11,2    0.9091      10      ==> 11
    11,3    0.9118      31      ==> 34
    11,4    0.6184      47      ==> 76
    11,5
    11,6
    11,7
        Score N=11: 2.4393 / 3
    12,3    0.8181      27      ==> 33
    12,4    0.8182      54      ==> 66
    12,5
    12,6
    12,7
        Score N=12: 0.8181 / 1
*/
