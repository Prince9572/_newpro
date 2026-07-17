package JDBC;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;

public class DeleteStudent {
    public static void main(String[] args) {
        String url = "jdbc:mysql://localhost:3306/testdb";
        String username = "root";
        String password = "password";

        try {
            Class.forName("com.mysql.cj.jdbc.Driver");

            Connection con = DriverManager.getConnection(url, username, password);

            String sql = "DELETE FROM student WHERE id=?";
            PreparedStatement ps = con.prepareStatement(sql);

            ps.setInt(1, 101);

            int rows = ps.executeUpdate();

            System.out.println(rows + " record deleted successfully.");

            ps.close();
            con.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}