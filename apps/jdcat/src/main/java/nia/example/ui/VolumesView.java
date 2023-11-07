package nia.example.ui;

import java.util.ArrayList;

import javax.swing.JPanel;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;
import javax.swing.JList;
import javax.swing.JLabel;
import java.awt.BorderLayout;
import java.awt.Dimension;

import nia.example.core.models.Volume;
import nia.example.lib.Observer;

// NOTE: JList - https://www.geeksforgeeks.org/java-swing-jlist-with-examples/
public class VolumesView extends JPanel implements ListSelectionListener, Observer {
    VolumesInterface controller;
    JList<String> list;
    ArrayList<Volume> current_volumes;

    public VolumesView(VolumesInterface controller) {
        this.controller = controller;
        this.controller.register(this);

        this.setup_ui();

        // start
        this._update_list();

    }

    private void setup_ui() {
        this.setLayout(new BorderLayout());
        this.setPreferredSize(new Dimension(200, 400));

        // title
        this.add(new JLabel("volumes list"), BorderLayout.NORTH);

        // list
        this.list = new JList<String>();
        this.list.addListSelectionListener(this);
        this.add(list, BorderLayout.CENTER);
    }

    private void _update_list() {
        // TODO: check if storage loaded
        // TODO: clear

        current_volumes = controller.get_volumes();
        // NOTE:
        // https://copyprogramming.com/howto/how-to-convert-the-object-to-string-in-java
        String volumes_str[] = current_volumes.stream().map(volume -> volume.name).toArray(String[]::new);
        this.list.setListData(volumes_str);

        // TODO: check len
        this.list.setSelectedIndex(0); // NOTE: сразу вызывает событие
    }

    @Override
    public void valueChanged(ListSelectionEvent arg0) {

        Volume volume = current_volumes.toArray(Volume[]::new)[this.list.getSelectedIndex()];
        this.controller.select_volume(volume);

        // ArrayList<FileRecord> files = controller.get_volume_files(volume.id, false);

        // for (FileRecord record : files) {
        // System.err.println("\t -> " + record.name);
        // }
    }

    // https://www.digitalocean.com/community/tutorials/observer-design-pattern-in-java
    @Override
    public void update(String event) {

        switch (event) {
            case VolumesInterface.event_open_storage:
                this._update_list();
                break;

            default:
                break;
        }

    }

    // @Override
    // public void setSubject(Subject sub) {
    // // TODO Auto-generated method stub
    // throw new UnsupportedOperationException("Unimplemented method 'setSubject'");
    // }

}
