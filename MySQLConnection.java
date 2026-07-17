package JDBC;
import java.sql.Connection;
import java.sql.DriverManager;
public class MySQLConnection {
    public static void main(String[] args) {

        String url = "jdbc:mysql://localhost:3306/testdb";
        String username = "root";
        String password = "root";

        try {
            Class.forName("com.mysql.cj.jdbc.Driver");

            Connection con = DriverManager.getConnection(url, username, password);

            System.out.println("Connection Established Successfully!");

            con.close();
        } catch (Exception e) {
            System.out.println("Connection Failed!");
            e.printStackTrace();
        }
    }
}

// git add .
// git commit -m "Initial commit"
// git push -u origin main
