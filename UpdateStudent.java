package JDBC;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;

public class UpdateStudent {
    public static void main(String[] args) {
        String url = "jdbc:mysql://localhost:3306/testdb";
        String username = "root";
        String password = "password";

        try {
            Class.forName("com.mysql.cj.jdbc.Driver");

            Connection con = DriverManager.getConnection(url, username, password);

            String sql = "UPDATE student SET name=?, age=? WHERE id=?";
            PreparedStatement ps = con.prepareStatement(sql);

            ps.setString(1, "Rahul");
            ps.setInt(2, 21);
            ps.setInt(3, 101);

            int rows = ps.executeUpdate();

            System.out.println(rows + " record updated successfully.");

            ps.close();
            con.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}