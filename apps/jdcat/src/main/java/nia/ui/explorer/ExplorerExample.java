package nia.ui.explorer;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Container;
import java.awt.Dimension;
import java.util.ArrayList;

import javax.swing.JFrame;
import javax.swing.SwingUtilities;

import nia.core.models.FileRecord;
import nia.core.models.Volume;
import nia.lib.Observer;
import nia.ui.IController;
import nia.ui.explorer.files.FilesInterface;
import nia.ui.explorer.volumes.VolumesInterface;

public class ExplorerExample {
    public static void main(String[] args) {

        // enable anti-aliased text:
        System.setProperty("awt.useSystemAAFontSettings", "on");

        ExplorerControllerMock ctrl = new ExplorerControllerMock();

        SwingUtilities.invokeLater(() -> {
            JFrame frame = new JFrame();
            Container container = frame.getContentPane();
            container.setLayout(new BorderLayout());

            Explorer view = new Explorer(ctrl);
            // view.setFont(new Font("ubuntu", Font.PLAIN, 18));

            // JLabel label = new JLabel("Example");
            // label.setFont(new Font("ubuntu", Font.PLAIN, 18));

            container.setBackground(Color.red);
            view.setBackground(Color.green);

            // frame.add(label);
            container.add(view, BorderLayout.CENTER);

            frame.setPreferredSize(new Dimension(800, 400));
            frame.pack();
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.setVisible(true);

            // start
            // ctrl.start();
        });

    }
}

class ExplorerControllerMock implements IController {
    VolumesInterface _volumes_ctrl;
    FilesInterface _files_ctrl;

    public ExplorerControllerMock() {
        _volumes_ctrl = new VolumesControllerMock();
        _files_ctrl = new FilesControllerMock();
    }

    @Override
    public VolumesInterface get_volumes_ctrl() {
        return _volumes_ctrl;
    }

    @Override
    public FilesInterface get_files_ctrl() {
        return _files_ctrl;
    }

    @Override
    public void open_db(String db_path) {
    }
}

class VolumesControllerMock implements VolumesInterface {

    @Override
    public void register(Observer obj) {
    }

    @Override
    public void unregister(Observer obj) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'unregister'");
    }

    @Override
    public void notifyObservers(String event) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'notifyObservers'");
    }

    @Override
    public ArrayList<Volume> get_volumes() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'get_volumes'");
    }

    @Override
    public void select_volume(Volume volume) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'select_volume'");
    }
}

class FilesControllerMock implements FilesInterface {

    @Override
    public void register(Observer obj) {
    }

    @Override
    public void unregister(Observer obj) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'unregister'");
    }

    @Override
    public void notifyObservers(String event) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'notifyObservers'");
    }

    @Override
    public ArrayList<FileRecord> get_files() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'get_files'");
    }

    @Override
    public void set_volume(Volume volume) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'set_volume'");
    }

    @Override
    public void set_file(FileRecord record) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'set_file'");
    }
}