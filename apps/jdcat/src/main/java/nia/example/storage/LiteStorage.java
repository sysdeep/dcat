package nia.example.storage;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;

import org.apache.logging.log4j.Logger;

import nia.example.core.models.FileRecord;
import nia.example.core.models.Volume;
import nia.example.lib.Log;

public class LiteStorage implements Storage {
    private String _db_file_path;
    Connection conn = null;
    Logger log;

    public LiteStorage() {
        log = Log.get_logger(LiteStorage.class.getName());

    }

    public void open(String db_path) {
        this._db_file_path = db_path;
        this._open();
    }

    private void _open() {
        Log.get_logger(LiteStorage.class.getName()).info("open: " + this._db_file_path);

        String url = String.format("jdbc:sqlite:%s", _db_file_path);

        try {
            // db parameters
            // "jdbc:sqlite:/tmp/chinook.db"

            // create a connection to the database
            conn = DriverManager.getConnection(url);

            log.info("Connection to SQLite has been established.");

        } catch (SQLException e) {
            log.error(e.getMessage());
        } finally {
            // try {
            // if (conn != null) {
            // conn.close();
            // }
            // } catch (SQLException ex) {
            // log.error(ex.getMessage());
            // }
        }

        // String sql = "SELECT id, name FROM volumes";

        // try {
        // Statement stmt = conn.createStatement();
        // ResultSet rs = stmt.executeQuery(sql);

        // // loop through the result set
        // while (rs.next()) {
        // System.out.println(rs.getInt("id") + "\t" +
        // rs.getString("name"));
        // }

        // } catch (SQLException e) {
        // log.error(e);
        // }

    }

    @Override
    public void ping() {
        Log.get_logger(LiteStorage.class.getName()).info("ping");

    }

    @Override
    public Volume get_volume() {

        String sql = "SELECT id, uuid, name FROM volumes";

        try {
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery(sql);

            // TODO: null list

            // loop through the result set
            while (rs.next()) {

                Volume record = new Volume();
                record.id = rs.getString("uuid");
                record.name = rs.getString("name");
                return record;
            }

        } catch (SQLException e) {
            log.error(e);
        }

        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'get_volume'");
    }

    @Override
    public ArrayList<Volume> get_volumes() {
        ArrayList<Volume> result = new ArrayList<Volume>();

        String sql = "SELECT id, uuid, name FROM volumes";

        try {
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery(sql);

            // loop through the result set
            while (rs.next()) {
                System.out.println(rs.getInt("id") + "\t" +
                        rs.getString("name"));

                Volume vol = new Volume();
                vol.id = rs.getString("uuid");
                vol.name = rs.getString("name");

                result.add(vol);
            }

            return result;

        } catch (SQLException e) {
            log.error(e);

            // TODO: как вызвать exception?
            return result;
        }
    }

    @Override
    public ArrayList<FileRecord> get_volume_files(String volume_id, Boolean is_root) {
        ArrayList<FileRecord> result = new ArrayList<FileRecord>();

        String sql = "SELECT uuid, parent_id, volume_id, name, type, rights, sowner, sgroup, size, ctime, atime, mtime, category, description";
        sql += " FROM files WHERE volume_id = ? AND parent_id='0'";

        try {
            PreparedStatement stmt = conn.prepareStatement(sql);
            stmt.setString(1, volume_id);

            ResultSet rs = stmt.executeQuery();

            while (rs.next()) {
                FileRecord record = new FileRecord(rs.getString("uuid"), rs.getString("name"));
                result.add(record);
            }

            return result;

        } catch (SQLException e) {
            log.error(e);

            // TODO: как вызвать exception?
            return result;
        }

    }

    public ArrayList<FileRecord> get_files(String parent_id) {
        ArrayList<FileRecord> result = new ArrayList<FileRecord>();

        String sql = "SELECT uuid, parent_id, volume_id, name, type, rights, sowner, sgroup, size, ctime, atime, mtime, category, description";
        sql += " FROM files WHERE parent_id=?";

        try {
            PreparedStatement stmt = conn.prepareStatement(sql);
            stmt.setString(1, parent_id);

            ResultSet rs = stmt.executeQuery();

            while (rs.next()) {
                FileRecord record = new FileRecord(rs.getString("uuid"), rs.getString("name"));
                result.add(record);
            }

            return result;

        } catch (SQLException e) {
            log.error(e);

            // TODO: как вызвать exception?
            return result;
        }

    }

}
