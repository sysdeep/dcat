package nia.example.ui;

import javax.swing.JPanel;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;
import java.util.ArrayList;

import nia.example.lib.Observer;
import nia.example.core.models.FileRecord;
import nia.example.core.models.Volume;

import javax.swing.JList;
import javax.swing.JLabel;
import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.GridLayout;

// NOTE: JList - https://www.geeksforgeeks.org/java-swing-jlist-with-examples/
public class FilesView extends JPanel implements ListSelectionListener, Observer {
    FilesInterface controller;
    JList<String> list;
    ArrayList<FileRecord> current_files = new ArrayList<FileRecord>();

    public FilesView(FilesInterface controller) {
        this.controller = controller;
        this.setup_ui();
        this.controller.register(this);

    }

    private void setup_ui() {
        this.setLayout(new BorderLayout());
        this.setPreferredSize(new Dimension(200, 400));

        // title
        this.add(new JLabel("files list"), BorderLayout.NORTH);

        // list
        String debug_files[] = { "file1" };
        this.list = new JList<String>(debug_files);
        this.list.addListSelectionListener(this);
        this.add(this.list, BorderLayout.CENTER);
    }

    private void _update_list() {
        // TODO: clear

        String files_str[] = current_files.stream().map(file -> file.name).toArray(String[]::new);
        this.list.setListData(files_str);

        // TODO: check len
        this.list.setSelectedIndex(0); // NOTE: сразу вызывает событие
    }

    @Override
    public void valueChanged(ListSelectionEvent arg0) {
        int index = this.list.getSelectedIndex();
        if (index < 0 || this.current_files.size() == 0)
            return;

        FileRecord selected_file = this.current_files.get(index);

        // TODO: запрашивать файлы можно если это каталог

        ArrayList<FileRecord> fff = this.controller.get_files(selected_file.id);

        // NOTE: work!
        for (FileRecord f : fff) {
            System.out.println(f.name);
        }
        // this.current_files = this.controller.get_files(selected_file.id);
        // this._update_list();
    }

    @Override
    public void update(String event) {
        System.out.println("FilesView on update: " + event);
        switch (event) {
            case FilesInterface.event_volume_selected:
                Volume volume = this.controller.get_volume();
                this.current_files = this.controller.get_volume_files(volume.id);
                this._update_list();
                break;

            default:
                break;
        }
    }

}
