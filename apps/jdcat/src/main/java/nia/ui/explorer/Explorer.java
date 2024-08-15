package nia.ui.explorer;

import javax.swing.BorderFactory;
import javax.swing.JPanel;

import nia.ui.IController;
import nia.ui.explorer.files.FilesView;
import nia.ui.explorer.volumes.VolumesView;

import java.awt.BorderLayout;

public class Explorer extends JPanel {
    private VolumesView _volumes_frame;
    private FilesView _files_frame;

    public Explorer(IController controller) {

        _volumes_frame = new VolumesView(controller.get_volumes_ctrl());
        _volumes_frame.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5));

        _files_frame = new FilesView(controller.get_files_ctrl());
        _files_frame.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5));

        this.setLayout(new BorderLayout());
        this.add(_volumes_frame, BorderLayout.WEST);
        this.add(_files_frame, BorderLayout.CENTER);
    }
}
