import java.util.Scanner;

public class tables { // Class names should start with an uppercase letter
    public static void main(String[] args) {
        // Print multiplication tables from 1 to 10
        for (int i = 1; i <= 10; i++) {
            for (int j = 1; j <= 10; j++) {
                System.out.print(i * j + " ");
            }
            System.out.println();
        }

        // Create a Scanner object for user input
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter a number: ");
        int n = sc.nextInt();

        // Print the multiplication table for the entered number
        for (int i = 1; i <= 10; i++) {
            System.out.println(n + " * " + i + " = " + n * i);
        }

        sc.close(); // Close the Scanner to free up resources
    }
}
