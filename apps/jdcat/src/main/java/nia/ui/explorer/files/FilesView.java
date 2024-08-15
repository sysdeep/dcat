package nia.ui.explorer.files;

import javax.swing.JPanel;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;
import java.util.ArrayList;

import nia.lib.Observer;
import nia.core.models.FileRecord;

import javax.swing.JList;
import javax.swing.JLabel;
import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;

public class FilesView extends JPanel implements ListSelectionListener, Observer, IActions {
    FilesInterface _controller;
    JList<String> _list;
    ArrayList<FileRecord> _current_files;

    public FilesView(FilesInterface controller) {
        _current_files = new ArrayList<FileRecord>();

        this._controller = controller;
        this._controller.register(this);

        this.setup_ui();

    }

    private void setup_ui() {
        this.setLayout(new BorderLayout());
        this.setPreferredSize(new Dimension(200, 400));

        // title
        this.add(new JLabel("files list"), BorderLayout.NORTH);

        // list
        this._list = new JList<String>();
        this._list.addListSelectionListener(this);
        new ListActionsHandler(_list, this);

        this.add(this._list, BorderLayout.CENTER);
    }

    private void _update_list() {
        // clear
        _list.clearSelection();
        _list.removeAll();

        if (_current_files.size() > 0) {

            String files_str[] = _current_files.stream().map(file -> _make_list_item(file)).toArray(String[]::new);
            this._list.setListData(files_str);

            this._list.setSelectedIndex(0); // NOTE: сразу вызывает событие
        }
    }

    @Override
    public void valueChanged(ListSelectionEvent arg0) {

        // NOTE: отсеиваем клики, обрабатываем только выделение
        if (!arg0.getValueIsAdjusting()) {

            // int index = this._list.getSelectedIndex();

            // if (index < 0 || this._current_files.size() == 0)
            // return;

            // FileRecord selected_file = this._current_files.get(index);
            // _controller.set_file(selected_file);
        }

    }

    // observer interface -----------------------------------------------------
    @Override
    public void update(String event) {
        System.out.println("FilesView on update: " + event);

        switch (event) {
            case FilesInterface.list_changed:
                _current_files = _controller.get_files();
                this._update_list();
                break;

            default:
                break;
        }
    }

    // IActions interface -----------------------------------------------------
    @Override
    public void do_open() {
        int index = _list.getSelectedIndex();

        if (index < 0 || _current_files.size() == 0)
            return;

        FileRecord selected_file = _current_files.get(index);
        _controller.set_file(selected_file);
    }

    // private ----------------------------------------------------------------
    String _make_list_item(FileRecord record) {

        String type_str = "🌎";
        if (record.type == FileRecord.TYPE_DIR) {
            type_str = "📁";
        } else if (record.type == FileRecord.TYPE_FILE) {
            type_str = "☘";
        }

        return type_str + " " + record.name;
    }

}

abstract class KeyAdapter implements KeyListener {
    // public KeyAdapter(Consumer func) {

    // }

    public void keyTyped(KeyEvent e) {
    }

    public void keyPressed(KeyEvent e) {
    }

    public void keyReleased(KeyEvent e) {
    }
}