package de.pardertec.codingdojo;

import org.testng.annotations.Test;

import static de.pardertec.codingdojo.Fizz.BUZZ;
import static de.pardertec.codingdojo.Fizz.FIZZ;
import static org.testng.AssertJUnit.assertEquals;
import static org.testng.internal.junit.ArrayAsserts.assertArrayEquals;

/**
 * Created by Thiemo on 05.03.2016.
 */
public class FizzTest {

    private Fizz fizz = new Fizz();

    @Test
    public void testThat1Returns1() throws Exception {
        assertEquals("1", fizz.buzz(1));
    }

    @Test
    public void testThat2Returns2() throws Exception {
        assertEquals("2", fizz.buzz(2));
    }

    @Test
    public void testThat3ReturnsFizz() throws Exception {
        assertEquals(Fizz.FIZZ, fizz.buzz(3));
    }

    @Test
    public void testThat13ReturnsFizz() throws Exception {
        assertEquals(Fizz.FIZZ, fizz.buzz(13));
    }

    @Test
    public void testThat51ReturnsBuzz() throws Exception {
        assertEquals(Fizz.FIZZBUZZ, fizz.buzz(51));
    }

    @Test
    public void testThat52ReturnsBuzz() throws Exception {
        assertEquals(Fizz.BUZZ, fizz.buzz(52));
    }

    @Test
    public void testThat5ReturnsBuzz() throws Exception {
        assertEquals("Buzz", fizz.buzz(5));
    }


    @Test
    public void testThat15ReturnsFizzBuzz() throws Exception {
        assertEquals("FizzBuzz", fizz.buzz(15));
    }

    @Test
    public void testThatArrayIsReturnedFor10() throws Exception {
        //arrange
        String[] expectedValues = new String[]{"1", "2", FIZZ, "4", BUZZ, FIZZ, "7", "8", FIZZ, BUZZ};

        //act
        String[] result = fizz.getFizzBuzzArray(10);

        //assert
        assertArrayEquals(expectedValues, result);
    }

    @Test
    public void testThatArrayIsReturned2() throws Exception {
        //arrange
        String[] expectedValues = new String[]{"1", "2"};

        //act
        String[] result = fizz.getFizzBuzzArray(2);

        //assert
        assertArrayEquals(expectedValues, result);
    }
}
