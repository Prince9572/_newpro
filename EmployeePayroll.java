package JDBC;

import java.sql.*;

public class EmployeePayroll {

    static final String URL = "jdbc:mysql://localhost:3306/payroll_db";
    static final String USER = "root";
    static final String PASSWORD = "password";

    public static void main(String[] args) {

        Connection con = null;

        try {
            Class.forName("com.mysql.cj.jdbc.Driver");

            con = DriverManager.getConnection(URL, USER, PASSWORD);

            con.setAutoCommit(false);

            int empId = 101;
            String name = "Prince Kumar";
            String department = "IT";
            double basicSalary = 50000;

            double hra = basicSalary * 0.20;
            double da = basicSalary * 0.10;
            double grossSalary = basicSalary + hra + da;
            double tax = grossSalary * 0.10;
            double netSalary = grossSalary - tax;

            String sql = "INSERT INTO employee VALUES(?,?,?,?,?,?,?,?)";

            PreparedStatement ps = con.prepareStatement(sql);

            ps.setInt(1, empId);
            ps.setString(2, name);
            ps.setString(3, department);
            ps.setDouble(4, basicSalary);
            ps.setDouble(5, hra);
            ps.setDouble(6, da);
            ps.setDouble(7, tax);
            ps.setDouble(8, netSalary);

            int rows = ps.executeUpdate();

            con.commit();

            System.out.println(rows + " Employee Record Inserted Successfully");

            System.out.println("Net Salary = " + netSalary);

            ps.close();
            con.close();

        } catch (Exception e) {

            try {
                if (con != null) {
                    con.rollback();
                    System.out.println("Transaction Rolled Back");
                }
            } catch (SQLException ex) {
                ex.printStackTrace();
            }

            e.printStackTrace();
        }
    }
}