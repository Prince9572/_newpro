package JDBC;

import java.sql.*;

public class BankingSystem {

    static final String URL = "jdbc:mysql://localhost:3306/bank_db";
    static final String USER = "root";
    static final String PASSWORD = "password";

    public static void main(String[] args) {

        Connection con = null;

        try {
            Class.forName("com.mysql.cj.jdbc.Driver");

            con = DriverManager.getConnection(URL, USER, PASSWORD);

            con.setAutoCommit(false);

            int fromAcc = 101;
            int toAcc = 102;
            double amount = 5000;

            PreparedStatement debit = con.prepareStatement(
                    "UPDATE account SET balance = balance - ? WHERE acc_no = ?");

            debit.setDouble(1, amount);
            debit.setInt(2, fromAcc);

            PreparedStatement credit = con.prepareStatement(
                    "UPDATE account SET balance = balance + ? WHERE acc_no = ?");

            credit.setDouble(1, amount);
            credit.setInt(2, toAcc);

            int d = debit.executeUpdate();
            int c = credit.executeUpdate();

            if (d > 0 && c > 0) {
                con.commit();
                System.out.println("Money Transferred Successfully.");
            } else {
                con.rollback();
                System.out.println("Transaction Failed. Rolled Back.");
            }

            debit.close();
            credit.close();
            con.close();

        } catch (Exception e) {
            try {
                if (con != null) {
                    con.rollback();
                    System.out.println("Transaction Rolled Back.");
                }
            } catch (SQLException ex) {
                ex.printStackTrace();
            }
            e.printStackTrace();
        }
    }
}