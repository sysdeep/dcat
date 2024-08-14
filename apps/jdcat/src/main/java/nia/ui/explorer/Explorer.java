package nia.ui.explorer;

import javax.swing.JPanel;

import nia.ui.IController;
import nia.ui.explorer.files.FilesView;
import nia.ui.explorer.volumes.VolumesView;

import java.awt.BorderLayout;
import java.awt.FlowLayout;

public class Explorer extends JPanel {
    private VolumesView _volumes_frame;
    private FilesView _files_frame;

    public Explorer(IController controller) {

        this._volumes_frame = new VolumesView(controller.get_volumes_ctrl());
        this._files_frame = new FilesView(controller.get_files_ctrl());

        this.setLayout(new FlowLayout());
        // Container c = getContentPane(); // клиентская область окна
        // c.setLayout(new BorderLayout()); // выбираем компоновщик
        // // метку наверх
        this.add(_volumes_frame, BorderLayout.WEST);
        this.add(_files_frame, BorderLayout.EAST);
    }
}
