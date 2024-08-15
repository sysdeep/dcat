package nia.ui;

// пример оконного приложения
import java.awt.BorderLayout;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.io.File;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JPanel;

import nia.ui.actions_bar.ActionsBarView;
import nia.ui.explorer.Explorer;
import nia.ui.toolbar.ToolbarView;

import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JMenu;
import javax.swing.AbstractAction;

/**
 * @author DarkRaha
 * 
 */
public class MainWindow extends JFrame {
    private String title_prefix = "JDCat";
    IController _controller;

    ToolbarView _toolbar;
    JPanel _explorer;
    ActionsBarView _actions_bar;

    public MainWindow(IController controller) {

        // controller
        this._controller = controller;

        // menu
        JMenuBar main_menu = new JMenuBar();
        this.setJMenuBar(main_menu);

        main_menu.add(create_file_menu());

        // добавление и настройка компонент -----------------------------------
        Container container = getContentPane(); // клиентская область окна
        container.setLayout(new BorderLayout()); // выбираем компоновщик

        // tool bar -----------------------------------------------------------
        _toolbar = new ToolbarView();
        container.add(_toolbar, BorderLayout.NORTH);

        // explorer -----------------------------------------------------------
        this._explorer = new Explorer(this._controller);
        container.add(this._explorer, BorderLayout.CENTER);

        // actions bar --------------------------------------------------------
        _actions_bar = new ActionsBarView();
        container.add(_actions_bar, BorderLayout.SOUTH);

        // настройка окна -----------------------------------------------------
        setTitle(this.title_prefix);
        setPreferredSize(new Dimension(1024, 600));
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        pack();
        setVisible(true);
    }

    // запуск оконного приложения
    // public static void main(String args[]) {
    // new MyWin();
    // }

    private JMenu create_file_menu() {
        // Создание выпадающего меню
        JMenu file = new JMenu("Файл");
        // Пункт меню "Открыть" с изображением
        JMenuItem open = new JMenuItem("Открыть",
                new ImageIcon("images/open.png"));
        // Пункт меню из команды с выходом из программы
        JMenuItem exit = new JMenuItem(new ExitAction());
        // Добавление к пункту меню изображения
        exit.setIcon(new ImageIcon("images/exit.png"));
        // Добавим в меню пункта open
        file.add(open);
        // Добавление разделителя
        file.addSeparator();
        file.add(exit);

        // NOTE:
        // https://www.codejava.net/java-core/the-java-language/java-8-lambda-listener-example
        open.addActionListener(e -> {
            System.out.println("ActionListener.actionPerformed : open");

            JFileChooser fileChooser = new JFileChooser();
            fileChooser.setCurrentDirectory(new File(System.getProperty("user.home")));
            int result = fileChooser.showOpenDialog(this._explorer);
            if (result == JFileChooser.APPROVE_OPTION) {
                File selectedFile = fileChooser.getSelectedFile();
                this._controller.open_db(selectedFile.getAbsolutePath());
            }

        });
        return file;
    }

    /**
     * Вложенный класс завершения работы приложения
     */
    class ExitAction extends AbstractAction {
        private static final long serialVersionUID = 1L;

        ExitAction() {
            putValue(NAME, "Выход");
        }

        public void actionPerformed(ActionEvent e) {
            System.exit(0);
        }
    }
}