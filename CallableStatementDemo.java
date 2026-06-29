package JDBC;

import java.sql.*;

public class CallableStatementDemo {

    static final String URL = "jdbc:mysql://localhost:3306/employee_db";
    static final String USER = "root";
    static final String PASSWORD = "password";

    public static void main(String[] args) {

        try {
            Class.forName("com.mysql.cj.jdbc.Driver");

            Connection con = DriverManager.getConnection(URL, USER, PASSWORD);

            CallableStatement cs = con.prepareCall("{call GetEmployee(?)}");

            cs.setInt(1, 101);

            ResultSet rs = cs.executeQuery();

            while (rs.next()) {
                System.out.println("ID      : " + rs.getInt("emp_id"));
                System.out.println("Name    : " + rs.getString("emp_name"));
                System.out.println("Salary  : " + rs.getDouble("salary"));
            }

            rs.close();
            cs.close();
            con.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}