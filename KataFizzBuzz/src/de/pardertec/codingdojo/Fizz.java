package de.pardertec.codingdojo;

/**
 * Created by Thiemo on 05.03.2016.
 */


public class Fizz {

    public static final String FIZZ = "Fizz";
    public static final String BUZZ = "Buzz";
    public static final String FIZZBUZZ = "FizzBuzz";

    public String buzz(int i) {
        if(isBuzz(i)&&isFizz(i))
            return FIZZBUZZ;

       else if(isFizz(i))
            return FIZZ;

        else if(isBuzz(i))
            return BUZZ;

        else return String.valueOf(i);
    }

    private boolean isBuzz(int i) {
        return isDividableBy(i,5) || String.valueOf(i).contains("5");
    }

    private boolean isFizz(int i) {
        return isDividableBy(i,3) || String.valueOf(i).contains("3");
    }

    private boolean isDividableBy(int i, int divisor) {
        return i%divisor==0;
    }

    public String[] getFizzBuzzArray(int arraySize) {
        String[] stringArray = new String[arraySize];
        for (int i = 0; i < stringArray.length; i++) {
            stringArray[i] = buzz(i+1);
        }
        return stringArray;
    }
}
