package JDBC;

import java.sql.*;

public class BatchProcessingDemo {

    static final String URL = "jdbc:mysql://localhost:3306/student_db";
    static final String USER = "root";
    static final String PASSWORD = "password";

    public static void main(String[] args) {

        try {
            Class.forName("com.mysql.cj.jdbc.Driver");

            Connection con = DriverManager.getConnection(URL, USER, PASSWORD);

            Statement st = con.createStatement();

            st.addBatch("INSERT INTO student VALUES(101,'Prince',20)");
            st.addBatch("INSERT INTO student VALUES(102,'Rahul',21)");
            st.addBatch("INSERT INTO student VALUES(103,'Amit',22)");

            int[] result = st.executeBatch();

            System.out.println("Records Inserted: " + result.length);

            st.close();
            con.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}