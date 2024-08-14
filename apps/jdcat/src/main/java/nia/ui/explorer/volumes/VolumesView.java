package nia.ui.explorer.volumes;

import java.util.ArrayList;

import javax.swing.JPanel;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;
import javax.swing.JList;
import javax.swing.JLabel;
import java.awt.BorderLayout;
import java.awt.Dimension;

import nia.core.models.Volume;
import nia.lib.Observer;

// NOTE: JList - https://www.geeksforgeeks.org/java-swing-jlist-with-examples/
public class VolumesView extends JPanel implements ListSelectionListener, Observer {
    VolumesInterface _controller;
    JList<String> _list;
    ArrayList<Volume> _current_volumes;

    public VolumesView(VolumesInterface controller) {
        this._controller = controller;
        this._controller.register(this);

        this.setup_ui();
    }

    void setup_ui() {
        this.setLayout(new BorderLayout());
        this.setPreferredSize(new Dimension(200, 400));

        // title
        this.add(new JLabel("volumes list"), BorderLayout.NORTH);

        // list
        this._list = new JList<String>();
        this._list.addListSelectionListener(this);
        this.add(_list, BorderLayout.CENTER);
    }

    void _update_list() {

        // clear
        _list.clearSelection();
        _list.removeAll();

        _current_volumes = _controller.get_volumes();

        if (_current_volumes.size() > 0) {

            // NOTE:
            // https://copyprogramming.com/howto/how-to-convert-the-object-to-string-in-java
            String volumes_str[] = _current_volumes.stream()
                    .map(volume -> _make_volume_title(volume))
                    .toArray(String[]::new);
            this._list.setListData(volumes_str);

            this._list.setSelectedIndex(0);
        }

    }

    @Override
    public void valueChanged(ListSelectionEvent arg0) {

        // NOTE: отсеиваем клики, обрабатываем только выделение
        if (!arg0.getValueIsAdjusting()) {

            int index = this._list.getSelectedIndex();
            if (index < 0 || _current_volumes.size() == 0)
                return;

            Volume volume = _current_volumes.get(index);
            // System.out.println("selected volume: " + volume.name);
            this._controller.select_volume(volume);
        }
    }

    // https://www.digitalocean.com/community/tutorials/observer-design-pattern-in-java
    @Override
    public void update(String event) {

        switch (event) {
            case VolumesInterface.volumes_changed:
                this._update_list();
                break;

            default:
                break;
        }

    }

    String _make_volume_title(Volume volume) {
        return "🌎" + " " + volume.name;
    }

    // @Override
    // public void setSubject(Subject sub) {
    // // TODO Auto-generated method stub
    // throw new UnsupportedOperationException("Unimplemented method 'setSubject'");
    // }

}
