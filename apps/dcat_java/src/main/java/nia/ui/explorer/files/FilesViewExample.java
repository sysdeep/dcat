package nia.ui.explorer.files;

import java.util.ArrayList;
import java.awt.Dimension;
// import java.awt.Font;

import javax.swing.JFrame;
import javax.swing.SwingUtilities;
// import javax.swing.JLabel;

import nia.core.models.FileRecord;
import nia.core.models.Volume;
import nia.lib.Observer;

public class FilesViewExample {

    public static void main(String[] args) {

        // enable anti-aliased text:
        System.setProperty("awt.useSystemAAFontSettings", "on");

        FilesControllerMock files_ctrl = new FilesControllerMock();

        SwingUtilities.invokeLater(() -> {
            JFrame frame = new JFrame();

            FilesView view = new FilesView(files_ctrl);
            // view.setFont(new Font("ubuntu", Font.PLAIN, 18));

            // JLabel label = new JLabel("Example");
            // label.setFont(new Font("ubuntu", Font.PLAIN, 18));

            // frame.add(label);
            frame.add(view);

            frame.setPreferredSize(new Dimension(800, 400));
            frame.pack();
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.setVisible(true);

            // start
            files_ctrl.start();
        });

    }

}

class FilesControllerMock implements FilesInterface {
    ArrayList<FileRecord> _files;
    ArrayList<FileRecord> _files_dataset_1;
    ArrayList<FileRecord> _files_dataset_2;
    ArrayList<FileRecord> _files_dataset_3;
    ArrayList<Observer> _observers;
    Volume _selected_volume;

    public FilesControllerMock() {
        _files = new ArrayList<>();
        _files_dataset_1 = new ArrayList<>();
        _files_dataset_2 = new ArrayList<>();
        _files_dataset_3 = new ArrayList<>();

        for (int i = 0; i < 13; i++) {

            String id = Integer.toString(i);
            String name_1 = "file_1 " + id;
            String name_2 = "file_2 " + id;
            String name_3 = "file_3 " + id;

            Integer type = 0;
            if (i == 2) {
                type = FileRecord.TYPE_DIR;
            } else {
                type = FileRecord.TYPE_FILE;
            }
            _files_dataset_1.add(new FileRecord(id, name_1, type));
            _files_dataset_2.add(new FileRecord(id, name_2, type));
            _files_dataset_3.add(new FileRecord(id, name_3, type));
        }

        _observers = new ArrayList<>();
    }

    public void start() {
        _files = _files_dataset_1;
        notifyObservers(list_changed);
    }

    @Override
    public void register(Observer obj) {
        _observers.add(obj);
    }

    @Override
    public void unregister(Observer obj) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'unregister'");
    }

    @Override
    public void notifyObservers(String event) {
        for (Observer obs : _observers) {
            obs.update(event);
        }
    }

    // @Override
    // public ArrayList<Volume> get_volumes() {
    // return _volumes;
    // }

    // @Override
    // public void select_volume(Volume volume) {
    // _selected_volume = volume;
    // }

    // @Override
    // public ArrayList<FileRecord> get_volume_files() {
    // return _files;
    // }

    @Override
    public ArrayList<FileRecord> get_files() {
        return _files;
    }

    @Override
    public void set_file(FileRecord record) {
        System.out.println("set_file: " + record.name);

        // only record with id == 2 change list
        if (record.type == FileRecord.TYPE_FILE) {
            return;
        }

        if (_files.equals(_files_dataset_1)) {
            _files = _files_dataset_2;
            notifyObservers(list_changed);
            return;
        }

        if (_files == _files_dataset_2) {
            _files = _files_dataset_3;
            notifyObservers(list_changed);
            return;
        }

        if (_files == _files_dataset_3) {
            _files = _files_dataset_1;
            notifyObservers(list_changed);
            return;
        }

    };

    @Override
    public void set_volume(Volume volume) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'set_volume'");
    }

    // @Override
    // public Volume get_volume() {
    // // TODO Auto-generated method stub
    // throw new UnsupportedOperationException("Unimplemented method 'get_volume'");
    // }

}
